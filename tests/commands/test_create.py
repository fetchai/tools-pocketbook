import unittest
from unittest.mock import patch
from io import StringIO

from tests.utils import SUPER_SECURE_PASSWORD

from fetchai.ledger.crypto import Entity
from pocketbook.key_store import KeyStore


class CreateCommandTests(unittest.TestCase):

    @patch('builtins.input', side_effect=['foo-bar'])
    @patch('getpass.getpass', side_effect=[SUPER_SECURE_PASSWORD, SUPER_SECURE_PASSWORD])
    @patch('fetchai.ledger.crypto.Entity', spec=Entity)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_simple_flow(self, MockKeyStore, MockEntity, *args):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = []
        entity = MockEntity()

        from pocketbook.commands.create import run_create
        run_create(None)

        key_store.add_key.assert_called_once_with('foo-bar', SUPER_SECURE_PASSWORD, entity)

    @patch('builtins.input', side_effect=['foo-bar'])
    @patch('getpass.getpass', side_effect=[SUPER_SECURE_PASSWORD, '', SUPER_SECURE_PASSWORD, SUPER_SECURE_PASSWORD])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('fetchai.ledger.crypto.Entity', spec=Entity)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_mismatching_passwords(self, MockKeyStore, MockEntity, output, *args):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = []
        entity = MockEntity()

        from pocketbook.commands.create import run_create
        run_create(None)

        key_store.add_key.assert_called_once_with('foo-bar', SUPER_SECURE_PASSWORD, entity)

        self.assertIn('Passwords did not match, try again', output.getvalue())

    @patch('builtins.input', side_effect=['foo-bar'])
    @patch('getpass.getpass', side_effect=['weak', SUPER_SECURE_PASSWORD, SUPER_SECURE_PASSWORD])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('fetchai.ledger.crypto.Entity', spec=Entity)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_weak_password(self, MockKeyStore, MockEntity, output, *args):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = []
        entity = MockEntity()

        from pocketbook.commands.create import run_create
        run_create(None)

        key_store.add_key.assert_called_once_with('foo-bar', SUPER_SECURE_PASSWORD, entity)

        self.assertIn('Password too simple, try again', output.getvalue())

    @patch('builtins.input', side_effect=['foo-bar', 'foo-baz'])
    @patch('getpass.getpass', side_effect=[SUPER_SECURE_PASSWORD, SUPER_SECURE_PASSWORD])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('fetchai.ledger.crypto.Entity', spec=Entity)
    @patch('pocketbook.key_store.KeyStore', spec=KeyStore)
    def test_re_prompt_for_duplicate_key(self, MockKeyStore, MockEntity, output, *args):
        key_store = MockKeyStore()
        key_store.list_keys.return_value = ['foo-bar']
        entity = MockEntity()

        from pocketbook.commands.create import run_create
        run_create(None)

        key_store.add_key.assert_called_once_with('foo-baz', SUPER_SECURE_PASSWORD, entity)

        self.assertIn('Key name already exists', output.getvalue())



