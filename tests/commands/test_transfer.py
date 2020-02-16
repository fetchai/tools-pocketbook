import unittest
from unittest.mock import patch, Mock, MagicMock

from fetchai.ledger.api.token import TokenTxFactory
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
    @patch('pocketbook.utils.create_api', spec=create_api)
    @patch('fetchai.ledger.api.token.TokenTxFactory', spec=TokenTxFactory)
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_transfer_to_addr_dest(self, MockKeyStore, MockAddressBook, MockTxFactory, mock_create_api, *args):
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
        api.submit_signed_tx.side_effect = ['0xTransactionHexId']

        # setup tx and tx factory
        tx = MagicMock()
        MockTxFactory.transfer.side_effect = [tx]

        args = Mock()
        args.destination = person2.name
        args.amount = 20000000000
        args.charge_rate = 1
        args.signers = [person1.name]
        args.from_address = None
        args.network = 'super-duper-net'

        from pocketbook.commands.transfer import run_transfer
        run_transfer(args)

        # create api and lookup the addresses from the key store and address book
        mock_create_api.assert_called_once_with('super-duper-net')
        key_store.load_key.assert_called_once_with(person1.name, 'weak-password')

        # expectations for configuring the transaction
        MockTxFactory.transfer.assert_called_once_with(Address(person1.address), person2.address, 20000000000, 0,
                                                       [person1.entity])
        self.assertEqual(tx.charge_rate, 1)
        self.assertEqual(tx.charge_limit, 1)
        api.set_validity_period.assert_called_once_with(tx)
        tx.sign.assert_called_with(person1.entity)

        # submission of the transaction
        api.submit_signed_tx.assert_called_once_with(tx)
        api.sync.assert_called_once_with('0xTransactionHexId')

    @patch('getpass.getpass', side_effect=['weak-password'])
    @patch('builtins.input', return_value='')
    @patch('pocketbook.utils.create_api', spec=create_api)
    @patch('fetchai.ledger.api.token.TokenTxFactory', spec=TokenTxFactory)
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_transfer_to_key_dest(self, MockKeyStore, MockAddressBook, MockTxFactory, mock_create_api, *args):
        person1 = Person('Jane')
        person2 = Person('Clare')

        key_store = MockKeyStore()
        key_store.list_keys.side_effect = [[person1.name, person2.name]]
        key_store.load_key.side_effect = [person1.entity, person2.entity]
        key_store.lookup_address.side_effect = [person2.address]

        address_book = MockAddressBook()
        address_book.keys.return_value = []

        api = MagicMock()
        mock_create_api.return_value = api
        api.submit_signed_tx.side_effect = ['0xTransactionHexId']

        # setup tx and tx factory
        tx = MagicMock()
        MockTxFactory.transfer.side_effect = [tx]

        args = Mock()
        args.destination = person2.name
        args.amount = 20000000000
        args.charge_rate = 2
        args.signers = [person1.name]
        args.from_address = None
        args.network = 'super-duper-net'

        from pocketbook.commands.transfer import run_transfer
        run_transfer(args)

        # create api and lookup the addresses from the key store and address book
        mock_create_api.assert_called_once_with('super-duper-net')
        key_store.lookup_address.assert_called_once_with(person2.name)
        key_store.load_key.assert_called_once_with(person1.name, 'weak-password')

        # expectations for configuring the transaction
        MockTxFactory.transfer.assert_called_once_with(person1.address, person2.address, 20000000000, 0,
                                                       [person1.entity])
        self.assertEqual(tx.charge_rate, 2)
        self.assertEqual(tx.charge_limit, 1)
        api.set_validity_period.assert_called_once_with(tx)
        tx.sign.assert_called_with(person1.entity)

        # submission of the transaction
        api.submit_signed_tx.assert_called_once_with(tx)
        api.sync.assert_called_once_with('0xTransactionHexId')

    @patch('getpass.getpass', side_effect=['weak-password'])
    @patch('builtins.input', return_value='')
    @patch('pocketbook.utils.create_api', spec=create_api)
    @patch('fetchai.ledger.api.token.TokenTxFactory', spec=TokenTxFactory)
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_transfer_to_new_dest(self, MockKeyStore, MockAddressBook, MockTxFactory, mock_create_api, *args):
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
        api.submit_signed_tx.side_effect = ['0xTransactionHexId']

        # setup tx and tx factory
        tx = MagicMock()
        MockTxFactory.transfer.side_effect = [tx]

        args = Mock()
        args.destination = str(person2.address)
        args.amount = 20000000000
        args.charge_rate = 1
        args.signers = [person1.name]
        args.from_address = None
        args.network = 'super-duper-net'

        from pocketbook.commands.transfer import run_transfer
        run_transfer(args)

        # create api and lookup the addresses from the key store and address book
        mock_create_api.assert_called_once_with('super-duper-net')
        key_store.load_key.assert_called_once_with(person1.name, 'weak-password')

        # expectations for configuring the transaction
        MockTxFactory.transfer.assert_called_once_with(Address(person1.address), person2.address, 20000000000, 0,
                                                       [person1.entity])
        self.assertEqual(tx.charge_rate, 1)
        self.assertEqual(tx.charge_limit, 1)
        api.set_validity_period.assert_called_once_with(tx)
        tx.sign.assert_called_with(person1.entity)

        # submission of the transaction
        api.submit_signed_tx.assert_called_once_with(tx)
        api.sync.assert_called_once_with('0xTransactionHexId')

    @patch('getpass.getpass', side_effect=['weak-password'])
    @patch('builtins.input', return_value='')
    @patch('pocketbook.utils.create_api', spec=create_api)
    @patch('fetchai.ledger.api.token.TokenTxFactory', spec=TokenTxFactory)
    @patch('pocketbook.address_book.AddressBook', spec=AddressBook)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_multisig_transfer(self, MockKeyStore, MockAddressBook, MockTxFactory, mock_create_api, *args):
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
        api.submit_signed_tx.side_effect = ['0xTransactionHexId']

        # setup tx and tx factory
        tx = MagicMock()
        MockTxFactory.transfer.side_effect = [tx]

        args = Mock()
        args.destination = person2.name
        args.amount = 20000000000
        args.charge_rate = 1
        args.signers = [person1.name]
        args.from_address = multisig.name
        args.network = 'super-duper-net'

        from pocketbook.commands.transfer import run_transfer
        run_transfer(args)

        # create api and lookup the addresses from the key store and address book
        mock_create_api.assert_called_once_with('super-duper-net')
        address_book.lookup_address.assert_called_once_with(multisig.name)
        key_store.lookup_address.assert_called_once_with(person2.name)
        key_store.load_key.assert_called_once_with(person1.name, 'weak-password')

        # expectations for configuring the transaction
        MockTxFactory.transfer.assert_called_once_with(Address(multisig.address), person2.address, 20000000000, 0,
                                                       [person1.entity])
        self.assertEqual(tx.charge_rate, 1)
        self.assertEqual(tx.charge_limit, 1)
        api.set_validity_period.assert_called_once_with(tx)
        tx.sign.assert_called_with(person1.entity)

        # submission of the transaction
        api.submit_signed_tx.assert_called_once_with(tx)
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
