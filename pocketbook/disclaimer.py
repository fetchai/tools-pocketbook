import os

from .constants import DEFAULT_KEY_STORE_ROOT

DISCLAIMER = """
                                == Warning ==

You use this application at your own risk. Whilst Fetch.ai have made every
effort to ensure its reliability and security, it comes with no warranty. It is
intended for the creation and management of Fetch.ai mainnet wallets and
transactions between them. You are responsible for the security of your own
private keys (see ~/.pocketbook folder). Do not use this application for
high-value operations: it is intended for utility operations on the main network.
"""


def display_disclaimer(root=None):
    key_store_root = root or DEFAULT_KEY_STORE_ROOT
    if not os.path.isdir(key_store_root):
        print(DISCLAIMER)
        input('Press enter to accept')
