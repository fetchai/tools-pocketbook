import os
import unittest

import toml
from fetchai.ledger.crypto import Entity, Address

from pocketbook.key_store import KeyStore, DuplicateKeyNameError, KeyNotFoundError, UnableToDecodeKeyError
from .utils import TemporaryPocketBookRoot

SUPER_SECURE_PASSWORD = 'Fetch!Ai-ToTh3M00n!'


class AddressBookTests(unittest.TestCase):
    def assertFlushedToDisk(self, name: str, password: str, entity: Entity, ctx: TemporaryPocketBookRoot):
        self.assertTrue(os.path.isdir(ctx.root))

        # check that the index record has been created correctly
        index_path = os.path.join(ctx.root, KeyStore.INDEX_FILE_NAME)
        self.assertTrue(os.path.isfile(index_path))
        with open(index_path, 'r') as index_file:
            index = toml.load(index_path)

            # build up the key listings
            key_addresses = {key['name']: key['address'] for key in index.get('key', [])}

            # ensure the key is reference in the index
            self.assertIn(name, key_addresses.keys())

            # also ensure the computed address is also correct
            expected_address = Address(entity)
            self.assertEqual(key_addresses[name], str(expected_address))

        # check the contents of the key
        key_path = os.path.join(ctx.root, '{}.key'.format(name))
        self.assertTrue(os.path.isfile(key_path))
        with open(key_path, 'r') as key_file:
            recovered = Entity.load(key_file, password)
            self.assertEqual(recovered.private_key, entity.private_key)

    def test_init(self):
        with TemporaryPocketBookRoot() as ctx:
            key_store = KeyStore(root=ctx.root)
            self.assertEqual(len(key_store.list_keys()), 0)

    def test_add_key(self):
        with TemporaryPocketBookRoot() as ctx:
            key_store = KeyStore(root=ctx.root)

            # create an entity and add it to the store
            entity = Entity()
            key_store.add_key('sample', SUPER_SECURE_PASSWORD, entity)

            self.assertEqual(len(key_store.list_keys()), 1)

    def test_added_key_is_flushed_to_disk(self):
        with TemporaryPocketBookRoot() as ctx:
            key_store = KeyStore(root=ctx.root)

            # create an entity and add it to the store
            entity = Entity()
            key_store.add_key('sample', SUPER_SECURE_PASSWORD, entity)

            # check the files on have been set correctly
            self.assertFlushedToDisk('sample', SUPER_SECURE_PASSWORD, entity, ctx)

    def test_address_lookup(self):
        with TemporaryPocketBookRoot() as ctx:
            entity = Entity()
            key_store = KeyStore(root=ctx.root)
            key_store.add_key('sample', SUPER_SECURE_PASSWORD, entity)

            expected_address = Address(entity)
            recovered_address = key_store.lookup_address('sample')

            self.assertEqual(str(expected_address), str(recovered_address))

    def test_duplicate_adds(self):
        with TemporaryPocketBookRoot() as ctx:
            entity = Entity()
            key_store = KeyStore(root=ctx.root)
            key_store.add_key('sample', SUPER_SECURE_PASSWORD, entity)

            with self.assertRaises(DuplicateKeyNameError):
                key_store.add_key('sample', SUPER_SECURE_PASSWORD, entity)

    def test_loading_of_multiple_stores(self):
        with TemporaryPocketBookRoot() as ctx:
            entity = Entity()
            key_store1 = KeyStore(root=ctx.root)
            key_store1.add_key('sample', SUPER_SECURE_PASSWORD, entity)

            key_store2 = KeyStore(root=ctx.root)
            self.assertEqual(set(key_store2.list_keys()), set(key_store1.list_keys()))

    def test_loading_saved_key(self):
        with TemporaryPocketBookRoot() as ctx:
            entity = Entity()
            key_store = KeyStore(root=ctx.root)
            key_store.add_key('sample', SUPER_SECURE_PASSWORD, entity)

            recovered = key_store.load_key('sample', SUPER_SECURE_PASSWORD)
            self.assertEqual(recovered.private_key, entity.private_key)

    def test_loading_invalid_key(self):
        with TemporaryPocketBookRoot() as ctx:
            key_store = KeyStore(root=ctx.root)

            with self.assertRaises(KeyNotFoundError):
                key_store.load_key('foo-bar', SUPER_SECURE_PASSWORD)

    def test_unable_to_load_saved_key(self):
        with TemporaryPocketBookRoot() as ctx:
            entity = Entity()
            key_store = KeyStore(root=ctx.root)
            key_store.add_key('sample', SUPER_SECURE_PASSWORD, entity)

            with self.assertRaises(UnableToDecodeKeyError):
                key_store.load_key('sample', '!' + SUPER_SECURE_PASSWORD)

    def test_duplicate_key_error_message(self):
        error = DuplicateKeyNameError()
        self.assertEqual(str(error), 'Duplicate key name found')

    def test_key_not_found_error_message(self):
        error = KeyNotFoundError()
        self.assertEqual(str(error), 'Unable to find key in store')

    def test_unable_to_decode_key_error_message(self):
        error = UnableToDecodeKeyError()
        self.assertEqual(str(error), 'Unable to decode key from key store')