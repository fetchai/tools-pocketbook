from typing import Union

from fetchai.ledger.crypto import Address

CANONICAL_FET_UNIT = 1e10
MINIMUM_FRACTIONAL_FET = 1 / CANONICAL_FET_UNIT
MAX_TOKEN_PADDING = 10


class NetworkUnavailableError(Exception):
    pass


class ConversionError(RuntimeError):
    def __init__(self, msg):
        super().__init__(msg)


def to_canonical(value: Union[float, int]) -> int:
    value = float(value)
    if value < 0:
        raise ConversionError('Unable to convert negative token amount: {}'.format(value))
    if value < MINIMUM_FRACTIONAL_FET:
        raise ConversionError(
            'Converted value {} is below minimum transfer value: {}'.format(value, MINIMUM_FRACTIONAL_FET))

    return int(value * CANONICAL_FET_UNIT)


def from_canonical(value: int) -> float:
    value = int(value)
    if value < 0:
        raise ConversionError('Unable to convert negative token amount: {}'.format(value))

    return value / int(CANONICAL_FET_UNIT)


def token_amount(value: float) -> str:
    """
    Converts a token amount into a fixed precision string value
    :param value: The input value to display
    :return: The converted value
    """
    padding = ' ' * (MAX_TOKEN_PADDING - min(len(str(int(value))), MAX_TOKEN_PADDING))
    return '{}{:10.10f} FET'.format(padding, float(value))


def get_balance(api, address):
    balance = int(api.tokens.balance(address))
    return from_canonical(balance)


def get_stake(api, addresss):
    stake = int(api.tokens.stake(addresss))
    return from_canonical(stake)


def create_api(name: str):
    from fetchai.ledger.api import LedgerApi

    try:
        if name == 'local':
            return LedgerApi('127.0.0.1', 8000)
        else:
            return LedgerApi(network=name)
    except:
        pass

    raise NetworkUnavailableError()


def checked_address(address):
    try:
        return Address(address)
    except:
        raise RuntimeError(
            'Unable to convert {} into and address. The address needs to be a base58 encoded value'.format(address))
