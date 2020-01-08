import os

import toml
from fetchai.ledger.crypto import Entity, Address

from .constants import DEFAULT_KEY_STORE_ROOT


class KeyStoreError(Exception):
    pass


class DuplicateKeyNameError(KeyStoreError):
    def __str__(self):
        return 'Duplicate key name found'


class KeyNotFoundError(KeyStoreError):
    def __str__(self):
        return 'Unable to find key in store'


class UnableToDecodeKeyError(KeyStoreError):
    def __str__(self):
        return 'Unable to decode key from key store'


class KeyStore:
    INDEX_FILE_NAME = 'index.toml'

    def __init__(self, root=None):
        self._root = root or DEFAULT_KEY_STORE_ROOT
        self._index_path = os.path.join(self._root, self.INDEX_FILE_NAME)

        os.makedirs(self._root, exist_ok=True)

        if os.path.exists(self._index_path):
            with open(self._index_path, 'r') as index_file:
                self._index = toml.load(index_file)
        else:
            self._index = {'key': []}

    def list_keys(self):
        return list([item['name'] for item in self._index['key']])

    def lookup_address(self, name):
        address = None
        for item in self._index['key']:
            if item['name'] == name:
                address = item['address']
                break
        return address

    def load_key(self, name: str, password: str) -> Entity:
        if name not in self.list_keys():
            raise KeyNotFoundError()

        key_file_path = self._format_key_path(name)
        assert os.path.exists(key_file_path)

        with open(key_file_path, 'r') as key_file:
            entity = Entity.load(key_file, password)
            address = Address(entity)

            # lookup the metadata for this
            metadata = self._lookup_meta_data(name)
            if metadata['address'] != str(address):
                raise UnableToDecodeKeyError()

            return entity

    def add_key(self, name: str, password: str, entity: Entity):
        if name in self.list_keys():
            raise DuplicateKeyNameError()

        key_file_path = self._format_key_path(name)
        assert not os.path.exists(key_file_path)

        # dump out the file
        with open(key_file_path, 'w') as key_file:
            entity.dump(key_file, password)

        # update the index
        self._index['key'].append({
            'name': name,
            'address': str(Address(entity)),
        })
        self._flush_index()

    def _format_key_path(self, name: str):
        return os.path.join(self._root, '{}.key'.format(name))

    def _lookup_meta_data(self, name: str):
        for item in self._index['key']:
            if item['name'] == name:
                return item

    def _flush_index(self):
        with open(self._index_path, 'w') as index_file:
            toml.dump(self._index, index_file)
