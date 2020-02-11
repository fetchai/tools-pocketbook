def run_create(args):
    from getpass import getpass
    from fetchai.ledger.crypto import Entity
    from pocketbook.key_store import KeyStore


    key_store = KeyStore()
    existing_keys = set(key_store.list_keys())

    # get the name for the new key
    while True:
        name = input('Enter name for key: ')
        if name in existing_keys:
            print('Key name already exists')
            continue
        break

    # prompt the user for the password
    while True:
        password = getpass('Enter password for key...: ')
        if not Entity.is_strong_password(password):
            print('Password too simple, try again')
            continue

        confirm = getpass('Confirm password for key.: ')
        if password != confirm:
            print('Passwords did not match, try again')
            continue

        break

    key_store.add_key(name, password, Entity())
