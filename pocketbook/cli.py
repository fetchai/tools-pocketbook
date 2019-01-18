import argparse
import base64
import os
import sys

import toml
from fetch.ledger.crypto.signing import Signing
from fetch.ledger.api.token import TokenApi

from .table import Table

CONFIG_PATH = os.path.abspath(os.path.expanduser('~/.pocketbookrc'))


def _unsigned(value):
    value = int(value)
    if value < 0:
        raise RuntimeError('Value must be greater than or equal to zero')
    return value


def _get_ledger_address(target: str, config: dict) -> (str, int):
    cfg = config.get('ledger', {}).get(target)
    if cfg is None:
        raise RuntimeError('No ledger configuration present. Please run setup')
    return cfg['host'], cfg['port']


def _create_api(target: str, config: dict) -> TokenApi:
    host, port = _get_ledger_address(target, config)
    return TokenApi(host, port)


def _extract_address_book(config: dict) -> dict:
    address_book = {}
    identities = config.get('identities', {})

    # list identities first
    for name, data in identities.items():
        address_book[name] = data['public']

    # add the remote addresses next
    for name, public_key in config.get('addresses', {}).items():
        address_book[name] = public_key

    return address_book


def run_balance(args, config) -> (dict, int):
    cols = ['name', 'balance'] + (['public_key'] if args.verbose else [])
    table = Table(cols)

    # create the api
    api = _create_api(args.target, config)

    for name, identity in config.get('identities', {}).items():

        row = {
            'name': name,
            'balance': api.balance(identity['public']),
        }

        if args.verbose:
            row['public_key'] = identity['public']

        table.add_row(**row)

    table.display()

    return config, 0


def run_create_identity(args, config) -> (dict, int):
    # lookup the existing identities
    identities = config.get('identities', {})

    # check the name
    if args.name in identities:
        print('Name already exists')
        return config, 1

    # generate the new private key
    signing_key = Signing.generate_private_key()
    verifying_key = signing_key.get_verifying_key()
    private_key = base64.b64encode(signing_key.to_string()).decode()
    public_key = base64.b64encode(verifying_key.to_string()).decode()

    # store the identity
    identities[args.name] = {
        'public': public_key,
        'private': private_key,
    }

    # update the configuration
    config['identities'] = identities

    return config, 0


def run_setup(args, config) -> (dict, int):

    # lookup the existing configuration (if any)
    ledger = config.get('ledger', {})

    ledger[args.target] = {
        'host': input('Host: '),
        'port': int(input('Port: ')),
    }

    # update the configuration
    config['ledger'] = ledger

    return config, 0


def run_addresses(args, config: dict) -> (dict, int):
    # choose columns
    columns = ['name']
    if args.verbose:
        columns.append('public_key')

    table = Table(columns)

    # add the local addresses first
    address_book = _extract_address_book(config)
    for name, public_key in address_book.items():

        row = {
            'name': name,
        }

        if args.verbose:
            row['public_key'] = public_key

        table.add_row(**row)

    table.display()

    return config, 0


def run_add(args, config: dict) -> (dict, int):
    key_valid = False

    try:

        # extract and parse parameters
        name = args.name

        # attempt to parse the
        Signing.create_public_key(base64.b64decode(args.key))

        # update the addresses section of the config
        addresses = config.get('addresses', {})
        addresses[name] = args.key
        config['addresses'] = addresses

        key_valid = True

    except AssertionError:
        pass

    if not key_valid:
        print('Error public key is not valid')

    return config, 0 if key_valid else 1


def run_wealth(args, config: dict) -> (dict, int):
    identities = config.get('identities', {})

    # ensure that the name exists in our list of addresses
    identity = identities.get(args.name)

    exit_code = 1
    if identity is None:
        print('Unable to look up identity "{}"'.format(args.name))
        return config, exit_code

    # create the API
    api = _create_api(args.target, config)

    # make the request
    api.wealth(base64.b64decode(identity['private']), args.amount)

    return config, 0


