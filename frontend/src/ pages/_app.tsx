import type { AppProps } from 'next/app'
import { HederaProvider } from '../lib/hedera'
import AuthGuard from '../components/Shared/AuthGuard'
import '../styles/globals.css'

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <HederaProvider>
      <AuthGuard>
        <Component {...pageProps} />
      </AuthGuard>
    </HederaProvider>
  )
}

export default MyApp