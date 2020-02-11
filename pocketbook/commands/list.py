from fnmatch import fnmatch
import warnings

def _should_display(item, patterns):
    return any([fnmatch(item, p) for p in patterns])


def run_list(args):
    from pocketbook.address_book import AddressBook
    from pocketbook.key_store import KeyStore
    from pocketbook.table import Table
    from pocketbook.utils import create_api, get_balance, get_stake, token_amount

    # the latest version of SDK will generate warning because we are using the staking API
    warnings.simplefilter('ignore')

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
            if not _should_display(key, args.pattern):
                continue

            address = key_store.lookup_address(key)
            balance = get_balance(api, address)
            stake = get_stake(api, address)

            row_data = {
                'name': key,
                'type': 'key',
                'balance': token_amount(balance),
                'stake': token_amount(stake),
                'address': str(address),
            }

            table.add_row(**row_data)

        for name, address in address_book.items():
            if not _should_display(name, args.pattern):
                continue

            balance = get_balance(api, address)
            stake = get_stake(api, address)

            row_data = {
                'name': name,
                'type': 'addr',
                'balance': token_amount(balance),
                'stake': token_amount(stake),
                'address': str(address),
            }

            table.add_row(**row_data)

        table.display()
