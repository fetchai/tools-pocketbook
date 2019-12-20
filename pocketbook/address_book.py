import os
import toml


class AddressBook:
    KEY_STORE_ROOT = os.path.abspath(os.path.expanduser('~/.pocketbook'))
    ADDRESS_BOOK_PATH = os.path.join(KEY_STORE_ROOT, 'addresses.toml')

    def __init__(self):
        self._address_book = self._load()

    def add(self, name, address):
        if name in self._address_book:
            raise RuntimeError('Address already exists')

        self._address_book[name] = str(address)
        self._save()

    def keys(self):
        return self._address_book.keys()

    def items(self):
        return self._address_book.items()

    def lookup_address(self, name):
        if name not in self._address_book:
            raise RuntimeError('Unable to lookup requested address: {}'.format(name))

        return self._address_book[name]

    def _save(self):
        with open(self.ADDRESS_BOOK_PATH, 'w') as output_file:
            toml.dump(self._address_book, output_file)

    @classmethod
    def _load(cls):
        if not os.path.exists(cls.ADDRESS_BOOK_PATH):
            return {}
        with open(cls.ADDRESS_BOOK_PATH, 'r') as input_file:
            return toml.load(input_file)
