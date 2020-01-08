

class NetworkUnavailableError(Exception):
    pass


def get_balance(api, address):
    balance = int(api.tokens.balance(address))
    return balance / 10000000000


def get_stake(api, addresss):
    stake = int(api.tokens.stake(addresss))
    return stake / 10000000000


def create_api(name: str):
    from fetchai.ledger.api import LedgerApi

    try:
        return LedgerApi(network=name)
    except:
        pass

    raise NetworkUnavailableError()
