"""
Trading Dictionary
Kamus lengkap istilah trading untuk edukasi pemula
"""
from typing import Dict, List


class TradingDictionary:
    """Kamus istilah trading dengan penjelasan ramah pemula"""

    def __init__(self):
        self.terms = self._build_dictionary()

    def _build_dictionary(self) -> Dict[str, Dict]:
        """Membangun kamus lengkap"""
        return {
            # === INDICATORS ===
            "rsi": {
                "name": "RSI (Relative Strength Index)",
                "category": "indicator",
                "simple": "Indikator yang mengukur apakah harga sudah 'terlalu mahal' (overbought) atau 'terlalu murah' (oversold). Skala 0-100.",
                "detailed": "RSI membandingkan kekuatan kenaikan vs penurunan harga dalam periode tertentu (biasanya 14 candle). RSI > 70 = overbought (potensi turun), RSI < 30 = oversold (potensi naik).",
                "analogy": "Bayangkan seperti speedometer mobil. Jika jarum di atas 70, mobil ngebut terlalu kencang dan perlu melambat. Jika di bawah 30, mobil terlalu pelan dan bisa ngebut lagi.",
                "example": "RSI BTC = 28 → BTC oversold, ada potensi rebound.",
            },
            "macd": {
                "name": "MACD (Moving Average Convergence Divergence)",
                "category": "indicator",
                "simple": "Indikator yang menunjukkan momentum tren dan arah pergerakan harga.",
                "detailed": "MACD terdiri dari 3 garis: MACD line (perbedaan EMA 12 & 26), Signal line (EMA 9 dari MACD), dan Histogram (perbedaan MACD & Signal). Crossover histogram dari negatif ke positif = sinyal beli.",
                "analogy": "Seperti melihat apakah mobil sedang加速 (accelerate) atau melambat. Histogram positif = mobil ngebut, negatif = melambat.",
                "example": "MACD histogram crossover ke positif → momentum beli meningkat.",
            },
            "ema": {
                "name": "EMA (Exponential Moving Average)",
                "category": "indicator",
                "simple": "Rata-rata harga yang memberi bobot lebih pada data terbaru, sehingga lebih responsif terhadap perubahan harga.",
                "detailed": "EMA 20 = rata-rata 20 candle terakhir dengan bobot lebih pada harga baru. EMA 50 & 200 untuk tren jangka menengah & panjang. Jika harga > EMA 200 = uptrend jangka panjang.",
                "analogy": "Seperti garis tren yang mulus di tengah fluktuasi harga. Harga di atas garis = tren naik, di bawah = tren turun.",
                "example": "Harga BTC > EMA 20 > EMA 50 > EMA 200 → uptrend kuat di semua timeframe.",
            },
            "bollinger": {
                "name": "Bollinger Bands",
                "category": "indicator",
                "simple": "Tiga garis yang mengapit harga: middle (SMA 20), upper, dan lower band. Menunjukkan volatilitas.",
                "detailed": "Harga yang menyentuh upper band = overbought, lower band = oversold. Band yang menyempit = volatilitas rendah (potensi breakout), melebar = volatilitas tinggi.",
                "analogy": "Seperti jalan raya dengan 3 lajur. Mobil (harga) biasanya di lajur tengah. Jika keluar lajur atas/bawah, biasanya akan kembali ke tengah.",
                "example": "Harga menyentuh lower band → potensi bounce ke middle band.",
            },
            "atr": {
                "name": "ATR (Average True Range)",
                "category": "indicator",
                "simple": "Mengukur volatilitas pasar - seberapa besar harga bergerak rata-rata per hari.",
                "detailed": "ATR digunakan untuk menentukan jarak stop-loss yang realistis. ATR tinggi = pasar volatil, ATR rendah = pasar tenang. Biasanya SL = 2x ATR dari entry.",
                "analogy": "Seperti mengukur ombak di laut. Ombak besar (ATR tinggi) = perlu perahu besar (SL lebar). Ombak kecil (ATR rendah) = perahu kecil cukup (SL sempit).",
                "example": "ATR BTC = $1,500 → Stop-loss ideal = 2 x $1,500 = $3,000 dari entry.",
            },
            "volume": {
                "name": "Volume",
                "category": "indicator",
                "simple": "Jumlah aset yang diperdagangkan dalam periode tertentu. Volume tinggi = banyak aktivitas, konfirmasi sinyal kuat.",
                "detailed": "Volume mengkonfirmasi kekuatan pergerakan harga. Kenaikan harga + volume tinggi = uptrend kuat. Kenaikan harga + volume rendah = potensi fakeout.",
                "analogy": "Seperti suara tepuk tangan. Tepuk ramai (volume tinggi) = pertunjukan bagus (tren kuat). Tepuk sepi (volume rendah) = kurang meyakinkan.",
                "example": "Volume 2x rata-rata → konfirmasi sinyal beli sangat kuat.",
            },
            
            # === TRADING CONCEPTS ===
            "long": {
                "name": "Long Position",
                "category": "concept",
                "simple": "Membeli aset dengan harapan harga akan NAIK.",
                "detailed": "Anda beli di harga rendah, jual di harga tinggi. Profit = harga jual - harga beli. Ini posisi paling umum di pasar spot.",
                "analogy": "Seperti beli rumah murah, tunggu harga naik, lalu jual mahal.",
                "example": "Buy BTC @ $60,000, sell @ $70,000 → profit $10,000.",
            },
            "short": {
                "name": "Short Position",
                "category": "concept",
                "simple": "Bertaruh harga akan TURUN. Jual dulu (pinjam), beli kembali nanti di harga lebih rendah.",
                "detailed": "Di pasar futures, Anda bisa 'jual' tanpa punya aset. Profit jika harga turun. Risiko tidak terbatas jika harga naik tak terkendali.",
                "analogy": "Pinjam iPhone teman seharga $1,000, jual ke orang lain $1,000. Minggu depan harga iPhone turun jadi $800, beli baru, kembalikan ke teman. Profit $200.",
                "example": "Short ETH @ $3,500, cover @ $3,000 → profit $500.",
            },
            "stop_loss": {
                "name": "Stop-Loss (SL)",
                "category": "concept",
                "simple": "Order otomatis untuk MEMBATASI KERUGIAN jika harga bergerak berlawanan prediksi.",
                "detailed": "Wajib dipasang di setiap trade. Biasanya 2x ATR dari entry. Jika harga menyentuh level SL, posisi otomatis ditutup untuk mencegah loss lebih besar.",
                "analogy": "Seperti rem darurat di mobil. Jika mobil meluncur tak terkendali, rem otomatis aktif sebelum terjadi kecelakaan fatal.",
                "example": "Buy BTC @ $67,000, SL @ $65,000 → max loss $2,000 jika harga turun.",
            },
            "take_profit": {
                "name": "Take-Profit (TP)",
                "category": "concept",
                "simple": "Order otomatis untuk MENGAMANKAN PROFIT saat harga mencapai target.",
                "detailed": "Target profit biasanya 2x jarak stop-loss (risk/reward 1:2). Jika harga menyentuh TP, posisi ditutup dan profit masuk ke saldo.",
                "analogy": "Seperti target skor dalam game. Begitu skor tercapai, level selesai dan Anda dapat reward.",
                "example": "Buy BTC @ $67,000, TP @ $71,000 → profit $4,000 otomatis diamankan.",
            },
            "confidence": {
                "name": "Confidence Score",
                "category": "concept",
                "simple": "Seberapa yakin AI dengan keputusannya. Skala 0-100%. Semakin tinggi = semakin banyak indikator yang sejalan.",
                "detailed": "Confidence dihitung dari bobot setiap indikator. Jika RSI, MACD, EMA, dan sentimen semua bullish → confidence tinggi. Jika hanya 1-2 indikator → confidence rendah.",
                "analogy": "Seperti voting di kelas. Jika 9 dari 10 teman bilang jawaban A benar → confidence 90%. Jika hanya 5 dari 10 → confidence 50% (ragu).",
                "example": "Confidence 85% → 85% indikator mendukung sinyal beli.",
            },
            "drawdown": {
                "name": "Drawdown",
                "category": "concept",
                "simple": "Penurunan saldo dari titik tertinggi (peak). Mengukur seberapa besar kerugian maksimum.",
                "detailed": "Jika saldo peak $12,000 lalu turun ke $10,000 → drawdown 16.7%. Max drawdown = kerugian terburuk yang pernah dialami. Trader profesional biasanya max drawdown < 20%.",
                "analogy": "Seperti mendaki gunung lalu turun ke lembah. Drawdown = seberapa dalam Anda turun dari puncak.",
                "example": "Peak $12,000 → current $10,800 → drawdown 10%.",
            },
            "position_sizing": {
                "name": "Position Sizing",
                "category": "concept",
                "simple": "Menentukan berapa banyak uang yang dipertaruhkan di satu trade. Aturan umum: max 2% risiko per trade.",
                "detailed": "Jika saldo $10,000 dan max risk 2% = max loss $200 per trade. Jika SL distance 5%, maka position size = $200/5% = $4,000 (40% dari saldo).",
                "analogy": "Seperti bertaruh di poker. Jangan all-in di satu tangan. Bet kecil untuk bertahan lama, bet besar hanya jika sangat yakin.",
                "example": "Saldo $10,000, risk 2% → max loss $200 → position size disesuaikan.",
            },
            "risk_reward_ratio": {
                "name": "Risk/Reward Ratio (RR)",
                "category": "concept",
                "simple": "Perbandingan antara potensi kerugian vs potensi keuntungan. Idealnya minimal 1:2.",
                "detailed": "Jika SL = $100 dan TP = $200 → RR = 1:2. Artinya Anda rela rugi $100 untuk potensi untung $200. Dengan RR 1:2, Anda bisa salah 50% masih profit.",
                "analogy": "Seperti investasi waktu. Rela belajar 1 jam (risiko) untuk dapat ilmu yang berguna seumur hidup (reward).",
                "example": "SL $500, TP $1,000 → RR 1:2. Worth it!",
            },
            "win_rate": {
                "name": "Win Rate",
                "category": "concept",
                "simple": "Persentase trade yang profit dari total trade. Win rate 60% = 6 dari 10 trade profit.",
                "detailed": "Win rate tinggi tidak selalu berarti profit. Jika win rate 90% tapi profit kecil-kecil dan loss besar-besar, tetap rugi. Yang penting adalah profit factor (avg win / avg loss).",
                "analogy": "Seperti basket. Shoot 10 kali masuk 6 (60% win rate). Tapi kalau yang masuk 2 poin, yang miss 3 poin (free throw), tetap rugi.",
                "example": "100 trades, 60 win, 40 loss → win rate 60%.",
            },
            "profit_factor": {
                "name": "Profit Factor",
                "category": "concept",
                "simple": "Rasio total profit vs total loss. Profit factor > 1 = sistem profit, < 1 = sistem loss.",
                "detailed": "Profit Factor = (Avg Win × Win Rate) / (Avg Loss × Loss Rate). PF 2.0 = setiap $1 yang rugi, sistem menghasilkan $2 profit. PF ideal > 1.5.",
                "analogy": "Seperti mesin penjual. Setiap $1 yang dimasukkan, keluar $2. Mesin bagus!",
                "example": "Avg win $200, avg loss $100, WR 50% → PF = 2.0.",
            },
            "slippage": {
                "name": "Slippage",
                "category": "concept",
                "simple": "Perbedaan antara harga yang diharapkan vs harga eksekusi aktual. Terjadi karena volatilitas atau likuiditas rendah.",
                "detailed": "Di market volatile (seperti crypto), slippage bisa signifikan. Order di harga $100 bisa ter-eksekusi di $100.50. Slippage tinggi = likuiditas rendah.",
                "analogy": "Seperti pesan makanan di aplikasi. Harga tertera $10, tapi saat checkout jadi $10.50 karena biaya tambahan.",
                "example": "Expected entry $67,000, actual $67,050 → slippage $50.",
            },
            
            # === MARKET TERMS ===
            "bullish": {
                "name": "Bullish",
                "category": "market",
                "simple": "Pasar atau aset diperkirakan akan NAIK. Optimis.",
                "detailed": "Istilah dari gerakan banteng (bull) yang menyeruduk ke atas. Bullish market = tren naik berkepanjangan. Bullish signal = indikator mendukung kenaikan.",
                "analogy": "Seperti musim semi - semua tumbuh, optimis, harga naik.",
                "example": "Sentimen berita positif → pasar bullish.",
            },
            "bearish": {
                "name": "Bearish",
                "category": "market",
                "simple": "Pasar atau aset diperkirakan akan TURUN. Pesimis.",
                "detailed": "Istilah dari gerakan beruang (bear) yang mencakar ke bawah. Bearish market = tren turun (bear market). Bearish signal = indikator mendukung penurunan.",
                "analogy": "Seperti musim dingin - semua layu, pesimis, harga turun.",
                "example": "Regulasi ketat → pasar bearish.",
            },
            "breakout": {
                "name": "Breakout",
                "category": "market",
                "simple": "Harga menembus level resistance/support penting dengan volume tinggi.",
                "detailed": "Breakout di atas resistance = sinyal beli kuat. Breakout di bawah support = sinyal jual kuat. Harus dikonfirmasi dengan volume tinggi agar tidak fakeout.",
                "analogy": "Seperti pelari yang menembus garis finish. Butuh tenaga besar (volume) untuk benar-benar breakthrough.",
                "example": "BTC break above $70,000 resistance dengan volume 2x → breakout valid.",
            },
            "fakeout": {
                "name": "Fakeout (False Breakout)",
                "category": "market",
                "simple": "Harga seolah menembus level penting, tapi segera berbalik arah. Jebakan.",
                "detailed": "Sering terjadi di market volatile. Trader yang entry saat fakeout akan rugi. Solusi: tunggu konfirmasi (close candle di luar level, volume tinggi).",
                "analogy": "Seperti hantu yang muncul tiba-tiba lalu menghilang. Kaget tapi tidak nyata.",
                "example": "BTC break $70K tapi langsung turun lagi → fakeout, jangan entry!",
            },
            "whale": {
                "name": "Whale (Paus)",
                "category": "market",
                "simple": "Investor/institusi dengan modal sangat besar yang bisa menggerakkan pasar.",
                "detailed": "Di crypto, whale = wallet dengan ribuan BTC atau jutaan USDT. Pergerakan whale sering jadi sinyal bagi trader ritel. Whale buying = bullish, whale selling = bearish.",
                "analogy": "Seperti ikan paus di laut. Gerakannya menciptakan ombak besar yang mempengaruhi ikan-ikan kecil (trader ritel).",
                "example": "Whale memindahkan 5,000 BTC ke exchange → potensi selling, bearish.",
            },
            
            # === STRATEGY TERMS ===
            "scalping": {
                "name": "Scalping",
                "category": "strategy",
                "simple": "Trading sangat cepat (detik-menit) untuk profit kecil tapi sering.",
                "detailed": "Scalper masuk-keluar pasar dalam hitungan detik/menit. Butuh fokus tinggi, fee rendah, dan eksekusi cepat. Profit per trade kecil (0.1-0.5%) tapi volume trade tinggi.",
                "analogy": "Seperti mengambil receh di jalanan. Satu-satu kecil, tapi kalau banyak jadi lumayan.",
                "example": "Scalping BTC 100 trades/hari, profit 0.2% per trade → total 20% sehari.",
            },
            "swing_trading": {
                "name": "Swing Trading",
                "category": "strategy",
                "simple": "Trading jangka menengah (hari-minggu) menangkap 'ayunan' harga.",
                "detailed": "Swing trader hold posisi beberapa hari hingga minggu. Target profit 5-20% per trade. Lebih santai daripada scalping, cocok untuk yang punya pekerjaan lain.",
                "analogy": "Seperti peselancar yang menunggu ombak besar. Sabar, lalu surf satu ombak panjang.",
                "example": "Buy BTC di support, hold 5 hari, sell di resistance → profit 8%.",
            },
            "dyor": {
                "name": "DYOR (Do Your Own Research)",
                "category": "strategy",
                "simple": "Lakukan riset mandiri. Jangan percaya 100% pada siapapun, termasuk AI ini!",
                "detailed": "Prinsip paling penting di trading. AI bisa salah, influencer bisa bias, berita bisa hoax. Selalu verifikasi dari banyak sumber sebelum mengambil keputusan.",
                "analogy": "Seperti sebelum beli rumah, Anda survei lokasi, cek sertifikat, tanya tetangga. Jangan cuma lihat foto!",
                "example": "AI bilang BUY, tapi Anda riset sendiri dan menemukan berita negatif → jangan ikuti AI!",
            },
        }

    def search(self, query: str) -> List[Dict]:
        """Mencari istilah berdasarkan query"""
        query_lower = query.lower()
        results = []

        for key, data in self.terms.items():
            # Cari di key, name, simple, detailed
            if (
                query_lower in key
                or query_lower in data["name"].lower()
                or query_lower in data["simple"].lower()
                or query_lower in data["detailed"].lower()
            ):
                results.append({"key": key, **data})

        return results

    def get_term(self, key: str) -> Dict:
        """Mengambil detail satu istilah"""
        return self.terms.get(key.lower())

    def get_by_category(self, category: str) -> List[Dict]:
        """Mengambil semua istilah dalam kategori"""
        return [
            {"key": k, **v}
            for k, v in self.terms.items()
            if v["category"] == category
        ]

    def format_explanation(self, term: Dict, level: str = "simple") -> str:
        """Format penjelasan istilah"""
        if level == "simple":
            return f"**{term['name']}**\n\n{term['simple']}"
        elif level == "detailed":
            return f"**{term['name']}**\n\n{term['detailed']}"
        elif level == "analogy":
            return f"**{term['name']}** - Analogi:\n\n🎯 {term['analogy']}"
        elif level == "example":
            return f"**{term['name']}** - Contoh:\n\n💡 {term['example']}"
        else:  # full
            return (
                f"**{term['name']}**\n\n"
                f"📖 {term['simple']}\n\n"
                f"🔍 {term['detailed']}\n\n"
                f"🎯 Analogi: {term['analogy']}\n\n"
                f"💡 Contoh: {term['example']}"
            )
