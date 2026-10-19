"""
Chat Agent
Chat interface dengan pattern matching untuk menjawab pertanyaan user
"""
from typing import Dict, Optional, List
from loguru import logger
from .trading_dictionary import TradingDictionary
from .explanation_generator import ExplanationGenerator
from .context_builder import ContextBuilder
from data_collector.database import DatabaseManager


class ChatAgent:
    """
    Chat agent untuk menjawab pertanyaan user tentang trading
    
    Menggunakan pattern matching untuk memahami pertanyaan dan memberikan jawaban yang relevan
    """

    def __init__(self, db: DatabaseManager):
        """
        Initialize chat agent
        
        Args:
            db: DatabaseManager instance
        """
        self.db = db
        self.dictionary = TradingDictionary()
        self.explanation_gen = ExplanationGenerator()
        self.context_builder = ContextBuilder(db)
        
        # Pattern matching rules
        self.patterns = self._build_patterns()
        
        logger.info("💬 Chat Agent initialized")

    def _build_patterns(self) -> Dict[str, Dict]:
        """Build pattern matching rules"""
        return {
            # Greetings
            "greeting": {
                "patterns": ["halo", "hai", "hello", "hi", "hey", "selamat"],
                "response": "Halo! 👋 Saya AI Trading Agent. Saya bisa membantu Anda memahami:\n\n"
                           "• Keputusan trading bot\n"
                           "• Istilah trading (ketik 'kamus [istilah]')\n"
                           "• Status portfolio (ketik 'portfolio')\n"
                           "• Analisis market (ketik 'analisis [symbol]')\n\n"
                           "Silakan tanya apa saja!"
            },
            
            # Help
            "help": {
                "patterns": ["help", "bantuan", "bantu", "cara", "bagaimana"],
                "response": "📚 Berikut cara menggunakan chat agent:\n\n"
                           "1️⃣  Tanya tentang istilah trading:\n"
                           "   • 'apa itu RSI?'\n"
                           "   • 'jelaskan MACD'\n"
                           "   • 'kamus bollinger'\n\n"
                           "2️⃣  Tanya tentang keputusan bot:\n"
                           "   • 'kenapa bot buy BTC?'\n"
                           "   • 'jelaskan signal terakhir'\n\n"
                           "3️⃣  Cek portfolio:\n"
                           "   • 'portfolio'\n"
                           "   • 'status portfolio'\n"
                           "   • 'performance'\n\n"
                           "4️⃣  Analisis market:\n"
                           "   • 'analisis BTC'\n"
                           "   • 'bagaimana ETH?'\n\n"
                           "Silakan coba!"
            },
            
            # Dictionary queries
            "dictionary": {
                "patterns": ["apa itu", "jelaskan", "kamus", "definisi", "artinya"],
                "handler": "handle_dictionary_query"
            },
            
            # Portfolio queries
            "portfolio": {
                "patterns": ["portfolio", "status", "performance", "kinerja", "saldo"],
                "handler": "handle_portfolio_query"
            },
            
            # Signal explanation
            "signal": {
                "patterns": ["kenapa bot", "mengapa bot", "signal terakhir", "keputusan"],
                "handler": "handle_signal_query"
            },
            
            # Market analysis
            "analysis": {
                "patterns": ["analisis", "bagaimana", "market", "harga"],
                "handler": "handle_analysis_query"
            },
            
            # Risk management
            "risk": {
                "patterns": ["risiko", "risk", "stop loss", "take profit", "safety"],
                "response": "🛡️  RISK MANAGEMENT BOT:\n\n"
                           "Bot menggunakan risk management ketat:\n\n"
                           "• Max 2% risiko per trade\n"
                           "• Max 5 posisi terbuka bersamaan\n"
                           "• Max 20% portfolio per posisi\n"
                           "• Daily loss limit 5%\n"
                           "• Min confidence 55% untuk trade\n"
                           "• Stop-loss otomatis (2x ATR)\n"
                           "• Take-profit otomatis (2:1 R:R ratio)\n\n"
                           "Semua ini untuk melindungi portfolio Anda dari kerugian besar!"
            },
            
            # Trading fees
            "fee": {
                "patterns": ["fee", "biaya", "komisi"],
                "response": "💰 TRADING FEE:\n\n"
                           "Bot mensimulasikan fee trading 0.1% per trade (seperti Binance).\n\n"
                           "Fee dihitung 2x:\n"
                           "• Saat entry (buka posisi)\n"
                           "• Saat exit (tutup posisi)\n\n"
                           "Contoh:\n"
                           "Position $1,000 → Fee $1 entry + $1 exit = Total $2\n\n"
                           "Ini membuat simulasi lebih realistis!"
            },
            
            # Paper trading
            "paper": {
                "patterns": ["paper trading", "simulasi", "virtual"],
                "response": "📝 PAPER TRADING:\n\n"
                           "Bot menggunakan paper trading (simulasi) dengan uang virtual.\n\n"
                           "Benefits:\n"
                           "• Belajar tanpa risiko\n"
                           "• Test strategy\n"
                           "• Build confidence\n"
                           "• Understand market\n\n"
                           "Initial balance: $10,000 (virtual)\n\n"
                           "Ini aman untuk belajar! Tidak ada uang asli yang digunakan."
            },
        }

    async def process_message(self, message: str) -> str:
        """
        Process user message dan generate response
        
        Args:
            message: User message
        
        Returns:
            Bot response
        """
        message_lower = message.lower().strip()
        
        # Check patterns
        for category, data in self.patterns.items():
            for pattern in data.get("patterns", []):
                if pattern in message_lower:
                    # If has handler, call it
                    if "handler" in data:
                        handler_name = data["handler"]
                        handler = getattr(self, handler_name, None)
                        if handler:
                            return await handler(message_lower)
                    # Otherwise return static response
                    elif "response" in data:
                        return data["response"]
        
        # Default response
        return self._get_default_response(message)

    async def handle_dictionary_query(self, message: str) -> str:
        """Handle dictionary/term queries"""
        # Extract term from message
        words = message.split()
        
        # Find term after keywords
        keywords = ["apa itu", "jelaskan", "kamus", "definisi", "artinya"]
        term = None
        
        for keyword in keywords:
            if keyword in message:
                parts = message.split(keyword)
                if len(parts) > 1:
                    term = parts[1].strip().replace("?", "").replace(".", "")
                    break
        
        if not term:
            return "Maaf, saya tidak mengerti istilah yang Anda maksud. Coba tanya 'apa itu RSI?' atau 'jelaskan MACD'"
        
        # Search in dictionary
        term_data = self.dictionary.get_term(term)
        
        if term_data:
            return self.dictionary.format_explanation(term_data, level="full")
        else:
            # Try search
            results = self.dictionary.search(term)
            if results:
                lines = [f"🔍 Hasil pencarian untuk '{term}':\n"]
                for result in results[:3]:
                    lines.append(f"• {result['name']}")
                    lines.append(f"  {result['simple']}\n")
                return "\n".join(lines)
            else:
                return f"Maaf, saya tidak menemukan istilah '{term}' dalam kamus. Coba istilah lain atau tanya 'help' untuk bantuan."

    async def handle_portfolio_query(self, message: str) -> str:
        """Handle portfolio queries"""
        # Get portfolio summary
        summary = await self.db.get_portfolio_stats()
        
        lines = []
        lines.append("💼 PORTFOLIO STATUS:")
        lines.append("")
        lines.append(f"📊 Total Trades: {summary.get('total_trades', 0)}")
        lines.append(f"🎯 Win Rate: {summary.get('win_rate', 0):.1f}%")
        lines.append(f"💰 Total P&L: ${summary.get('total_pnl', 0):+,.2f}")
        lines.append(f"📈 Profit Factor: {summary.get('profit_factor', 0):.2f}")
        lines.append(f"📉 Max Loss: ${summary.get('max_loss', 0):,.2f}")
        lines.append("")
        
        if summary.get('total_trades', 0) > 0:
            lines.append(f"✅ Winning Trades: {summary.get('wins', 0)}")
            lines.append(f"❌ Losing Trades: {summary.get('losses', 0)}")
            lines.append(f"💵 Avg Win: ${summary.get('avg_win', 0):,.2f}")
            lines.append(f"💸 Avg Loss: ${summary.get('avg_loss', 0):,.2f}")
        
        return "\n".join(lines)

    async def handle_signal_query(self, message: str) -> str:
        """Handle signal explanation queries"""
        # Get recent trades
        trades = await self.db.get_trade_history(limit=5)
        
        if not trades:
            return "Belum ada trade yang dieksekusi. Bot sedang menganalisis market..."
        
        lines = []
        lines.append("📊 TRADE TERAKHIR:")
        lines.append("")
        
        for i, trade in enumerate(trades[:3], 1):
            symbol = trade.get("symbol", "Unknown")
            action = trade.get("action", "Unknown")
            price = trade.get("price", 0)
            notes = trade.get("notes", "")
            
            lines.append(f"{i}. {symbol} - {action}")
            lines.append(f"   Price: ${price:,.2f}")
            if notes:
                lines.append(f"   Notes: {notes}")
            lines.append("")
        
        lines.append("💡 Untuk penjelasan detail tentang signal tertentu, tanya:")
        lines.append("   'jelaskan signal [symbol]'")
        
        return "\n".join(lines)

    async def handle_analysis_query(self, message: str) -> str:
        """Handle market analysis queries"""
        # Extract symbol from message
        symbols = ["BTC", "ETH", "SOL", "BNB", "XRP"]
        symbol = None
        
        for sym in symbols:
            if sym in message.upper():
                symbol = f"{sym}/USDT"
                break
        
        if not symbol:
            return "Symbol mana yang ingin Anda analisis? (BTC, ETH, SOL, BNB, XRP)"
        
        # Build context
        context = await self.context_builder.build_symbol_context(symbol)
        
        lines = []
        lines.append(f"📈 ANALISIS {symbol}:")
        lines.append("")
        
        if "current_price" in context:
            lines.append(f"💰 Current Price: ${context['current_price']:,.2f}")
        
        if "price_change_24h" in context:
            change = context["price_change_24h"]
            emoji = "🟢" if change >= 0 else "🔴"
            lines.append(f"{emoji} 24h Change: {change:+.2f}%")
        
        if "price_high_24h" in context and "price_low_24h" in context:
            lines.append(f"📊 24h Range: ${context['price_low_24h']:,.2f} - ${context['price_high_24h']:,.2f}")
        
        if "open_positions_count" in context:
            lines.append(f"📂 Open Positions: {context['open_positions_count']}")
        
        lines.append("")
        lines.append("💡 Untuk analisis lengkap, jalankan:")
        lines.append("   python -m analysis.main_analysis")
        
        return "\n".join(lines)

    def _get_default_response(self, message: str) -> str:
        """Get default response for unrecognized messages"""
        return (
            "Maaf, saya tidak mengerti pertanyaan Anda. 😔\n\n"
            "Coba tanya:\n"
            "• 'apa itu RSI?' - untuk penjelasan istilah\n"
            "• 'portfolio' - untuk status portfolio\n"
            "• 'kenapa bot buy?' - untuk penjelasan keputusan\n"
            "• 'help' - untuk bantuan lengkap\n\n"
            "Atau ketik 'help' untuk melihat semua fitur!"
        )

    def get_available_commands(self) -> str:
        """Get list of available commands"""
        lines = []
        lines.append("📚 PERINTAH YANG TERSEDIA:")
        lines.append("")
        lines.append("1️⃣  Kamus Istilah:")
        lines.append("   • 'apa itu [istilah]'")
        lines.append("   • 'jelaskan [istilah]'")
        lines.append("   • 'kamus [istilah]'")
        lines.append("")
        lines.append("2️⃣  Portfolio:")
        lines.append("   • 'portfolio'")
        lines.append("   • 'status'")
        lines.append("   • 'performance'")
        lines.append("")
        lines.append("3️⃣  Analisis:")
        lines.append("   • 'analisis [symbol]'")
        lines.append("   • 'bagaimana [symbol]?'")
        lines.append("")
        lines.append("4️⃣  Signal:")
        lines.append("   • 'kenapa bot buy?'")
        lines.append("   • 'signal terakhir'")
        lines.append("")
        lines.append("5️⃣  Bantuan:")
        lines.append("   • 'help'")
        lines.append("   • 'bantuan'")
        
        return "\n".join(lines)
