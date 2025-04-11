# blockchain/nft_minting/payment_verifier.py
from hedera import AccountBalanceQuery, Hbar
from .hts_nft import HederaNFTHandler
import os

class PaymentValidator:
    def __init__(self):
        self.nft_handler = HederaNFTHandler()
        
    async def validate_parking_payment(self, nft_id):
        """Validate NFT payment and account balance"""
        # Check NFT ownership
        owner = await self.nft_handler.validate_nft_ownership(nft_id)
        
        # Check account balance
        balance_query = AccountBalanceQuery().setAccountId(
            AccountId.fromString(owner)
        )
        balance = await balance_query.executeAsync(self.nft_handler.client)
        
        # Verify minimum balance
        return balance.hbars > Hbar.fromTinybars(10000)  # 0.01 HBAR