def run_transfer(args, config: dict) -> (dict, int):
    # lookup the source identity
    identity = config.get('identities', {}).get(args.source)

    # sanity check the identity
    if identity is None:
        print('Unable to lookup identity "{}"'.format(args.source))
        return config, 1

    # lookup the destination address
    destination = _extract_address_book(config).get(args.destination)

    # ensure that we have the target identity
    if destination is None:
        print('Unable to look up destination address "{}"'.format(args.destination))
        return config, 1

    # create the API
    api = _create_api(args.target, config)

    # issue the transfer
    api.transfer(
        base64.b64decode(identity['private']),
        base64.b64decode(destination),
        args.amount,
    )

    return config, 0


def load_config() -> dict:
    config = dict()

    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as config_file:
            config = toml.load(config_file)

    return config


def save_config(config: dict):
    with open(CONFIG_PATH, 'w') as config_file:
        toml.dump(config, config_file)


def parse_commandline():
    parser = argparse.ArgumentParser(prog='pocketbook')
    parser.add_argument('-t', '--target', help='The name of the target being addressed')
    subparsers = parser.add_subparsers()

    # balance parser
    parser_balance = subparsers.add_parser('balance', aliases=['b'], help='Lists all the balances')
    parser_balance.add_argument('-v', '--verbose', action='store_true', help='Display extra information (if available)')
    parser_balance.set_defaults(handler=run_balance)

    parser_setup = subparsers.add_parser('setup', aliases=['s'])
    parser_setup.set_defaults(handler=run_setup)

    parser_create_ident = subparsers.add_parser('create', aliases=['c'], help='Create a new identity')
    parser_create_ident.add_argument('name', help='The name to be associated with the key')
    parser_create_ident.set_defaults(handler=run_create_identity)

    parser_addresses = subparsers.add_parser('addresses', aliases=['as'], help='List the addresses stored')
    parser_addresses.add_argument('-v', '--verbose', action='store_true',
                                  help='Display extra information (if available)')
    parser_addresses.set_defaults(handler=run_addresses)

    parser_add = subparsers.add_parser('add', aliases=['a'], help='Add an address to the address book')
    parser_add.add_argument('name', help='The name of the address')
    parser_add.add_argument('key', help='The base64 encoded key')
    parser_add.add_argument('--hex', action='store_true', help='Signal the input key is provided in hex format')
    parser_add.set_defaults(handler=run_add)

    parser_wealth = subparsers.add_parser('wealth', aliases=['w'], help='Create wealth for a given account')
    parser_wealth.add_argument('name', help='The name of the address to create wealth for')
    parser_wealth.add_argument('amount', type=_unsigned, help='The amount of balance to be added to the account')
    parser_wealth.set_defaults(handler=run_wealth)

    parser_transfer = subparsers.add_parser('transfer', aliases=['t'], help='Transfer wealth between accounts')
    parser_transfer.add_argument('source', help='The source account name to be used in the transfer')
    parser_transfer.add_argument('destination', help='The destination name to be used in the transfer')
    parser_transfer.add_argument('amount', type=_unsigned, help='The amount to be transferred')
    parser_transfer.set_defaults(handler=run_transfer)

    # parse some argument lists
    return parser, parser.parse_args()


def main():
    parser, args = parse_commandline()

    # load the previous configuration
    config = load_config()

    # select the command handler
    if hasattr(args, 'handler'):
        handler = args.handler
    else:
        parser.print_usage()
        handler = None

    # run the specified command
    exit_code = 1
    if handler is not None:
        try:

            # execute the handler
            config, exit_code = handler(args, config)

        except Exception as ex:
            print('Error:', ex)

            exit_code = 1

    # save the configuration
    save_config(config)

    # close the program with the given exit code
    sys.exit(int(exit_code))


if __name__ == '__main__':
    main()
