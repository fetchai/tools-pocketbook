import unittest
from unittest.mock import MagicMock, patch
from typing import Union

from fetchai.ledger.crypto import Address, Entity

from pocketbook.utils import get_balance, get_stake, NetworkUnavailableError, checked_address, to_canonical, from_canonical


class UtilsTests(unittest.TestCase):

    def test_get_balance(self):
        api = MagicMock()
        api.tokens.balance.return_value = to_canonical(10)

        balance = get_balance(api, 'some address')
        self.assertEqual(balance, 10)

        api.tokens.balance.assert_called_once_with('some address')

    def test_get_stake(self):
        api = MagicMock()
        api.tokens.stake.return_value = to_canonical(5)

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


class FetConversionTests(unittest.TestCase):
    def assertIsConvertible(self, canonical: int, value: Union[int, float]):
        converted_canonical = to_canonical(value)
        self.assertEqual(canonical, converted_canonical)
        self.assertEqual(float(value), from_canonical(converted_canonical))

    def test_canonical_conversions(self):
        self.assertIsConvertible(10000000000, 1)
        self.assertIsConvertible(10000000000, 1.0)
        self.assertIsConvertible(12000000000, 1.2)
        self.assertIsConvertible(10020000000, 1.002)
        self.assertIsConvertible(1, 1e-10)
        self.assertIsConvertible(100, 1e-8)
        self.assertIsConvertible(10000000, 1e-3)
        self.assertIsConvertible(10000, 1e-6)
        self.assertIsConvertible(10, 1e-9)
        self.assertIsConvertible(10000000000000, 1e3)
        self.assertIsConvertible(10000000000000000, 1e6)
        self.assertIsConvertible(10000000000000000000, 1e9)
