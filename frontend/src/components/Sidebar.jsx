import { Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, LineChart, ScrollText, MessageCircle, Settings, Bot } from 'lucide-react'

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/chart', label: 'Chart', icon: LineChart },
  { path: '/signals', label: 'Signals', icon: ScrollText },
  { path: '/chat', label: 'Chat AI', icon: MessageCircle },
  { path: '/settings', label: 'Settings', icon: Settings },
]

export default function Sidebar() {
  const location = useLocation()

  return (
    <aside className="w-64 bg-dark-card border-r border-dark-border flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-dark-border">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white">AI Trading</h1>
            <p className="text-xs text-dark-muted">Agent v1.0</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-primary-600 text-white'
                  : 'text-dark-muted hover:bg-dark-border hover:text-white'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="font-medium">{item.label}</span>
            </Link>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-dark-border">
        <div className="flex items-center gap-2 text-xs text-dark-muted">
          <div className="w-2 h-2 bg-success rounded-full animate-pulse"></div>
          <span>System Online</span>
        </div>
      </div>
    </aside>
  )
}
