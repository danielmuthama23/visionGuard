/** @type {import('next').NextConfig} */
module.exports = {
  reactStrictMode: true,
  images: {
    domains: [
      'hashscan.io',
      '*.azurestorage.net'
    ],
  },
  env: {
    API_URL: process.env.API_URL || 'http://localhost:5000',
    WS_URL: process.env.WS_URL || 'ws://localhost:5001',
    HEDERA_NETWORK: process.env.HEDERA_NETWORK || 'testnet',
    HEDERA_ACCOUNT_ID: process.env.HEDERA_ACCOUNT_ID,
    HEDERA_PRIVATE_KEY: process.env.HEDERA_PRIVATE_KEY
  },
  webpack: (config) => {
    config.resolve.fallback = { 
      fs: false,
      net: false,
      tls: false
    }
    return config
  }
}