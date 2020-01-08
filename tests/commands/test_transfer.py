import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock

from fetchai.ledger.crypto import Entity, Address
from fetchai.ledger.serialisation.transaction import encode_transaction

from pocketbook.address_book import AddressBook
from pocketbook.key_store import KeyStore
from pocketbook.utils import create_api


class Person:
    def __init__(self, name):
        self.name = str(name)
        self.entity = Entity()
        self.address = Address(self.entity)


class TransferCommandUnitTests(unittest.TestCase):

    @patch('getpass.getpass', side_effect=['weak-password'])
    @patch('builtins.input', return_value='')
    @patch('fetchai.ledger.serialisation.transaction.encode_transaction', spec=encode_transaction)
    @patch('pocketbook.utils.create_api', spec=create_api)
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_transfer_to_addr_dest(self, MockKeyStore, MockAddressBook, mock_create_api, mock_encode_transaction,
                                   *args):
        person1 = Person('Jane')
        person2 = Person('Clare')

        key_store = MockKeyStore()
        key_store.list_keys.return_value = [person1.name]
        key_store.load_key.return_value = person1.entity

        address_book = MockAddressBook()
        address_book.keys.return_value = [person2.name]
        address_book.lookup_address.return_value = person2.address

        api = MagicMock()
        mock_create_api.return_value = api

        tx = MagicMock()
        tx.charge_rate = PropertyMock()
        api.tokens._create_skeleton_tx.return_value = tx
        api.tokens._post_tx_json.return_value = '0xTransactionHexId'

        encoded_tx = MagicMock()
        mock_encode_transaction.return_value = encoded_tx

        args = Mock()
        args.destination = person2.name
        args.amount = 20000000000
        args.charge_rate = 1
        args.signers = [person1.name]
        args.from_address = None
        args.network = 'super-duper-net'

        from pocketbook.commands.transfer import run_transfer
        run_transfer(args)

        mock_create_api.assert_called_once_with('super-duper-net')
        key_store.load_key.assert_called_once_with(person1.name, 'weak-password')
        api.tokens._create_skeleton_tx.assert_called_once_with(1)  # single signature
        tx.add_transfer.assert_called_once_with(person2.address, 20000000000)
        mock_encode_transaction.assert_called_once_with(tx, [person1.entity])
        api.tokens._post_tx_json.assert_called_once_with(encoded_tx, 'transfer')
        api.sync.assert_called_once_with('0xTransactionHexId')

    @patch('getpass.getpass', side_effect=['weak-password'])
    @patch('builtins.input', return_value='')
    @patch('fetchai.ledger.serialisation.transaction.encode_transaction', spec=encode_transaction)
    @patch('pocketbook.utils.create_api', spec=create_api)
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_transfer_to_key_dest(self, MockKeyStore, MockAddressBook, mock_create_api, mock_encode_transaction, *args):
        person1 = Person('Jane')
        person2 = Person('Clare')

        key_store = MockKeyStore()
        key_store.list_keys.return_value = [person1.name, person2.name]
        key_store.load_key.side_effect = [person1.entity, person2.entity]
        key_store.lookup_address.return_value = person2.address

        address_book = MockAddressBook()
        address_book.keys.return_value = []

        api = MagicMock()
        mock_create_api.return_value = api

        tx = MagicMock()
        api.tokens._create_skeleton_tx.return_value = tx
        api.tokens._post_tx_json.return_value = '0xTransactionHexId'

        encoded_tx = MagicMock()
        mock_encode_transaction.return_value = encoded_tx

        args = Mock()
        args.destination = person2.name
        args.amount = 20000000000
        args.charge_rate = 1
        args.signers = [person1.name]
        args.from_address = None
        args.network = 'super-duper-net'

        from pocketbook.commands.transfer import run_transfer
        run_transfer(args)

    @patch('getpass.getpass', side_effect=['weak-password'])
    @patch('builtins.input', return_value='')
    @patch('fetchai.ledger.serialisation.transaction.encode_transaction', spec=encode_transaction)
    @patch('pocketbook.utils.create_api', spec=create_api)
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_transfer_to_new_dest(self, MockKeyStore, MockAddressBook, mock_create_api, mock_encode_transaction, *args):
        person1 = Person('Jane')
        person2 = Person('Clare')

        key_store = MockKeyStore()
        key_store.list_keys.return_value = [person1.name, person2.name]
        key_store.load_key.side_effect = [person1.entity]
        key_store.lookup_address.return_value = None

        address_book = MockAddressBook()
        address_book.keys.return_value = []

        api = MagicMock()
        mock_create_api.return_value = api

        tx = MagicMock()
        api.tokens._create_skeleton_tx.return_value = tx
        api.tokens._post_tx_json.return_value = '0xTransactionHexId'

        encoded_tx = MagicMock()
        mock_encode_transaction.return_value = encoded_tx

        args = Mock()
        args.destination = str(person2.address)
        args.amount = 20000000000
        args.charge_rate = 1
        args.signers = [person1.name]
        args.from_address = None
        args.network = 'super-duper-net'

        from pocketbook.commands.transfer import run_transfer
        run_transfer(args)

        mock_create_api.assert_called_once_with('super-duper-net')
        key_store.load_key.assert_called_once_with(person1.name, 'weak-password')
        api.tokens._create_skeleton_tx.assert_called_once_with(1)  # single signature
        tx.add_transfer.assert_called_once_with(person2.address, 20000000000)
        mock_encode_transaction.assert_called_once_with(tx, [person1.entity])
        api.tokens._post_tx_json.assert_called_once_with(encoded_tx, 'transfer')
        api.sync.assert_called_once_with('0xTransactionHexId')

    @patch('getpass.getpass', side_effect=['weak-password'])
    @patch('builtins.input', return_value='')
    @patch('fetchai.ledger.serialisation.transaction.encode_transaction', spec=encode_transaction)
    @patch('pocketbook.utils.create_api', spec=create_api)
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_multisig_transfer(self, MockKeyStore, MockAddressBook, mock_create_api, mock_encode_transaction, *args):
        multisig = Person('MultiSig')
        person1 = Person('Jane')
        person2 = Person('Clare')

        key_store = MockKeyStore()
        key_store.list_keys.return_value = [person1.name, person2.name]
        key_store.load_key.side_effect = [person1.entity]
        key_store.lookup_address.return_value = person2.address

        address_book = MockAddressBook()
        address_book.keys.return_value = [multisig.name]
        address_book.lookup_address.return_value = multisig.address

        api = MagicMock()
        mock_create_api.return_value = api

        tx = MagicMock()
        api.tokens._create_skeleton_tx.return_value = tx
        api.tokens._post_tx_json.return_value = '0xTransactionHexId'

        encoded_tx = MagicMock()
        mock_encode_transaction.return_value = encoded_tx

        args = Mock()
        args.destination = person2.name
        args.amount = 20000000000
        args.charge_rate = 1
        args.signers = [person1.name]
        args.from_address = multisig.name
        args.network = 'super-duper-net'

        from pocketbook.commands.transfer import run_transfer
        run_transfer(args)

        mock_create_api.assert_called_once_with('super-duper-net')
        address_book.lookup_address.assert_called_once_with(multisig.name)
        key_store.lookup_address.assert_called_once_with(person2.name)
        key_store.load_key.assert_called_once_with(person1.name, 'weak-password')
        api.tokens._create_skeleton_tx.assert_called_once_with(1)  # single signature
        tx.add_transfer.assert_called_once_with(person2.address, 20000000000)
        mock_encode_transaction.assert_called_once_with(tx, [person1.entity])
        api.tokens._post_tx_json.assert_called_once_with(encoded_tx, 'transfer')
        api.sync.assert_called_once_with('0xTransactionHexId')

    @patch('getpass.getpass', side_effect=['weak-password'])
    @patch('builtins.input', return_value='')
    @patch('fetchai.ledger.serialisation.transaction.encode_transaction', spec=encode_transaction)
    @patch('pocketbook.utils.create_api', spec=create_api)
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_error_when_signer_not_present(self, MockKeyStore, MockAddressBook, mock_create_api,
                                           mock_encode_transaction, *args):
        person1 = Person('Jane')
        person2 = Person('Clare')

        key_store = MockKeyStore()
        key_store.list_keys.return_value = []
        key_store.load_key.side_effect = [person1.entity]
        key_store.lookup_address.return_value = person2.address

        address_book = MockAddressBook()
        address_book.keys.return_value = [person1.name, person2.name]
        address_book.lookup_address.return_value = person2.address

        args = Mock()
        args.destination = person2.name
        args.amount = 20000000000
        args.charge_rate = 1
        args.signers = [person1.name]
        args.from_address = person2.name
        args.network = 'super-duper-net'

        with self.assertRaises(RuntimeError):
            from pocketbook.commands.transfer import run_transfer
            run_transfer(args)

        # mock_create_api.assert_called_once_with('super-duper-net')
        address_book.lookup_address.assert_called_once_with(person2.name)

    @patch('getpass.getpass', side_effect=['weak-password'])
    @patch('builtins.input', return_value='')
    @patch('fetchai.ledger.serialisation.transaction.encode_transaction', spec=encode_transaction)
    @patch('pocketbook.utils.create_api', spec=create_api)
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_error_when_from_field_is_invalid(self, MockKeyStore, MockAddressBook, mock_create_api,
                                              mock_encode_transaction, *args):
        person1 = Person('Jane')
        person2 = Person('Clare')

        key_store = MockKeyStore()
        key_store.list_keys.return_value = [person1.name]
        key_store.load_key.side_effect = [person1.entity]
        key_store.lookup_address.return_value = person2.address

        address_book = MockAddressBook()
        address_book.keys.return_value = [person2.name]
        address_book.lookup_address.return_value = person2.address

        args = Mock()
        args.destination = person2.name
        args.amount = 20000000000
        args.charge_rate = 1
        args.signers = [person1.name]
        args.from_address = 'some-one-missing'
        args.network = 'super-duper-net'

        with self.assertRaises(RuntimeError):
            from pocketbook.commands.transfer import run_transfer
            run_transfer(args)

        # mock_create_api.assert_called_once_with('super-duper-net')
        address_book.lookup_address.assert_called_once_with(person2.name)

    @patch('getpass.getpass', side_effect=['weak-password'])
    @patch('builtins.input', return_value='')
    @patch('fetchai.ledger.serialisation.transaction.encode_transaction', spec=encode_transaction)
    @patch('pocketbook.utils.create_api', spec=create_api)
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_error_case_with_bad_args(self, MockKeyStore, MockAddressBook, mock_create_api, mock_encode_transaction,
                                      *args):
        person1 = Person('Jane')
        person2 = Person('Clare')

        key_store = MockKeyStore()
        key_store.list_keys.return_value = [person1.name]
        key_store.load_key.side_effect = [person1.entity]
        key_store.lookup_address.return_value = person2.address

        address_book = MockAddressBook()
        address_book.keys.return_value = [person2.name]
        address_book.lookup_address.return_value = person2.address

        args = Mock()
        args.destination = person2.name
        args.amount = 20000000000
        args.charge_rate = 1
        args.signers = []
        args.from_address = 'some-one-missing'
        args.network = 'super-duper-net'

        with self.assertRaises(RuntimeError):
            from pocketbook.commands.transfer import run_transfer
            run_transfer(args)

        # mock_create_api.assert_called_once_with('super-duper-net')
        address_book.lookup_address.assert_called_once_with(person2.name)
