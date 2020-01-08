from typing import Union

from fetchai.ledger.crypto import Address

CANONICAL_FET_UNIT = 1e10


class NetworkUnavailableError(Exception):
    pass


def to_canonical(value: Union[float, int]) -> int:
    return int(value * CANONICAL_FET_UNIT)


def from_canonical(value: int) -> float:
    return value / int(CANONICAL_FET_UNIT)


def get_balance(api, address):
    balance = int(api.tokens.balance(address))
    return from_canonical(balance)


def get_stake(api, addresss):
    stake = int(api.tokens.stake(addresss))
    return from_canonical(stake)


def create_api(name: str):
    from fetchai.ledger.api import LedgerApi

    try:
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
