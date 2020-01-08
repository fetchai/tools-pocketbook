import unittest
from unittest.mock import patch, Mock


class AddCommandTests(unittest.TestCase):

    @patch('pocketbook.address_book.AddressBook')
    def test_add(self, address_book):
        from pocketbook.commands.add import run_add

        args = Mock()
        args.name = 'foo'
        args.address = 'foo-address'

        run_add(args)

        instance = address_book.return_value
        instance.add.assert_called_once_with('foo', 'foo-address')
