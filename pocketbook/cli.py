import argparse
import sys

from . import __version__
from .commands.add import run_add
from .commands.create import run_create
from .commands.delete import run_delete
from .commands.list import run_list
from .commands.rename import run_rename
from .commands.transfer import run_transfer
from .disclaimer import display_disclaimer
from .utils import NetworkUnavailableError, checked_address, to_canonical, MINIMUM_FRACTIONAL_FET


def parse_commandline():
    parser = argparse.ArgumentParser(prog='pocketbook')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('-n', '--network', default='mainnet', help='The name of the target being addressed')
    subparsers = parser.add_subparsers()

    parser_list = subparsers.add_parser('list', aliases=['ls'], help='Lists all the balances and addresses')
    parser_list.add_argument('-v', '--verbose', action='store_true', help='Display extra information (if available)')
    parser_list.add_argument('pattern', nargs='*', default=['*'])
    parser_list.set_defaults(handler=run_list)

    parser_create = subparsers.add_parser('create', aliases=['new'], help='Create a new key')
    parser_create.set_defaults(handler=run_create)

    parser_add = subparsers.add_parser('add', help='Adds an address to the address book')
    parser_add.add_argument('name', help='The name of the key')
    parser_add.add_argument('address', type=checked_address, help='The account address')
    parser_add.set_defaults(handler=run_add)

    parser_transfer = subparsers.add_parser('transfer', help='Transfers funds between wallets')
    parser_transfer.add_argument('destination',
                                 help='The destination address either a name in the address book or an address')
    parser_transfer.add_argument('amount', type=to_canonical, help='The amount of FET to be transferred')
    parser_transfer.add_argument('--from', dest='from_address', help='The signing account, required for multi-sig')
    parser_transfer.add_argument('-R', '--charge-rate', type=to_canonical, default=to_canonical(MINIMUM_FRACTIONAL_FET),
                                 help='The charge rate associated with this transaction')
    parser_transfer.add_argument('signers', nargs='+', help='The series of key names needed to sign the transaction')
    parser_transfer.set_defaults(handler=run_transfer)

    parser_rename = subparsers.add_parser('rename', aliases=['mv'], help='Renames and address or key to another name')
    parser_rename.add_argument('old', help='The name of the old account name')
    parser_rename.add_argument('new', help='The new name of the account')
    parser_rename.set_defaults(handler=run_rename)

    parser_delete = subparsers.add_parser('delete', aliases=['rm'], help='Deletes an address or key from the wallet')
    parser_delete.add_argument('name', help='The name of the account to remove')
    parser_delete.set_defaults(handler=run_delete)

    return parser, parser.parse_args()


def main():
    # run the specified command
    exit_code = 1
    try:
        display_disclaimer()

        # parse the command line
        parser, args = parse_commandline()

        # select the command handler
        if hasattr(args, 'handler'):
            handler = args.handler
        else:
            parser.print_usage()
            handler = None

        if handler is not None:
            # execute the handler
            ret = handler(args)

            # update the exit code based on the return value
            if isinstance(ret, int):
                exit_code = ret
            else:
                exit_code = 0

    except KeyboardInterrupt:
        print('Stopped!')

    except NetworkUnavailableError:
        print('The network appears to be unavailable at the moment. Please try again later')

    except Exception as ex:
        print('Error:', ex)

    # close the program with the given exit code
    sys.exit(int(exit_code))
