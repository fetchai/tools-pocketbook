def run_add(args):
    from pocketbook.address_book import AddressBook

    address_book = AddressBook()
    address_book.add(args.name, args.address)
