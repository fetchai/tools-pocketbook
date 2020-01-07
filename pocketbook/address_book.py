import os

import toml

from .constants import DEFAULT_KEY_STORE_ROOT


class AddressBook:
    INDEX_FILE_NAME = 'addresses.toml'

    def __init__(self, root=None):
        self._root = root or DEFAULT_KEY_STORE_ROOT
        self._address_book_path = os.path.join(self._root, self.INDEX_FILE_NAME)
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
        with open(self._address_book_path, 'w') as output_file:
            toml.dump(self._address_book, output_file)

    def _load(self):
        if not os.path.exists(self._address_book_path):
            return {}
        with open(self._address_book_path, 'r') as input_file:
            return toml.load(input_file)
