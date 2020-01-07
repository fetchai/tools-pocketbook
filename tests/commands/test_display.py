import unittest
from unittest.mock import patch, Mock
from io import StringIO

from pocketbook.key_store import KeyStore

from tests.utils import SUPER_SECURE_PASSWORD

from fetchai.ledger.crypto import Entity, Address

class DisplayCommandTests(unittest.TestCase):

    @patch('getpass.getpass', return_value=SUPER_SECURE_PASSWORD)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_empty_list(self, MockKeyStore, output, *args):
        entity = Entity()
        address = Address(entity)

        key_store = MockKeyStore()
        key_store.load_key.return_value = entity

        args = Mock()
        args.name = 'foo-bar'

        # run the command
        from pocketbook.commands.display import run_display
        run_display(args)

        key_store.load_key.assert_called_once_with('foo-bar', SUPER_SECURE_PASSWORD)

        self.assertIn(entity.public_key, output.getvalue())
        self.assertIn(str(address), output.getvalue())