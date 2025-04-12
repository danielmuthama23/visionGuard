import { Client, AccountId, PrivateKey, TokenNftInfoQuery, TokenMintTransaction } from "@hashgraph/sdk";
import { hederaConfig } from '@/config/hedera';
import axios from "axios";

const client = Client.forTestnet()
  .setOperator(
    AccountId.fromString(hederaConfig.accountId),
    PrivateKey.fromString(hederaConfig.privateKey)
  );

export const blockchain = {
  verifyNFTOwnership: async (nftId: string, accountId: string) => {
    try {
      const query = new TokenNftInfoQuery()
        .setNftId(nftId)
        .setAccountId(AccountId.fromString(accountId));
      
      const nftInfo = await query.execute(client);
      return nftInfo.length > 0;
    } catch (error) {
      throw new Error("Failed to verify NFT ownership");
    }
  },

  getTransactionHistory: async (accountId: string) => {
    try {
      const response = await axios.get(
        `${hederaConfig.mirrorNodeUrl}/accounts/${accountId}/nfts`
      );
      return response.data.nfts;
    } catch (error) {
      throw new Error("Failed to fetch transaction history");
    }
  },

  mintParkingNFT: async (metadata: object) => {
    try {
      const transaction = await new TokenMintTransaction()
        .setTokenId(hederaConfig.tokenId)
        .addMetadata(JSON.stringify(metadata))
        .execute(client);

      const receipt = await transaction.getReceipt(client);
      return receipt.serials[0].toString();
    } catch (error) {
      throw new Error("Failed to mint NFT");
    }
  }
};