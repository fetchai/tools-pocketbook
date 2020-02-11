def run_transfer(args):
    from getpass import getpass

    from fetchai.ledger.crypto import Address
    from fetchai.ledger.api.token import TokenTxFactory

    from pocketbook.address_book import AddressBook
    from pocketbook.key_store import KeyStore
    from pocketbook.utils import create_api, from_canonical, token_amount

    address_book = AddressBook()
    key_store = KeyStore()

    # choose the destination
    destination_name = '{}:'.format(args.destination)
    if args.destination in address_book.keys():
        destination = address_book.lookup_address(args.destination)
    else:
        destination = key_store.lookup_address(args.destination)
        if destination is None:
            destination = Address(args.destination)
            destination_name = ''

    # convert the amount
    amount = args.amount
    charge_rate = args.charge_rate
    computed_amount = from_canonical(amount)

    # check all the signers make sense
    for signer in args.signers:
        if signer not in key_store.list_keys():
            raise RuntimeError('Unknown key: {}'.format(signer))

    # determine the from account
    from_address_name = None
    if len(args.signers) == 1 and args.from_address is None:
        from_address_name = args.signers[0]
    elif len(args.signers) >= 1 and args.from_address is not None:
        present = args.from_address in key_store.list_keys() or args.from_address in address_book.keys()
        from_address_name = args.from_address
        if not present:
            raise RuntimeError('Unknown from address: {}'.format(args.from_address))
    else:
        raise RuntimeError('Unable to determine from account')

    required_ops = len(args.signers)
    fee = required_ops * charge_rate
    computed_fee = from_canonical(fee)
    computed_total = computed_amount + computed_fee
    computed_charge_rate = from_canonical(charge_rate)

    print('Network....:', args.network)
    print('From.......:', str(from_address_name))
    print('Signer(s)..:', ','.join(args.signers))
    print('Destination:', destination_name, str(destination))
    print('Amount.....:', token_amount(computed_amount))
    print('Fee........:', token_amount(computed_fee))

    # only display extended fee information if something other than the default it selected
    if charge_rate != 1:
        print('           : {} ops @ {}'.format(required_ops, token_amount(computed_charge_rate)))

    print('Total......:', token_amount(computed_total), '(Amount + Fee)')
    print()
    input('Press enter to continue')

    api = create_api(args.network)

    # start unsealing the private keys
    entities = {}
    for signer in args.signers:
        entity = key_store.load_key(signer, getpass('Enter password for key {}: '.format(signer)))
        entities[signer] = entity

    from_address = None
    if from_address_name in entities:
        from_address = Address(entities[from_address_name])
    elif from_address_name in address_book.keys():
        from_address = Address(address_book.lookup_address(from_address_name))

    # cache the signers
    signers = list(entities.values())

    # build up the basic transaction information
    tx = TokenTxFactory.transfer(Address(from_address), destination, amount, 0, signers)
    tx.charge_rate = charge_rate
    tx.charge_limit = required_ops
    api.set_validity_period(tx)
    for entity in signers:
        tx.sign(entity)

    tx_digest = api.submit_signed_tx(tx)
    print('TX: 0x{} submitted'.format(tx_digest))

    # submit the transaction
    print('Waiting for transaction to be confirmed...')
    api.sync(tx_digest)
    print('Waiting for transaction to be confirmed...complete')

    # determine if there is a block explorer link to be printed
    explorer_link = None
    if args.network == 'mainnet':
        explorer_link = 'https://explore.fetch.ai/transactions/0x{}'.format(tx_digest)
    elif args.network == 'testnet':
        explorer_link = 'https://explore-testnet.fetch.ai/transactions/0x{}'.format(tx_digest)

    if explorer_link is not None:
        print()
        print('See {} for more details'.format(explorer_link))