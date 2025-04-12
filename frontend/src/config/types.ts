// src/config/types.ts
export type HederaConfig = {
    accountId: string;
    privateKey: string;
    tokenId: string;
    mirrorNodeUrl: string;
    network: 'testnet' | 'mainnet';
  }