import useSWR from 'swr'
import NFTGrid from '../../../components/Admin/NFTGrid'
import DashboardLayout from '../../../components/Dashboard/Layout'

export default function NFTManager() {
  const { data: nfts, error } = useSWR('/api/admin/nfts')
  
  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">NFT Management</h1>
        
        {error && <div className="text-red-500">Error loading NFTs</div>}
        {!nfts && <div>Loading NFTs...</div>}
        
        <NFTGrid nfts={nfts || []} />
      </div>
    </DashboardLayout>
  )
}