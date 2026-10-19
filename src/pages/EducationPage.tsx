import { useState } from 'react';
import { glossaryTerms } from '../data/mockData';
import {
  BookOpen,
  MessageCircle,
  Lightbulb,
  Search,
  ChevronDown,
  ChevronUp,
  Send,
  Bot,
  User,
  GraduationCap,
} from 'lucide-react';

interface ChatMessage {
  id: string;
  role: 'user' | 'bot';
  content: string;
  timestamp: string;
}

const predefinedQA: Record<string, string> = {
  'kenapa bot buy': 'Bot melakukan BUY ketika beberapa indikator teknikal dan analisis sentimen secara bersamaan menunjukkan sinyal bullish. Misalnya, ketika RSI menunjukkan oversold (< 30), ada golden cross pada EMA, dan sentimen berita positif. Bot memerlukan minimal confidence 60% untuk mengeksekusi trade.',
  'kenapa bot sell': 'Bot melakukan SELL ketika indikator menunjukkan potensi penurunan harga. Contohnya: RSI overbought (> 70), bearish divergence pada MACD, atau sentimen berita negatif. Bot akan menjual untuk mengamankan profit atau membatasi kerugian.',
  'apa itu rsi': 'RSI (Relative Strength Index) adalah indikator momentum yang mengukur kecepatan perubahan harga. Nilainya 0-100. Di atas 70 = overbought (harga mungkin turun), di bawah 30 = oversold (harga mungkin naik). Ini membantu bot mengidentifikasi titik masuk dan keluar yang optimal.',
  'apa itu paper trading': 'Paper Trading adalah simulasi trading dengan uang virtual. Anda bisa belajar dan menguji strategi tanpa risiko kehilangan uang nyata. Portfolio virtual dimulai dari $10,000 USDT. Semua trade disimulasikan berdasarkan data pasar real-time.',
  'bagaimana risk management': 'Bot menerapkan risk management ketat: (1) Max 2% risiko per trade, (2) Stop-loss otomatis di setiap posisi, (3) Diversifikasi across multiple symbols, (4) Max drawdown limit. Ini melindungi portfolio dari kerugian besar.',
  'apa itu confidence score': 'Confidence Score (0-100%) menunjukkan seberapa yakin bot dengan sinyalnya. Skor dihitung berdasarkan jumlah indikator yang mendukung sinyal. Semakin tinggi confidence, semakin banyak faktor yang mendukung. Bot hanya mengeksekusi trade dengan confidence > 60%.',
  'default': 'Terima kasih atas pertanyaannya! Saya adalah AI Trading Agent yang dirancang untuk membantu Anda memahami trading crypto. Anda bisa bertanya tentang: strategi bot, indikator teknikal (RSI, MACD, EMA), risk management, paper trading, atau istilah trading lainnya. Silakan tanya apa saja!',
};

function getBotResponse(question: string): string {
  const q = question.toLowerCase();
  for (const [key, answer] of Object.entries(predefinedQA)) {
    if (key !== 'default' && q.includes(key.replace(' ', '')) || q.includes(key)) {
      return answer;
    }
  }
  // Check for keyword matches
  if (q.includes('rsi')) return predefinedQA['apa itu rsi'];
  if (q.includes('buy') || q.includes('beli')) return predefinedQA['kenapa bot buy'];
  if (q.includes('sell') || q.includes('jual')) return predefinedQA['kenapa bot sell'];
  if (q.includes('paper') || q.includes('simulasi')) return predefinedQA['apa itu paper trading'];
  if (q.includes('risk') || q.includes('risiko') || q.includes('stop')) return predefinedQA['bagaimana risk management'];
  if (q.includes('confidence') || q.includes('yakin')) return predefinedQA['apa itu confidence score'];
  return predefinedQA['default'];
}

