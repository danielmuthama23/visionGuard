# blockchain/hashgraph_client/mainnet_connector.py
from hedera import Client, AccountId, PrivateKey
import os

class MainnetClient:
    def __init__(self):
        self.client = Client.forMainnet()
        self._configure_client()
        
    def _configure_client(self):
        account_id = AccountId.fromString(os.getenv("HEDERA_MAINNET_ACCOUNT_ID"))
        private_key = PrivateKey.fromString(os.getenv("HEDERA_MAINNET_PRIVATE_KEY"))
        self.client.setOperator(account_id, private_key)
        
        # Configure mainnet mirror node
        self.client.setMirrorNetwork(["hcs.mainnet.mirrornode.hedera.com:5600"])
        
    def get_client(self):
        return self.client