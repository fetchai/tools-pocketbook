
def run_display(args):
    from getpass import getpass
    from fetchai.ledger.crypto import Address
    from pocketbook.key_store import KeyStore

    key_store = KeyStore()

    entity = key_store.load_key(args.name, getpass('Enter password for key: '))
    address = Address(entity)

    print('Address....:', str(address))
    print('Public Key.:', str(entity.public_key))
