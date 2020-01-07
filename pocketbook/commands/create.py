import getpass

from fetchai.ledger.crypto import Entity
from fetchai.ledger.crypto.entity import _strong_password as is_strong_password

from pocketbook.key_store import KeyStore


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
