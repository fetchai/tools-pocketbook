import unittest
from unittest.mock import patch, Mock

from pocketbook.address_book import AddressBook
from pocketbook.key_store import KeyStore


class RenameCommandTests(unittest.TestCase):

    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_normal_key_rename(self, MockKeyStore, MockAddressBook):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = ['old-name']

        address_book = MockAddressBook()
        address_book.keys.return_value = []

        args = Mock()
        args.old = 'old-name'
        args.new = 'new-name'

        from pocketbook.commands.rename import run_rename
        self.assertEqual(run_rename(args), 0)

        key_store.rename_key.assert_called_once_with('old-name', 'new-name')

    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_normal_address_rename(self, MockKeyStore, MockAddressBook):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = []

        address_book = MockAddressBook()
        address_book.keys.return_value = ['old-name']

        args = Mock()
        args.old = 'old-name'
        args.new = 'new-name'

        from pocketbook.commands.rename import run_rename
        self.assertEqual(run_rename(args), 0)

        address_book.rename.assert_called_once_with('old-name', 'new-name')

    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_doesnt_exits(self, MockKeyStore, MockAddressBook):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = []

        address_book = MockAddressBook()
        address_book.keys.return_value = []

        args = Mock()
        args.old = 'old-name'
        args.new = 'new-name'

        from pocketbook.commands.rename import run_rename
        self.assertEqual(run_rename(args), 1)

    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_duplicate_destination_key_name(self, MockKeyStore, MockAddressBook):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = ['new-name']

        address_book = MockAddressBook()
        address_book.keys.return_value = []

        args = Mock()
        args.old = 'old-name'
        args.new = 'new-name'

        from pocketbook.commands.rename import run_rename
        self.assertEqual(run_rename(args), 1)

    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_duplicate_destination_address_name(self, MockKeyStore, MockAddressBook):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = []

        address_book = MockAddressBook()
        address_book.keys.return_value = ['new-name']

        args = Mock()
        args.old = 'old-name'
        args.new = 'new-name'

        from pocketbook.commands.rename import run_rename
        self.assertEqual(run_rename(args), 1)

    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_corrupted_db_duplicate_address_key(self, MockKeyStore, MockAddressBook):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = ['old-name']

        address_book = MockAddressBook()
        address_book.keys.return_value = ['old-name']

        args = Mock()
        args.old = 'old-name'
        args.new = 'new-name'

        from pocketbook.commands.rename import run_rename
        with self.assertRaises(RuntimeError):
            run_rename(args)

    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_handle_address_rename_failure(self, MockKeyStore, MockAddressBook):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = []

        address_book = MockAddressBook()
        address_book.keys.return_value = ['old-name']
        address_book.rename.return_value = False

        args = Mock()
        args.old = 'old-name'
        args.new = 'new-name'

        from pocketbook.commands.rename import run_rename
        self.assertEqual(run_rename(args), 1)

        address_book.rename.assert_called_once_with('old-name', 'new-name')

    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_handle_key_rename_failure(self, MockKeyStore, MockAddressBook):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = ['old-name']
        key_store.rename_key.return_value = False

        address_book = MockAddressBook()
        address_book.keys.return_value = []

        args = Mock()
        args.old = 'old-name'
        args.new = 'new-name'

        from pocketbook.commands.rename import run_rename
        self.assertEqual(run_rename(args), 1)

        key_store.rename_key.assert_called_once_with('old-name', 'new-name')
