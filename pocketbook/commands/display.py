import getpass

from fetchai.ledger.crypto import Address

from pocketbook.key_store import KeyStore


def run_display(args):
    key_store = KeyStore()

    entity = key_store.load_key(args.name, getpass.getpass('Enter password for key: '))
    address = Address(entity)

    print('Address....:', str(address))
    print('Public Key.:', str(entity.public_key))
