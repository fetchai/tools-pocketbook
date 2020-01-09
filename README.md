# PocketBook
![](https://github.com/fetchai/tools-pocketbook/workflows/CI/badge.svg)
![](https://img.shields.io/pypi/v/pocketbook)
![](https://img.shields.io/github/release-date/fetchai/tools-pocketbook)
![](https://img.shields.io/pypi/pyversions/pocketbook)

PocketBook is a simple command line wallet that is intended to be used for test purposes on the Fetch.ai networks.

## License

This application is licensed under the Apache software license (see LICENSE file). Unless required by
applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

Fetch.AI makes no representation or guarantee that this software (including any third-party libraries)
will perform as intended or will be free of errors, bugs or faulty code. The software may fail which
could completely or partially limit functionality or compromise computer systems. If you use or
implement the ledger, you do so at your own risk. In no event will Fetch.ai be liable to any party
for any damages whatsoever, even if it had been advised of the possibility of damage.

# Getting Started

## Installation

This application is available from the PyPI. Simply run the following command to download and install the latest version

```
pip3 install -U pocketbook
```

## Creating a new address

To create a new address simply run the following command:

```
pocketbook create
```

You will be prompted to enter a name for this key pair, followed by a password for the key. Below is a sample output:

```
Enter name for key: foo
Enter password for key...:
Confirm password for key.:
```

## Querying funds

You can query the balance of your account with the following command:

```
pocketbook -n devnet list
```

The example above is querying the `devnet` network. If you do not specify a network, `mainnet` will be used.


## Adding addresses

The wallet also has an address book. You can add addresses with the following command:

```
pocketbook add <name-for-the-address> <address>
```

## Renaming addresses

If you don't like the name that you have given to a wallet, this can be changed with the following command:

```
pocketbook rename <bad-name> <new-name>
```

## Deleting addresses

If you want to remove an address this can be done with the following command:

```
pocketbook delete <name>
```

Be very careful when running the command, because this is not revertable. It could potentially mean that you loose
access to your funds.

When deleting a private key, `pocketbook` will prompt you to enter the full address of the wallet that you want to
delete as a security check.

## Making a transfer

To make a transfer you would use the `transfer` command in the following form:

```
pocketbook -n devnet transfer <destination-name> <amount> <source-main>
```

For example, if you wanted to send `10` FET from your address called `main` to another address called `other` you would
use the following command:

```
pocketbook -n devnet transfer other 10 main
```

You would then be prompted with a summary of the transfer (before it happens) so that you can verify the details.

```
Network....: devnet
From.......: main
Signers....: main
Destination: other: UAHCrmwEEmYBNFt8mJXZB6CiqJ2kZcGsR8tjj3f6GkZuR7YnR
Amount.....: 10.0000000000 FET
Fee........: 0.0000000001 FET
Total......: 10.0000000001 FET (Amount + Fee)
    
Press enter to continue
```

If you are happy with the transfer, then press enter to continue. You will be then prompted for the password for your
signing account.

```
Enter password for key main:
```

After this you except to see the following as the transaction is submitted to the network. This process by default 
blocks until the transaction has been included into the chain

```
Submitting TX...
Submitting TX...complete
```

### Changing the charge rate

By default `pocketbook` chooses the minimum possible fee to be paid, however, if you want to update this, then simply
use the `--charge-rate` or `-R` flag to set the required charge rate
