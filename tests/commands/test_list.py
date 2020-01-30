import unittest
from io import StringIO
from unittest.mock import patch, Mock, call

from pocketbook.address_book import AddressBook
from pocketbook.key_store import KeyStore
from pocketbook.table import Table
from pocketbook.utils import create_api, get_balance, get_stake, token_amount
from tests.utils import SAMPLE_ADDRESS


class ListCommandTests(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_empty_list(self, MockKeyStore, MockAddressBook, output, *args):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = []

        # run the command
        from pocketbook.commands.list import run_list
        run_list(None)

        self.assertIn('No keys present', output.getvalue())

    @patch('pocketbook.utils.get_stake', spec=get_stake)
    @patch('pocketbook.utils.get_balance', spec=get_balance)
    @patch('pocketbook.utils.create_api', spec=create_api)
    @patch('pocketbook.table.Table', spec=Table)
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_normal_display(self, MockKeyStore, MockAddressBook, MockTable, mock_create_api, mock_get_balance,
                            mock_get_stake, *args):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = ['sample']
        key_store.lookup_address.return_value = SAMPLE_ADDRESS

        address_book = MockAddressBook()
        address_book.items.return_value = [('other', 'another-address')]

        mock_get_balance.side_effect = [10, 5]
        mock_get_stake.side_effect = [5, 10]

        api = mock_create_api()
        mock_create_api.reset_mock()

        args = Mock()
        args.verbose = False
        args.network = 'bar-net'
        args.pattern = ['*']

        table = MockTable()
        MockTable.reset_mock()

        # run the command
        from pocketbook.commands.list import run_list
        run_list(args)

        MockTable.assert_called_once_with(['name', 'type', 'balance', 'stake'])
        mock_create_api.assert_called_once_with('bar-net')
        key_store.lookup_address.assert_called_once_with('sample')

        self.assertEqual(mock_get_balance.call_args_list, [call(api, SAMPLE_ADDRESS), call(api, 'another-address')])
        self.assertEqual(mock_get_stake.call_args_list, [call(api, SAMPLE_ADDRESS), call(api, 'another-address')])

        # check that we call the correct number of calls
        expected_row_calls = [
            call(name='sample', type='key', balance=token_amount(10), stake=token_amount(5), address=SAMPLE_ADDRESS),
            call(name='other', type='addr', balance=token_amount(5), stake=token_amount(10), address='another-address'),
        ]
        self.assertEqual(table.add_row.call_args_list, expected_row_calls)
        table.display.assert_called_once_with()

    @patch('pocketbook.utils.get_stake', spec=get_stake)
    @patch('pocketbook.utils.get_balance', spec=get_balance)
    @patch('pocketbook.utils.create_api', spec=create_api)
    @patch('pocketbook.table.Table', spec=Table)
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_verbose_display(self, MockKeyStore, MockAddressBook, MockTable, mock_create_api, mock_get_balance,
                             mock_get_stake, *args):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = ['sample']
        key_store.lookup_address.return_value = SAMPLE_ADDRESS

        address_book = MockAddressBook()
        address_book.items.return_value = [('other', 'another-address')]

        mock_get_balance.side_effect = [10, 5]
        mock_get_stake.side_effect = [5, 10]

        api = mock_create_api()
        mock_create_api.reset_mock()

        args = Mock()
        args.verbose = True
        args.network = 'bar-net'
        args.pattern = ['*']

        table = MockTable()
        MockTable.reset_mock()

        # run the command
        from pocketbook.commands.list import run_list
        run_list(args)

        MockTable.assert_called_once_with(['name', 'type', 'balance', 'stake', 'address'])
        mock_create_api.assert_called_once_with('bar-net')
        key_store.lookup_address.assert_called_once_with('sample')

        self.assertEqual(mock_get_balance.call_args_list, [call(api, SAMPLE_ADDRESS), call(api, 'another-address')])
        self.assertEqual(mock_get_stake.call_args_list, [call(api, SAMPLE_ADDRESS), call(api, 'another-address')])

        # check that we call the correct number of calls
        expected_row_calls = [
            call(name='sample', type='key', balance=token_amount(10), stake=token_amount(5), address=SAMPLE_ADDRESS),
            call(name='other', type='addr', balance=token_amount(5), stake=token_amount(10), address='another-address'),
        ]
        self.assertEqual(table.add_row.call_args_list, expected_row_calls)
        table.display.assert_called_once_with()


    @patch('pocketbook.utils.get_stake', spec=get_stake)
    @patch('pocketbook.utils.get_balance', spec=get_balance)
    @patch('pocketbook.utils.create_api', spec=create_api)
    @patch('pocketbook.table.Table', spec=Table)
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_normal_filtered_display(self, MockKeyStore, MockAddressBook, MockTable, mock_create_api, mock_get_balance,
                            mock_get_stake, *args):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = ['sample1', 'other1']
        key_store.lookup_address.return_value = SAMPLE_ADDRESS

        address_book = MockAddressBook()
        address_book.items.return_value = [('sample2', 'address1'), ('other2', 'address2')]

        mock_get_balance.side_effect = [10, 5]
        mock_get_stake.side_effect = [5, 10]

        api = mock_create_api()
        mock_create_api.reset_mock()

        args = Mock()
        args.verbose = False
        args.network = 'bar-net'
        args.pattern = ['sample*']

        table = MockTable()
        MockTable.reset_mock()

        # run the command
        from pocketbook.commands.list import run_list
        run_list(args)

        MockTable.assert_called_once_with(['name', 'type', 'balance', 'stake'])
        mock_create_api.assert_called_once_with('bar-net')
        key_store.lookup_address.assert_called_once_with('sample1')

        self.assertEqual(mock_get_balance.call_args_list, [call(api, SAMPLE_ADDRESS), call(api, 'address1')])
        self.assertEqual(mock_get_stake.call_args_list, [call(api, SAMPLE_ADDRESS), call(api, 'address1')])

        # check that we call the correct number of calls
        expected_row_calls = [
            call(name='sample1', type='key', balance=token_amount(10), stake=token_amount(5), address=SAMPLE_ADDRESS),
            call(name='sample2', type='addr', balance=token_amount(5), stake=token_amount(10), address='address1'),
        ]
        self.assertEqual(table.add_row.call_args_list, expected_row_calls)
        table.display.assert_called_once_with()