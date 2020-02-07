import unittest
from typing import Union
from unittest.mock import MagicMock, patch

from fetchai.ledger.crypto import Address, Entity

from pocketbook.utils import get_balance, get_stake, NetworkUnavailableError, checked_address, to_canonical, \
    from_canonical, token_amount, ConversionError


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

    @patch('fetchai.ledger.api.LedgerApi')
    def test_create_api_local(self, MockLedgerApi):
        # normal use
        from pocketbook.utils import create_api
        create_api('local')

        MockLedgerApi.assert_called_once_with('127.0.0.1', 8000)
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

    def test_token_amount_formatting(self):
        self.assertEqual(token_amount(1), '         1.0000000000 FET')
        self.assertEqual(token_amount(1.0), '         1.0000000000 FET')
        self.assertEqual(token_amount(1.2), '         1.2000000000 FET')
        self.assertEqual(token_amount(1.002), '         1.0020000000 FET')
        self.assertEqual(token_amount(1e-10), '         0.0000000001 FET')
        self.assertEqual(token_amount(1e-8), '         0.0000000100 FET')
        self.assertEqual(token_amount(1e-3), '         0.0010000000 FET')
        self.assertEqual(token_amount(1e-6), '         0.0000010000 FET')
        self.assertEqual(token_amount(1e-9), '         0.0000000010 FET')
        self.assertEqual(token_amount(1e3), '      1000.0000000000 FET')
        self.assertEqual(token_amount(1e6), '   1000000.0000000000 FET')
        self.assertEqual(token_amount(1e9), '1000000000.0000000000 FET')

    def test_invalid_negative_to_canonical(self):
        with self.assertRaises(ConversionError):
            to_canonical(-10)

    def test_invalid_too_small_to_canonical(self):
        with self.assertRaises(ConversionError):
            to_canonical(1e-20)

    def test_invalid_non_number_to_canonical(self):
        with self.assertRaises(ValueError):
            to_canonical('foo-bar')

    def test_invalid_negative_from_canonical(self):
        with self.assertRaises(ConversionError):
            from_canonical(-10)
