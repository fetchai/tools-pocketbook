def run_import(args):
    from fetchai.ledger.crypto import Entity, Address
    from fetchai.ledger.crypto.entity import _strong_password as is_strong_password
    from pocketbook.key_store import KeyStore
    import getpass

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
        key_str = getpass.getpass('Enter private key (hex of b64 encoded)...: ')

        try:
            e = Entity.from_hex(key_str)
        except:
            try:
                e = Entity.from_base64(key_str)
            except:
                print('Given key is not ecdsa secp256k1 priv key encoded as either hex or base64!')
                continue

        print('\nAssociated address: {}'.format(Address(e)))
        print('Associated public key [hex]: {}'.format(e.public_key_hex))
        print('Associated public key [b64]: {}'.format(e.public_key))
        confirm = input('\nIs above correct? [y/N]: ')
        if confirm.lower() != 'y':
            print("\n=====================================\n")
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

    key_store.add_key(name, password, e)
