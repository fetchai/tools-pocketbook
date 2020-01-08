KEY_WARNING_TEMPLATE = """
### WARNING ###

You are about to delete the key {} from the database. This is a PERMANENT change and can
no be reverted. This might mean that you loose access to funds forever.

If you want to continue please confirm by entering the address of wallet you want to remove
below:

Address (Base58): """


def run_delete(args):
    from pocketbook.key_store import KeyStore
    from pocketbook.address_book import AddressBook

    key_store = KeyStore()
    address_book = AddressBook()

    is_key = args.name in key_store.list_keys()
    is_address = args.name in address_book.keys()

    def address_delete():
        return address_book.remove(args.name)

    def key_delete():
        return key_store.remove_key(args.name)

    if is_key and is_address:
        raise RuntimeError('Corrected database, account is both an address and a key')
    elif is_key:
        warning = True
        handler = key_delete
    elif is_address:
        warning = False
        handler = address_delete
    else:
        print('Unknown key or address: {}. Please check and try again'.format(args.name))
        return 1

    # double check that the user really want to remove the key
    if warning:
        input_address = input(KEY_WARNING_TEMPLATE.format(args.name))

        address = key_store.lookup_address(args.name)

        if str(address) != input_address:
            print('The input address for key {} does not match. Please double check and try again')
            return 1

    # perform the removal
    if not handler():
        print('Failed to remove the specified key or address')
        return 1

    return 0
