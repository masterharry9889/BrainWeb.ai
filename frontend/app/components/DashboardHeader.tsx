import { Settings } from 'lucide-react';

export default function DashboardHeader() {
  return (
    <header style={{ width: '100%', padding: '1rem 2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div className="logo-small" style={{ fontSize: '1.5rem', padding: 0, display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <img src="./logo.webp" alt="BrainWeb Logo" style={{ height: '36px', width: 'auto', borderRadius: '8px' }} />
        BrainWeb
      </div>
      <a href="./settings/index.html" className="notch-icon-btn" style={{ background: 'transparent', margin: 0 }} title="Settings">
        <Settings size={20} />
      </a>
    </header>
  );
}