export default function EducationPage() {
  const [activeTab, setActiveTab] = useState<'chat' | 'glossary' | 'guide'>('chat');
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      role: 'bot',
      content: 'Halo! 👋 Saya AI Trading Agent. Saya bisa membantu Anda memahami keputusan trading bot, menjelaskan istilah trading, atau mengajarkan konsep trading. Silakan tanya apa saja!',
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [expandedTerm, setExpandedTerm] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toLocaleTimeString(),
    };

    const botResponse = getBotResponse(inputMessage);
    const botMsg: ChatMessage = {
      id: (Date.now() + 1).toString(),
      role: 'bot',
      content: botResponse,
      timestamp: new Date().toLocaleTimeString(),
    };

    setChatMessages((prev) => [...prev, userMsg, botMsg]);
    setInputMessage('');
  };

  const filteredTerms = glossaryTerms.filter(
    (t) =>
      t.term.toLowerCase().includes(searchTerm.toLowerCase()) ||
      t.definition.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Edukasi & XAI</h1>
          <p className="text-sm text-dark-muted mt-1">Learn trading concepts & understand bot decisions</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-1 bg-dark-card rounded-lg border border-dark-border p-1 w-fit">
        <button
          onClick={() => setActiveTab('chat')}
          className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'chat' ? 'bg-primary text-white' : 'text-dark-muted hover:text-white'
          }`}
        >
          <MessageCircle className="w-4 h-4" />
          Tanya Bot
        </button>
        <button
          onClick={() => setActiveTab('glossary')}
          className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'glossary' ? 'bg-primary text-white' : 'text-dark-muted hover:text-white'
          }`}
        >
          <BookOpen className="w-4 h-4" />
          Kamus Trading
        </button>
        <button
          onClick={() => setActiveTab('guide')}
          className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'guide' ? 'bg-primary text-white' : 'text-dark-muted hover:text-white'
          }`}
        >
          <GraduationCap className="w-4 h-4" />
          Panduan
        </button>
      </div>

      {activeTab === 'chat' && (
        <div className="bg-dark-card rounded-xl border border-dark-border overflow-hidden">
          {/* Chat Header */}
          <div className="px-4 py-3 border-b border-dark-border flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
              <Bot className="w-4 h-4 text-primary" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-white">AI Trading Assistant</h3>
              <p className="text-xs text-dark-muted">Tanya apapun tentang trading & bot</p>
            </div>
          </div>

          {/* Chat Messages */}
          <div className="h-96 overflow-y-auto p-4 space-y-4">
            {chatMessages.map((msg) => (
              <div key={msg.id} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}>
                {msg.role === 'bot' && (
                  <div className="w-7 h-7 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                    <Bot className="w-3.5 h-3.5 text-primary" />
                  </div>
                )}
                <div
                  className={`max-w-[80%] rounded-xl px-4 py-2.5 ${
                    msg.role === 'user'
                      ? 'bg-primary text-white'
                      : 'bg-dark-bg border border-dark-border'
                  }`}
                >
                  <p className="text-sm leading-relaxed">{msg.content}</p>
                  <p className={`text-xs mt-1 ${msg.role === 'user' ? 'text-white/60' : 'text-dark-muted'}`}>
                    {msg.timestamp}
                  </p>
                </div>
                {msg.role === 'user' && (
                  <div className="w-7 h-7 rounded-full bg-success/20 flex items-center justify-center shrink-0">
                    <User className="w-3.5 h-3.5 text-success" />
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Quick Questions */}
          <div className="px-4 py-2 border-t border-dark-border/50">
            <p className="text-xs text-dark-muted mb-2">Pertanyaan cepat:</p>
            <div className="flex flex-wrap gap-2">
              {['Kenapa bot BUY?', 'Apa itu RSI?', 'Bagaimana risk management?', 'Apa itu paper trading?'].map((q) => (
                <button
                  key={q}
                  onClick={() => {
                    setInputMessage(q);
                  }}
                  className="text-xs px-2.5 py-1 rounded-full bg-dark-bg border border-dark-border text-dark-muted hover:text-white hover:border-primary/30 transition-colors"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>

          {/* Input */}
          <div className="px-4 py-3 border-t border-dark-border">
            <div className="flex items-center gap-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Ketik pertanyaan Anda..."
                className="flex-1 px-4 py-2 bg-dark-bg border border-dark-border rounded-lg text-sm text-white placeholder:text-dark-muted focus:outline-none focus:border-primary/50"
              />
              <button
                onClick={handleSendMessage}
                className="w-9 h-9 rounded-lg bg-primary flex items-center justify-center hover:bg-primary-dark transition-colors"
              >
                <Send className="w-4 h-4 text-white" />
              </button>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'glossary' && (
        <div className="space-y-4">
          {/* Search */}
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-dark-muted" />
            <input
              type="text"
              placeholder="Cari istilah trading..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-2.5 bg-dark-card border border-dark-border rounded-lg text-sm text-white placeholder:text-dark-muted focus:outline-none focus:border-primary/50"
            />
          </div>

          {/* Terms */}
          <div className="space-y-2">
            {filteredTerms.map((term) => (
              <div
                key={term.term}
                className="bg-dark-card rounded-xl border border-dark-border overflow-hidden"
              >
                <button
                  onClick={() => setExpandedTerm(expandedTerm === term.term ? null : term.term)}
                  className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-white/[0.02] transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <Lightbulb className="w-4 h-4 text-warning shrink-0" />
                    <span className="text-sm font-semibold text-white">{term.term}</span>
                  </div>
                  {expandedTerm === term.term ? (
                    <ChevronUp className="w-4 h-4 text-dark-muted" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-dark-muted" />
                  )}
                </button>
                {expandedTerm === term.term && (
                  <div className="px-4 pb-4 pt-0 border-t border-dark-border/50">
                    <div className="mt-3 space-y-3">
                      <div>
                        <p className="text-xs font-medium text-dark-muted mb-1">DEFINISI:</p>
                        <p className="text-sm text-dark-text leading-relaxed">{term.definition}</p>
                      </div>
                      <div className="bg-dark-bg rounded-lg p-3 border border-dark-border/50">
                        <p className="text-xs font-medium text-primary mb-1">CONTOH:</p>
                        <p className="text-sm text-dark-text leading-relaxed">{term.example}</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'guide' && (
        <div className="space-y-4">
          {/* Getting Started Guide */}
          <div className="bg-dark-card rounded-xl border border-dark-border p-6">
            <h3 className="text-lg font-bold text-white mb-4">🚀 Panduan Memulai</h3>
            <div className="space-y-4">
              <GuideStep
                step={1}
                title="Pahami Paper Trading"
                description="Sistem ini menggunakan uang virtual ($10,000 USDT). Tidak ada risiko kehilangan uang nyata. Gunakan ini untuk belajar dan memahami bagaimana bot bekerja."
              />
              <GuideStep
                step={2}
                title="Pelajari Indikator Dasar"
                description="Mulai dengan memahami RSI, MACD, dan EMA. Buka tab 'Kamus Trading' untuk penjelasan lengkap setiap istilah."
              />
              <GuideStep
                step={3}
                title="Perhatikan Decision Log"
                description="Setiap keputusan bot dicatat lengkap dengan alasannya. Pelajari pola keputusan bot untuk memahami strateginya."
              />
              <GuideStep
                step={4}
                title="Atur Risk Level"
                description="Mulai dengan 'Conservative' (risiko 1% per trade). Naikkan ke 'Moderate' (2%) atau 'Aggressive' (3%) setelah Anda paham."
              />
              <GuideStep
                step={5}
                title="Tanya Bot!"
                description="Gunakan fitur chat untuk bertanya tentang keputusan bot atau konsep trading. Bot akan menjelaskan dengan bahasa sederhana."
              />
            </div>
          </div>

          {/* How Bot Works */}
          <div className="bg-dark-card rounded-xl border border-dark-border p-6">
            <h3 className="text-lg font-bold text-white mb-4">🤖 Bagaimana Bot Bekerja</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-dark-bg rounded-lg p-4 border border-dark-border">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-6 h-6 rounded bg-blue-500/20 flex items-center justify-center">
                    <span className="text-xs font-bold text-blue-400">1</span>
                  </div>
                  <h4 className="text-sm font-semibold text-white">Data Collection</h4>
                </div>
                <p className="text-xs text-dark-muted leading-relaxed">
                  Bot menarik data harga real-time dari Binance (OHLCV) dan berita crypto dari berbagai sumber setiap 15 menit.
                </p>
              </div>
              <div className="bg-dark-bg rounded-lg p-4 border border-dark-border">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-6 h-6 rounded bg-purple-500/20 flex items-center justify-center">
                    <span className="text-xs font-bold text-purple-400">2</span>
                  </div>
                  <h4 className="text-sm font-semibold text-white">Analysis</h4>
                </div>
                <p className="text-xs text-dark-muted leading-relaxed">
                  Indikator teknikal (RSI, MACD, EMA, Bollinger Bands) dihitung. Sentimen berita dianalisis dengan AI (FinBERT).
                </p>
              </div>
              <div className="bg-dark-bg rounded-lg p-4 border border-dark-border">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-6 h-6 rounded bg-green-500/20 flex items-center justify-center">
                    <span className="text-xs font-bold text-green-400">3</span>
                  </div>
                  <h4 className="text-sm font-semibold text-white">Signal Generation</h4>
                </div>
                <p className="text-xs text-dark-muted leading-relaxed">
                  Semua analisis digabungkan untuk menghasilkan sinyal trading (BUY/SELL/HOLD) dengan confidence score.
                </p>
              </div>
              <div className="bg-dark-bg rounded-lg p-4 border border-dark-border">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-6 h-6 rounded bg-orange-500/20 flex items-center justify-center">
                    <span className="text-xs font-bold text-orange-400">4</span>
                  </div>
                  <h4 className="text-sm font-semibold text-white">Execution</h4>
                </div>
                <p className="text-xs text-dark-muted leading-relaxed">
                  Jika confidence {'>'} threshold, bot mengeksekusi trade dengan stop-loss & take-profit otomatis. Risk management aktif.
                </p>
              </div>
            </div>
          </div>

          {/* Tips */}
          <div className="bg-gradient-to-r from-primary/5 to-purple-500/5 rounded-xl border border-primary/20 p-6">
            <h3 className="text-lg font-bold text-white mb-3">💡 Tips untuk Pemula</h3>
            <ul className="space-y-2">
              <li className="flex items-start gap-2">
                <span className="text-primary mt-0.5">•</span>
                <p className="text-sm text-dark-text">Jangan terburu-buru naik ke risk level tinggi. Habiskan minimal 2 minggu di Conservative.</p>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary mt-0.5">•</span>
                <p className="text-sm text-dark-text">Perhatikan Decision Log setiap hari untuk memahami pola keputusan bot.</p>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary mt-0.5">•</span>
                <p className="text-sm text-dark-text">Gunakan fitur chat untuk bertanya kapanpun Anda bingung dengan keputusan bot.</p>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary mt-0.5">•</span>
                <p className="text-sm text-dark-text">Paper trading bukan jaminan profit di real trading. Selalu lakukan riset tambahan.</p>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary mt-0.5">•</span>
                <p className="text-sm text-dark-text">Focus pada proses belajar, bukan hanya profit. Pahami MENGAPA bot melakukan sesuatu.</p>
              </li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

function GuideStep({ step, title, description }: { step: number; title: string; description: string }) {
  return (
    <div className="flex items-start gap-3">
      <div className="w-7 h-7 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
        <span className="text-xs font-bold text-primary">{step}</span>
      </div>
      <div>
        <h4 className="text-sm font-semibold text-white">{title}</h4>
        <p className="text-xs text-dark-muted leading-relaxed mt-0.5">{description}</p>
      </div>
    </div>
  );
}
