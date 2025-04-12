// src/config/hedera.ts
export const hederaConfig = {
    accountId: import.meta.env.VITE_HEDERA_ACCOUNT_ID,
    privateKey: import.meta.env.VITE_HEDERA_PRIVATE_KEY,
    tokenId: import.meta.env.VITE_HEDERA_TOKEN_ID,
    mirrorNodeUrl: import.meta.env.VITE_HEDERA_MIRROR_URL,
    network: import.meta.env.VITE_HEDERA_NETWORK || 'testnet'
  } as const;