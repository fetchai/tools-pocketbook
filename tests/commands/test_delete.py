import unittest
from unittest.mock import patch, Mock

from pocketbook.address_book import AddressBook
from pocketbook.key_store import KeyStore
from tests.utils import SAMPLE_ADDRESS


class DeleteCommandTests(unittest.TestCase):

    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_delete_address(self, MockKeyStore, MockAddressBook):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = []

        address_book = MockAddressBook()
        address_book.keys.return_value = ['foo']

        args = Mock()
        args.name = 'foo'

        from pocketbook.commands.delete import run_delete
        self.assertEqual(0, run_delete(args))

        address_book.remove.assert_called_once_with('foo')

    @patch('builtins.input', return_value='foo-address')
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_delete_key(self, MockKeyStore, MockAddressBook, *args):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = ['foo']
        key_store.lookup_address.return_value = 'foo-address'

        address_book = MockAddressBook()
        address_book.keys.return_value = []

        args = Mock()
        args.name = 'foo'

        from pocketbook.commands.delete import run_delete
        self.assertEqual(0, run_delete(args))

        key_store.lookup_address.assert_called_once_with('foo')
        key_store.remove_key.assert_called_once_with('foo')

    @patch('builtins.input', return_value='foo-address')
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_delete_unknown(self, MockKeyStore, MockAddressBook, *args):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = []

        address_book = MockAddressBook()
        address_book.keys.return_value = []

        args = Mock()
        args.name = 'foo'

        from pocketbook.commands.delete import run_delete
        self.assertEqual(1, run_delete(args))

    @patch('builtins.input', return_value='not-sample-address')
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_delete_key_invalid_confirmation(self, MockKeyStore, MockAddressBook, *args):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = ['foo']
        key_store.lookup_address.return_value = SAMPLE_ADDRESS

        address_book = MockAddressBook()
        address_book.keys.return_value = []

        args = Mock()
        args.name = 'foo'

        from pocketbook.commands.delete import run_delete
        self.assertEqual(1, run_delete(args))

        key_store.lookup_address.assert_called_once_with('foo')

    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_delete_address_failed(self, MockKeyStore, MockAddressBook):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = []

        address_book = MockAddressBook()
        address_book.keys.return_value = ['foo']
        address_book.remove.return_value = False

        args = Mock()
        args.name = 'foo'

        from pocketbook.commands.delete import run_delete
        self.assertEqual(1, run_delete(args))

        address_book.remove.assert_called_once_with('foo')

    @patch('builtins.input', return_value='foo-address')
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_delete_key_failed(self, MockKeyStore, MockAddressBook, *args):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = ['foo']
        key_store.lookup_address.return_value = 'foo-address'
        key_store.remove_key.return_value = False

        address_book = MockAddressBook()
        address_book.keys.return_value = []

        args = Mock()
        args.name = 'foo'

        from pocketbook.commands.delete import run_delete
        self.assertEqual(1, run_delete(args))

        key_store.lookup_address.assert_called_once_with('foo')
        key_store.remove_key.assert_called_once_with('foo')

    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_db_corruption(self, MockKeyStore, MockAddressBook):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = ['foo']

        address_book = MockAddressBook()
        address_book.keys.return_value = ['foo']

        args = Mock()
        args.name = 'foo'

        from pocketbook.commands.delete import run_delete
        with self.assertRaises(RuntimeError):
            run_delete(args)
