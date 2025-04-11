import { NextApiRequest, NextApiResponse } from 'next'
import { getParkingLots, processParkingEntry } from '../../../lib/backend-api'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'POST') {
    try {
      const result = await processParkingEntry(req.body)
      res.status(201).json(result)
    } catch (error) {
      res.status(500).json({ error: 'Failed to process parking entry' })
    }
  } else if (req.method === 'GET') {
    const lots = await getParkingLots()
    res.status(200).json(lots)
  } else {
    res.setHeader('Allow', ['GET', 'POST'])
    res.status(405).end(`Method ${req.method} Not Allowed`)
  }
}