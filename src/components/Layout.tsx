import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  LineChart,
  ScrollText,
  GraduationCap,
  Settings,
  Bot,
  Menu,
  X,
  Zap,
  Activity,
} from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/chart', label: 'Chart & Signals', icon: LineChart },
  { path: '/log', label: 'Decision Log', icon: ScrollText },
  { path: '/education', label: 'Edukasi & XAI', icon: GraduationCap },
  { path: '/system', label: 'System Status', icon: Activity },
  { path: '/settings', label: 'Pengaturan', icon: Settings },
];

export default function Layout({ children }: LayoutProps) {
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen bg-dark-bg">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed lg:static inset-y-0 left-0 z-50 w-64 bg-dark-card border-r border-dark-border transform transition-transform duration-200 ease-in-out ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center gap-3 px-6 py-5 border-b border-dark-border">
            <div className="w-9 h-9 rounded-lg bg-primary/20 flex items-center justify-center">
              <Bot className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h1 className="text-sm font-bold text-white">AI Trading Agent</h1>
              <p className="text-xs text-dark-muted">Paper Trading Mode</p>
            </div>
          </div>

          {/* Status indicator */}
          <div className="px-6 py-3 border-b border-dark-border">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-success animate-pulse-green" />
              <span className="text-xs text-dark-muted">Bot Active • Binance Testnet</span>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-3 py-4 space-y-1">
            {navItems.map((item) => {
              const isActive = location.pathname === item.path;
              const Icon = item.icon;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setSidebarOpen(false)}
                  className={`flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 ${
                    isActive
                      ? 'bg-primary/10 text-primary border border-primary/20'
                      : 'text-dark-muted hover:text-white hover:bg-white/5'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {item.label}
                </Link>
              );
            })}
          </nav>

          {/* Bottom info */}
          <div className="px-4 py-4 border-t border-dark-border">
            <div className="bg-gradient-to-r from-primary/10 to-purple-500/10 rounded-lg p-3 border border-primary/20">
              <div className="flex items-center gap-2 mb-1">
                <Zap className="w-3.5 h-3.5 text-warning" />
                <span className="text-xs font-medium text-white">Pro Tip</span>
              </div>
              <p className="text-xs text-dark-muted leading-relaxed">
                Mulai dengan risk level "Conservative" saat belajar.
              </p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top bar */}
        <header className="h-14 border-b border-dark-border flex items-center justify-between px-4 lg:px-6 bg-dark-card/50 backdrop-blur-sm">
          <button
            onClick={() => setSidebarOpen(true)}
            className="lg:hidden p-2 rounded-lg hover:bg-white/5"
          >
            {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>

          <div className="hidden lg:flex items-center gap-4">
            <div className="flex items-center gap-2 text-xs">
              <span className="text-dark-muted">Portfolio:</span>
              <span className="text-white font-semibold">$11,247.83</span>
              <span className="text-success font-medium">+12.48%</span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-success/10 border border-success/20">
              <div className="w-1.5 h-1.5 rounded-full bg-success animate-pulse" />
              <span className="text-xs font-medium text-success">Paper Trading</span>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-auto p-4 lg:p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
