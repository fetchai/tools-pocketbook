import argparse
import sys
import os
import getpass

from fetchai.ledger.api import LedgerApi
from fetchai.ledger.crypto import Entity, Address
from fetchai.ledger.crypto.entity import _strong_password as is_strong_password
from fetchai.ledger.serialisation.transaction import encode_transaction

from .address_book import AddressBook
from .key_store import KeyStore
from .table import Table
from . import __version__


DISCLAIMER = """
                                == Warning ==

You use this application at your own risk. Whilst Fetch.ai have made every
effort to ensure its reliability and security, it comes with no warranty. It is
intended for the creation and management of Fetch.ai mainnet wallets and
transactions between them. You are responsible for the security of your own
private keys (see ~/.pocketbook folder). Do not use this application for
high-value operations: it is intended for utility operations on the main network.
"""


class NetworkUnavailableError(Exception):
    pass


def get_balance(api: LedgerApi, address):
    balance = int(api.tokens.balance(address))
    return balance / 10000000000


def get_stake(api: LedgerApi, addresss):
    stake = int(api.tokens.stake(addresss))
    return stake / 10000000000


def create_api(name: str) -> LedgerApi:
    try:
        return LedgerApi(network=name)
    except:
        pass

    raise NetworkUnavailableError()


def run_list(args):
    address_book = AddressBook()
    key_store = KeyStore()
    keys = key_store.list_keys()

    if len(keys) == 0:
        print('No keys present')
    else:

        # select the columns
        cols = ['name', 'type', 'balance', 'stake']
        if args.verbose:
            cols.append('address')

        api = create_api(args.network)

        table = Table(cols)
        for key in keys:
            address = key_store.lookup_address(key)
            balance = get_balance(api, address)
            stake = get_stake(api, address)

            row_data = {
                'name': key,
                'type': 'key',
                'balance': balance,
                'stake': stake,
                'address': str(address),
            }

            table.add_row(**row_data)

        for name, address in address_book.items():
            balance = get_balance(api, address)
            stake = get_stake(api, address)

            row_data = {
                'name': name,
                'type': 'addr',
                'balance': balance,
                'stake': stake,
                'address': str(address),
            }

            table.add_row(**row_data)

        table.display()


def run_create(args):
    key_store = KeyStore()

    # get the name for the new key
    while True:
        name = input('Enter name for key: ')
        if name in key_store.list_keys():
            print('Key name already exists')
            continue
        break

    # prompt the user for the password
    while True:
        password = getpass.getpass('Enter password for key...: ')
        if not is_strong_password(password):
            print('Password too simple, try again')
            continue

        confirm = getpass.getpass('Confirm password for key.: ')
        if password != confirm:
            print('Passwords did not match, try again')
            continue

        break

    key_store.add_key(name, password, Entity())


def run_display(args):
    key_store = KeyStore()

    entity = key_store.load_key(args.name, getpass.getpass('Enter password for key: '))
    address = Address(entity)

    print('Address....:', str(address))
    print('Public Key.:', str(entity.public_key))


def parse_commandline():
    parser = argparse.ArgumentParser(prog='pocketbook')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('-n', '--network', default='mainnet', help='The name of the target being addressed')
    subparsers = parser.add_subparsers()

    parser_list = subparsers.add_parser('list', aliases=['ls'], help='Lists all the balances')
    parser_list.add_argument('-v', '--verbose', action='store_true', help='Display extra information (if available)')
    parser_list.set_defaults(handler=run_list)

    parser_create = subparsers.add_parser('create', aliases=['new'], help='Create a key key')
    parser_create.set_defaults(handler=run_create)

    parser_display = subparsers.add_parser('display', help='Displays the address and public key for a private key')
    parser_display.add_argument('name', help='The name of the key')
    parser_display.set_defaults(handler=run_display)

    parser_add = subparsers.add_parser('add', help='Adds an address to the address book')
    parser_add.add_argument('name', help='The name of the key')
    parser_add.add_argument('address', type=Address, help='The account address')
    parser_add.set_defaults(handler=run_add)

    parser_transfer = subparsers.add_parser('transfer')
    parser_transfer.add_argument('destination',
                                 help='The destination address either a name in the address book or an address')
    parser_transfer.add_argument('amount', type=int, help='The amount in whole FET to be transferred')
    parser_transfer.add_argument('--from', dest='from_address', help='The signing account, required for multi-sig')
    parser_transfer.add_argument('signers', nargs='+', help='The series of key names needed to sign the transaction')
    parser_transfer.set_defaults(handler=run_transfer)

    return parser, parser.parse_args()


def run_add(args):
    address_book = AddressBook()
    address_book.add(args.name, args.address)


def run_transfer(args):
    address_book = AddressBook()
    key_store = KeyStore()

    # choose the destination
    if args.destination in address_book.keys():
        destination = address_book.lookup_address(args.destination)
    else:
        destination = key_store.lookup_address(args.destination)
        if destination is None:
            destination = Address(args.destination)

    # change the amount
    amount = args.amount * 10000000000

    # check all the signers make sense
    for signer in args.signers:
        if signer not in key_store.list_keys():
            raise RuntimeError('Unknown key: {}'.format(signer))

    # determine the from account
    from_address_name = None
    if len(args.signers) == 1 and args.from_address is None:
        from_address_name = args.signers[0]
    elif len(args.signers) >= 1 and args.from_address is not None:
        present = args.from_address in key_store.list_keys() or args.from_address in address_book.keys()
        from_address_name = args.from_address
        if not present:
            raise RuntimeError('Unknown from address: {}'.format(args.from_address))
    else:
        raise RuntimeError('Unable to determine from account')

    print('Network....:', args.network)
    print('From.......:', str(from_address_name))
    print('Signers....:', args.signers)
    print('Destination:', str(destination))
    print('Amount.....:', args.amount, 'FET')
    print()
    input('Press enter to continue')

    api = create_api(args.network)

    # start unsealing the private keys
    entities = {}
    for signer in args.signers:
        entity = key_store.load_key(signer, getpass.getpass('Enter password for key {}: '.format(signer)))
        entities[signer] = entity

    from_address = None
    if from_address_name in entities:
        from_address = Address(entities[from_address_name])
    elif from_address_name in address_book.keys():
        from_address = Address(address_book.lookup_address(from_address_name))

    # build up the basic transaction information
    tx = api.tokens._create_skeleton_tx(len(entities.values()))
    tx.from_address = Address(from_address)
    tx.add_transfer(destination, amount)
    for entity in entities.values():
        tx.add_signer(entity)

    # encode and sign the transaction
    encoded_tx = encode_transaction(tx, list(entities.values()))

    # # submit the transaction
    print('Submitting TX...')
    api.sync(api.tokens._post_tx_json(encoded_tx, 'transfer'))
    print('Submitting TX...complete')


def main():

    # disclaimer
    if not os.path.join(KeyStore.KEY_STORE_ROOT):
        print(DISCLAIMER)
        input('Press enter to accept')

    parser, args = parse_commandline()

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
            handler(args)

            exit_code = 0

        except NetworkUnavailableError:
            print('The network appears to be unavailable at the moment. Please try again later')

        except Exception as ex:
            print('Error:', ex)

    # close the program with the given exit code
    sys.exit(int(exit_code))


if __name__ == '__main__':
    main()
