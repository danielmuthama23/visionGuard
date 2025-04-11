# blockchain/nft_minting/hts_nft.py
from hedera import (
    Client, PrivateKey, AccountId, TokenCreateTransaction,
    TokenType, TokenSupplyType, TokenMintTransaction, CustomFee,
    Hbar, TokenId, NftId, TokenNftInfoQuery
)
import json
import os

class HederaNFTHandler:
    def __init__(self):
        self.client = Client.forName(os.getenv("HEDERA_NETWORK", "testnet"))
        self.client.setOperator(
            AccountId.fromString(os.getenv("HEDERA_ACCOUNT_ID")),
            PrivateKey.fromString(os.getenv("HEDERA_PRIVATE_KEY"))
        )
        self.nft_token_id = None

    async def create_parking_nft_collection(self):
        """Create NFT collection for parking tickets"""
        transaction = (
            TokenCreateTransaction()
            .setTokenName("VisionGuard Parking NFT")
            .setTokenSymbol("VGPN")
            .setTokenType(TokenType.NON_FUNGIBLE_UNIQUE)
            .setSupplyType(TokenSupplyType.FINITE)
            .setMaxSupply(100000)
            .setTreasuryAccountId(AccountId.fromString(os.getenv("HEDERA_TREASURY_ACCOUNT")))
            .setCustomFees([
                CustomFee()
                .setFeeCollectorAccountId(AccountId.fromString(os.getenv("HEDERA_FEE_ACCOUNT")))
                .setHbarFee(Hbar(1))
            ])
        )

        tx_response = await transaction.executeAsync(self.client)
        receipt = await tx_response.getReceiptAsync(self.client)
        self.nft_token_id = receipt.tokenId
        return self.nft_token_id

    async def mint_parking_nft(self, vehicle_data):
        """Mint NFT with vehicle metadata"""
        metadata = {
            "vehicle": {
                "plate": vehicle_data["plate"],
                "color": vehicle_data["color"],
                "type": vehicle_data["type"],
                "entry_time": vehicle_data["entry_time"],
                "location": vehicle_data["location"]
            },
            "payment": {
                "rate": vehicle_data["rate"],
                "currency": "HBAR"
            }
        }

        mint_tx = (
            TokenMintTransaction()
            .setTokenId(self.nft_token_id)
            .addMetadata(json.dumps(metadata).encode())
            .freezeWith(self.client)
        )

        signed_tx = await mint_tx.signAsync(
            PrivateKey.fromString(os.getenv("HEDERA_PRIVATE_KEY"))
        )
        response = await signed_tx.executeAsync(self.client)
        receipt = await response.getReceiptAsync(self.client)
        return NftId(self.nft_token_id, receipt.serials[0])

    async def validate_nft_ownership(self, nft_id):
        """Verify NFT ownership"""
        query = TokenNftInfoQuery().setNftId(nft_id)
        nft_info = await query.executeAsync(self.client)
        return nft_info.owner.toString()