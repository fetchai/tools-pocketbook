import os
import unittest

import toml

from pocketbook.address_book import AddressBook
from .utils import TemporaryPocketBookRoot, SAMPLE_ADDRESS


class AddressBookTests(unittest.TestCase):

    def assertAddressIsPresentOnDisk(self, name: str, address: str, ctx: TemporaryPocketBookRoot):
        address_index_path = os.path.join(ctx.root, AddressBook.INDEX_FILE_NAME)
        self.assertTrue(os.path.isfile(address_index_path))

        with open(address_index_path, 'r') as address_index_file:
            address_index = toml.load(address_index_file)

            self.assertIn(name, address_index)
            self.assertEqual(address_index[name], address)

    def test_no_writing_on_empty_folder(self):
        with TemporaryPocketBookRoot() as ctx:
            address_book = AddressBook(root=ctx.root)
            self.assertEqual(len(os.listdir(ctx.root)), 0)

    def test_simple_write(self):
        with TemporaryPocketBookRoot() as ctx:
            # add the sample address
            address_book = AddressBook(root=ctx.root)
            address_book.add('sample', SAMPLE_ADDRESS)

            self.assertAddressIsPresentOnDisk('sample', SAMPLE_ADDRESS, ctx)

    def test_check_keys_exists(self):
        with TemporaryPocketBookRoot() as ctx:
            address_book = AddressBook(root=ctx.root)
            address_book.add('sample', SAMPLE_ADDRESS)

            self.assertIn('sample', address_book.keys())
            self.assertNotIn('foo', address_book.keys())

    def test_get_items(self):
        with TemporaryPocketBookRoot() as ctx:
            address_book = AddressBook(root=ctx.root)
            address_book.add('sample', SAMPLE_ADDRESS)

            address_book_items = list(address_book.items())
            self.assertEqual(len(address_book_items), 1)
            self.assertEqual(address_book_items[0], ('sample', SAMPLE_ADDRESS))

    def test_lookup_of_address(self):
        with TemporaryPocketBookRoot() as ctx:
            address_book = AddressBook(root=ctx.root)
            address_book.add('sample', SAMPLE_ADDRESS)

            self.assertEqual(address_book.lookup_address('sample'), SAMPLE_ADDRESS)

    def test_invalid_lookup_of_address(self):
        with TemporaryPocketBookRoot() as ctx:
            address_book = AddressBook(root=ctx.root)
            with self.assertRaises(RuntimeError):
                address_book.lookup_address('foo-bar')

    def test_throw_on_duplicate_add(self):
        with TemporaryPocketBookRoot() as ctx:
            address_book = AddressBook(root=ctx.root)
            address_book.add('sample', SAMPLE_ADDRESS)

            with self.assertRaises(RuntimeError):
                address_book.add('sample', SAMPLE_ADDRESS)

    def test_load_of_addresses(self):
        with TemporaryPocketBookRoot() as ctx:
            address_book1 = AddressBook(root=ctx.root)
            address_book1.add('sample', SAMPLE_ADDRESS)

            address_book2 = AddressBook(root=ctx.root)
            self.assertEqual(set(address_book1.items()), set(address_book2.items()))
