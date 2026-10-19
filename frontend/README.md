# 🎨 AI Trading Agent - Frontend

Frontend React untuk AI Trading Agent dengan Vite, Tailwind CSS, dan TypeScript.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Run Development Server

```bash
npm run dev
```

Frontend akan berjalan di `http://localhost:5173`

### 3. Build for Production

```bash
npm run build
```

Output akan ada di folder `dist/`

## 📁 Struktur Folder

```
frontend/
├── src/
│   ├── components/
│   │   ├── Sidebar.jsx          # Navigation sidebar
│   │   ├── Dashboard.jsx        # Portfolio overview
│   │   └── ChatInterface.jsx    # Chat dengan AI
│   ├── pages/
│   │   └── Home.jsx             # Main page
│   ├── App.jsx                  # Router setup
│   ├── main.jsx                 # Entry point
│   └── index.css                # Tailwind styles
├── index.html                   # HTML template
├── package.json                 # Dependencies
├── vite.config.js               # Vite config
├── tailwind.config.js           # Tailwind config
└── postcss.config.js            # PostCSS config
```

## 🎨 Tech Stack

- **React 18** - UI library
- **Vite** - Build tool & dev server
- **Tailwind CSS** - Utility-first CSS
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Lightweight Charts** - TradingView charts
- **Lucide React** - Icon library

## 📡 API Integration

Frontend terhubung ke backend API di `http://localhost:8000`

### Endpoints yang Digunakan:

**Portfolio:**
- `GET /api/portfolio/summary` - Portfolio summary
- `GET /api/portfolio/positions` - Open positions
- `GET /api/portfolio/history` - Trade history
- `GET /api/portfolio/equity-curve` - Equity curve data

**Signals:**
- `GET /api/signals/analyze/{symbol}` - Analyze symbol
- `GET /api/signals/active` - Active signals
- `GET /api/signals/history` - Signal history

**Market:**
- `GET /api/market/tickers` - All tickers
- `GET /api/market/candles/{symbol}` - Candlestick data
- `GET /api/market/news` - Latest news

**Chat:**
- `POST /api/chat/message` - Send message to AI
- `GET /api/chat/suggestions` - Suggestion questions

**WebSocket:**
- `WS /ws` - Real-time updates

## 🎯 Components

### Sidebar
Navigation sidebar dengan links ke semua pages.

### Dashboard
Overview portfolio dengan:
- Total balance & P&L
- Open positions
- Performance metrics
- Win rate & profit factor

### ChatInterface
Chat interface dengan AI Trading Assistant:
- Real-time chat
- Suggestion buttons
- Message history
- Typing indicators

## 🔧 Configuration

### Vite Config (`vite.config.js`)
```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      },
    },
  },
})
```

### Tailwind Config (`tailwind.config.js`)
Custom colors untuk dark theme:
```javascript
colors: {
  primary: { ... },
  success: '#10b981',
  danger: '#ef4444',
  warning: '#f59e0b',
  dark: {
    bg: '#0f1117',
    card: '#1a1d29',
    border: '#2a2d3a',
    text: '#e2e8f0',
    muted: '#94a3b8',
  },
}
```

## 📊 Data Flow

```
User Input
    ↓
React Components
    ↓
API Calls (Axios)
    ↓
Backend API (FastAPI)
    ↓
Database (SQLite)
    ↓
Response
    ↓
Update UI
```

## 🎨 Styling

Menggunakan Tailwind CSS dengan custom dark theme:

```jsx
<div className="bg-dark-card border border-dark-border rounded-lg p-6">
  <h2 className="text-xl font-bold text-white">Title</h2>
  <p className="text-dark-muted">Description</p>
</div>
```

## 🚀 Deployment

### Build
```bash
npm run build
```

### Serve
```bash
# Menggunakan serve
npx serve dist

# Atau menggunakan nginx/apache
# Point root ke folder dist/
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process di port 3000
lsof -ti:3000 | xargs kill -9
```

### API Connection Failed
- Pastikan backend running di `http://localhost:8000`
- Check CORS settings di backend
- Check proxy config di `vite.config.js`

### Tailwind Not Working
```bash
# Rebuild Tailwind
npm run build
```

## 📚 Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [React Router](https://reactrouter.com/)
- [Axios](https://axios-http.com/)
- [Lightweight Charts](https://tradingview.github.io/lightweight-charts/)

## ✅ Status

**Frontend: READY ✅**

- ✅ React 18 setup
- ✅ Vite configured
- ✅ Tailwind CSS integrated
- ✅ API integration ready
- ✅ Components created
- ✅ Build successful

---

**Frontend siap untuk development! 🎨🚀**
