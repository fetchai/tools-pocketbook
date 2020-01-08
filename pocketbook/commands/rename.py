def run_rename(args):
    from pocketbook.address_book import AddressBook
    from pocketbook.key_store import KeyStore

    address_book = AddressBook()
    key_store = KeyStore()

    # make sure that the new name is not present either as a key, or as an address
    new_present = args.new in address_book.keys() or args.new in key_store.list_keys()
    if new_present:
        print('{} is already present, please choose a different destination name'.format(args.new))
        return 1

    # check the old address or key name
    old_is_address = args.old in address_book.keys()
    old_is_key = args.old in key_store.list_keys()

    success = False
    if old_is_address and old_is_key:
        raise RuntimeError('Data store corrupting, key looks like an address + key')
    elif old_is_address:
        success = address_book.rename(args.old, args.new)
    elif old_is_key:
        success = key_store.rename_key(args.old, args.new)
    else:
        print('{} doesn\'t appear to be a valid key or address name, please check and try again'.format(args.old))
        return 1

    if not success:
        print('Failed to rename {} to {}'.format(args.old, args.new))
        return 1

    return 0
