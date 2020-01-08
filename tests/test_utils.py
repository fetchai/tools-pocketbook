import unittest
from unittest.mock import MagicMock, patch

from pocketbook.utils import get_balance, get_stake, NetworkUnavailableError

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