# blockchain/hashgraph_client/testnet_connector.py
from hedera import Client, AccountId, PrivateKey
import os

class TestnetClient:
    def __init__(self):
        self.client = Client.forTestnet()
        self._configure_client()
        
    def _configure_client(self):
        account_id = AccountId.fromString(os.getenv("HEDERA_TESTNET_ACCOUNT_ID"))
        private_key = PrivateKey.fromString(os.getenv("HEDERA_TESTNET_PRIVATE_KEY"))
        self.client.setOperator(account_id, private_key)
        
        # Configure testnet mirror node
        self.client.setMirrorNetwork(["hcs.testnet.mirrornode.hedera.com:5600"])
        
    def get_client(self):
        return self.client