import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk import account

from algosdk.transaction  import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn, wait_for_confirmation

class Algorand():

    def __init__(self,**kwargs):

        algod_address = kwargs.get("algod_address","http://localhost:4001")
        algod_token = kwargs.get("algod_address","aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        self.algod_client = algod.AlgodClient(algod_token, algod_address)
        print(self.algod_client.status())


    def create_account(self):
        
        private_key, public_address = account.generate_account()
        print("Base64 Private Key: {}\nPublic Algorand Address: {}\n".format(private_key, public_address))
        print("Reminder: Send Algo to Public Address")
        return private_key, public_address


    def account_info(self,account_address):

        
        print("My address: {}".format(account_address))  
        account_info = self.algod_client.account_info(account_address)  
        print("Account balance: {} microAlgos".format(account_info.get('amount')))  

        return account_info

    def create_asset(self,kwargs):
        manager_address = kwargs.get("asset_manager_address")
        sender_address= kwargs.get("sender_address",manager_address)
        reserve_address =  kwargs.get("reserve_address",manager_address)
        freeze_address = kwargs.get("freeze_address",manager_address)
        clawback_address = kwargs.get("clawback",manager_address)


        # CREATE ASSET
        # Get network params for transactions before every transaction.
        params = self.algod_client.suggested_params()
        # comment these two lines if you want to use suggested params
        # params.fee = 1000
        # params.flat_fee = True
        # Account 1 creates an asset called latinum and
        # sets Account 2 as the manager, reserve, freeze, and clawback address.
        # Asset Creation transaction
        txn = AssetConfigTxn(
            sender=sender_address,
            sp=params,
            total=1000,
            default_frozen=False,
            unit_name="TenToken",
            asset_name="10 Academy Certificate",
            manager=manager_address,
            reserve=reserve_address,
            freeze=freeze_address,
            clawback=clawback_address,
            url="https://www.10academy.org/", 
            decimals=0)
        # Sign with secret key of creator
        stxn = txn.sign(private_key)
        # Send the transaction to the network and retrieve the txid.
        try:
            txid = algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            # Wait for the transaction to be confirmed
            confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
            print("TXID: ", txid)
            print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))   
        except Exception as err:
            print("error")
            print(err)
        # Retrieve the asset ID of the newly created asset by first
        # ensuring that the creation transaction was confirmed,
        # then grabbing the asset id from the transaction.
        print("Transaction information: {}".format(
            json.dumps(confirmed_txn, indent=4)))
       
    def opt_in(self, opting_private_address, opting_public_address, asset_id ):
        
        params = self.algod_client.suggested_params()
        
        if not False:
            # Use the AssetTransferTxn class to transfer assets and opt-in
            txn = AssetTransferTxn(
                sender=opting_public_address,
                sp=params,
                receiver=opting_public_address,
                amt=0,
                index=asset_id)
            stxn = txn.sign(opting_private_address)
            # Send the transaction to the network and retrieve the txid.
            try:
                txid = self.algod_client.send_transaction(stxn)
                print("Signed transaction with txID: {}".format(txid))
                # Wait for the transaction to be confirmed
                confirmed_txn = wait_for_confirmation(self.algod_client, txid, 4) 
                print("TXID: ", txid)
                print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))    
            except Exception as err:
                print("error")
                print(err)
            
        print(self.algod_client.account_info(opting_private_address))


    def transfer_asset(self,sender_public_address,sender_private_address,receiver_public_address,asset_id):

        params = self.algod_client.suggested_params()
        # comment these two lines if you want to use suggested params
        # params.fee = 1000
        # params.flat_fee = True
        txn = AssetTransferTxn(
            sender=sender_public_address,
            sp=params,
            receiver=receiver_public_address,
            amt=10,
            index=asset_id)
        stxn = txn.sign(sender_private_address)
        # Send the transaction to the network and retrieve the txid.
        try:
            txid = self.algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            # Wait for the transaction to be confirmed
            confirmed_txn = wait_for_confirmation(self.algod_client, txid, 4) 
            print("TXID: ", txid)
            print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
        except Exception as err:
            print(err)
