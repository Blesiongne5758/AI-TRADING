import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Home from './pages/Home'
import ChartView from './components/ChartView'
import SignalLog from './components/SignalLog'
import ChatInterface from './components/ChatInterface'
import Settings from './components/Settings'

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-dark-bg">
        <Sidebar />
        <main className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/chart" element={<ChartView />} />
            <Route path="/signals" element={<SignalLog />} />
            <Route path="/chat" element={<ChatInterface />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
