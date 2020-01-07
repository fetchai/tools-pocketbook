from fetchai.ledger.api import LedgerApi


class NetworkUnavailableError(Exception):
    pass


def get_balance(api: LedgerApi, address):
    balance = int(api.tokens.balance(address))
    return balance / 10000000000


def get_stake(api: LedgerApi, addresss):
    stake = int(api.tokens.stake(addresss))
    return stake / 10000000000


def create_api(name: str) -> LedgerApi:
    try:
        return LedgerApi(network=name)
    except:
        pass

    raise NetworkUnavailableError()
