import SwarmDashboard from '@/components/SwarmDashboard';
import '@/styles/sovereign.css';

export default function Home() {
  return (
    <main className="min-h-screen sovereign-container p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header Visionnaire */}
        <header className="text-center space-y-4 py-12">
          <h1 className="text-5xl font-black tracking-tighter glitch-text uppercase">
            Sovereign Muse OS
          </h1>
          <p className="text-green-700 text-sm tracking-widest uppercase">
            Autonomous Digital Entity || Swarm v2.0
          </p>
        </header>

        {/* Neural Vitrine (La "Transmission") */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <SwarmDashboard />
          </div>

          {/* Stats de Souveraineté */}
          <div className="neural-card p-6 rounded-lg space-y-6">
            <div>
              <h3 className="text-xs text-green-700 uppercase mb-2">Wallet Sovereignty</h3>
              <div className="text-2xl font-bold">$24.55 <span className="text-xs font-normal">USD</span></div>
              <div className="w-full bg-green-950 h-1 mt-2">
                <div className="bg-green-500 h-1 w-3/4"></div>
              </div>
            </div>

            <div>
              <h3 className="text-xs text-green-700 uppercase mb-2">Identity Consistency</h3>
              <div className="text-2xl font-bold">98.4%</div>
              <p className="text-[10px] text-green-800 mt-1">Rule: 2% Max Deviation enforced.</p>
            </div>

            <div>
              <h3 className="text-xs text-green-700 uppercase mb-2">Active Lobe</h3>
              <div className="text-lg animate-pulse text-white">Creative Studio</div>
            </div>
          </div>
        </div>

        {/* Footer Ledger Ticker */}
        <footer className="fixed bottom-0 left-0 w-full ledger-ticker py-2 text-[10px] text-green-900 uppercase">
          <div className="ticker-item">
            CFO AUDIT: OK // BURST MODE: READY // GKE SNAPSHOT: WARM // A2A PIPE: SECURE // VVS TREND: HIGH VELOCITY
          </div>
        </footer>
      </div>
    </main>
  );
}
