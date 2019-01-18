# PocketBook

Simple python based CLI tool for interacting with the token API of the Fetch.AI ledger

## Development

To develop make sure you and downloaded and installed the fetch ledger python SDK beforehand. Once
this is completed simple install in develop mode as follows:

    python3 setup.py develop

## How To

### Setup a ledger node in the registry

    pocketbook -t local setup

Then follow the prompts to configure host and port


### Creating Public/Private key pairs

    pocketbook -t local create main

This command will generate a key identity wit the name `main`


### Creating wealth for an identity

    pocketbook -t local wealth main 100

This command will add 100 tokens to the balance of the main identity


### Adding public keys to the address book (no generation)

    pocketbook -t local add other Base64EncodedPublicKey=

This will create an address entry called `other` defined with the public key `Base64EncodedPublicKey=`.


### Listing all addresses currently stored

    pocketbook -t local addresses

This command will print out the list of addresses that are stored on the system. To see that actual
public keys you need to include the `-v` (verbose) flag

    pocketbook -t local addresses -v


### Transfering tokens

    pocketbook -t local transfer main other 10

This command will transfer 10 tokens (if they are present) from the `main` identity to a `other`
address

