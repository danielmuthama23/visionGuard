import { NextApiRequest, NextApiResponse } from 'next'
import { getNFTsByAccount } from '../../../lib/hedera'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { accountId } = req.query
  
  if (req.method === 'GET') {
    try {
      const nfts = await getNFTsByAccount(accountId as string)
      res.status(200).json(nfts)
    } catch (error) {
      res.status(500).json({ error: 'Failed to fetch NFTs' })
    }
  } else {
    res.setHeader('Allow', ['GET'])
    res.status(405).end(`Method ${req.method} Not Allowed`)
  }
}