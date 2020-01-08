import unittest
from unittest.mock import MagicMock, patch

from fetchai.ledger.crypto import Address, Entity

from pocketbook.utils import get_balance, get_stake, NetworkUnavailableError, checked_address


class UtilsTests(unittest.TestCase):

    def test_get_balance(self):
        api = MagicMock()
        api.tokens.balance.return_value = 100000000000

        balance = get_balance(api, 'some address')
        self.assertEqual(balance, 10)

        api.tokens.balance.assert_called_once_with('some address')

    def test_get_stake(self):
        api = MagicMock()
        api.tokens.stake.return_value = 50000000000

        stake = get_stake(api, 'some address')
        self.assertEqual(stake, 5)

        api.tokens.stake.assert_called_once_with('some address')

    @patch('fetchai.ledger.api.LedgerApi')
    def test_create_api(self, MockLedgerApi):
        # normal use
        from pocketbook.utils import create_api
        create_api('super-duper-net')

        MockLedgerApi.assert_called_once_with(network='super-duper-net')
        MockLedgerApi.reset_mock()

    @patch('fetchai.ledger.api.LedgerApi', side_effect=[RuntimeError('Bad Error')])
    def test_error_on_create_api(self, MockLedgerApi):
        # internal error case
        from pocketbook.utils import create_api
        with self.assertRaises(NetworkUnavailableError):
            create_api('super-duper-net')

        MockLedgerApi.assert_called_once_with(network='super-duper-net')

    def test_valid_address(self):
        entity = Entity()
        address = Address(entity)

        recovered_address = checked_address(str(address))

        self.assertEqual(str(recovered_address), str(address))

    def test_invalid_address_exception(self):
        with self.assertRaises(RuntimeError) as ctx:
            checked_address('foo-bar-baz')
        self.assertEqual(str(ctx.exception),
                         'Unable to convert foo-bar-baz into and address. The address needs to be a base58 encoded value')
