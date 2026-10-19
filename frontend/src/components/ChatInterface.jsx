import { useState } from 'react'
import { Send } from 'lucide-react'
import axios from 'axios'

export default function ChatInterface() {
  const [messages, setMessages] = useState([
    { role: 'ai', content: '👋 Halo! Saya AI Trading Assistant. Ada yang bisa saya bantu?' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post('/api/chat/message', { message: input })
      const aiMessage = { role: 'ai', content: response.data.response }
      setMessages(prev => [...prev, aiMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      setMessages(prev => [...prev, { 
        role: 'ai', 
        content: '❌ Maaf, terjadi kesalahan. Silakan coba lagi.' 
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="p-6 border-b border-dark-border">
        <h1 className="text-2xl font-bold text-white">Chat AI</h1>
        <p className="text-dark-muted mt-1">Tanya apa saja tentang trading</p>
      </div>

      <div className="flex-1 overflow-auto p-6 space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-2xl rounded-lg p-4 ${
              msg.role === 'user' 
                ? 'bg-primary-600 text-white' 
                : 'bg-dark-card border border-dark-border text-white'
            }`}>
              <pre className="whitespace-pre-wrap font-sans">{msg.content}</pre>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-dark-card border border-dark-border rounded-lg p-4">
              <div className="flex gap-2">
                <div className="w-2 h-2 bg-dark-muted rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-dark-muted rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                <div className="w-2 h-2 bg-dark-muted rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="p-6 border-t border-dark-border">
        <div className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ketik pertanyaan Anda..."
            className="flex-1 bg-dark-bg border border-dark-border rounded-lg px-4 py-3 text-white placeholder-dark-muted focus:outline-none focus:border-primary-600"
            disabled={loading}
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className="bg-primary-600 hover:bg-primary-700 disabled:bg-dark-border disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center gap-2"
          >
            <Send className="w-5 h-5" />
            Send
          </button>
        </div>
      </div>
    </div>
  )
}
