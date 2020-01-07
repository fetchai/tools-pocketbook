from pocketbook.address_book import AddressBook
from pocketbook.key_store import KeyStore
from pocketbook.table import Table
from pocketbook.utils import create_api, get_balance, get_stake


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
