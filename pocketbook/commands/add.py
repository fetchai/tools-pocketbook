from pocketbook.address_book import AddressBook


def run_add(args):
    address_book = AddressBook()
    address_book.add(args.name, args.address)
