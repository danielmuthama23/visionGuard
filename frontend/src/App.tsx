import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@/components/ui/theme-provider';
import { Dashboard } from '@/pages/Dashboard';
import { Analytics } from '@/pages/Analytics';
import { NFTViewer } from '@/pages/NFTViewer';
import { Admin } from '@/pages/Admin';
import { Navbar } from '@/components/ui/navbar';
import { Toaster } from '@/components/ui/toaster';

export default function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="visionguard-ui-theme">
      <BrowserRouter>
        <div className="min-h-screen bg-background text-foreground">
          <Navbar />
          
          <main className="p-6 max-w-7xl mx-auto">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/nfts" element={<NFTViewer />} />
              <Route path="/admin" element={<Admin />} />
            </Routes>
          </main>
          
          <Toaster />
        </div>
      </BrowserRouter>
    </ThemeProvider>
  );
}