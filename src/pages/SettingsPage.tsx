import { useState } from 'react';
import {
  Settings as SettingsIcon,
  Bell,
  Shield,
  TrendingUp,
  Save,
  CheckCircle2,
  Info,
} from 'lucide-react';

export default function SettingsPage() {
  const [saved, setSaved] = useState(false);
  const [settings, setSettings] = useState({
    // Trading symbols
    symbols: { BTC: true, ETH: true, SOL: true, AVAX: true, ADA: false, LINK: false },
    // Timeframes
    timeframes: { '5M': false, '15M': true, '1H': true, '4H': true, '1D': true },
    // Risk level
    riskLevel: 'conservative' as 'conservative' | 'moderate' | 'aggressive',
    // Confidence threshold
    confidenceThreshold: 65,
    // Max position size (% of portfolio)
    maxPositionSize: 10,
    // Stop loss %
    stopLossPercent: 2,
    // Take profit %
    takeProfitPercent: 5,
    // Notifications
    telegramNotifications: true,
    signalAlerts: true,
    tradeExecuted: true,
    dailyReport: true,
    // Bot
    botEnabled: true,
    autoTrade: false,
  });

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const riskConfig = {
    conservative: { riskPerTrade: 1, maxPositions: 3, description: 'Cocok untuk pemula. Risiko rendah per trade.' },
    moderate: { riskPerTrade: 2, maxPositions: 5, description: 'Untuk yang sudah berpengalaman. Balance risk/reward.' },
    aggressive: { riskPerTrade: 3, maxPositions: 8, description: 'High risk, high reward. Hanya untuk trader berpengalaman.' },
  };

  return (
    <div className="space-y-6 animate-fade-in max-w-4xl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Pengaturan</h1>
          <p className="text-sm text-dark-muted mt-1">Konfigurasi bot trading dan preferensi Anda</p>
        </div>
        <button
          onClick={handleSave}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            saved
              ? 'bg-success/10 text-success border border-success/30'
              : 'bg-primary text-white hover:bg-primary-dark'
          }`}
        >
          {saved ? (
            <>
              <CheckCircle2 className="w-4 h-4" />
              Tersimpan!
            </>
          ) : (
            <>
              <Save className="w-4 h-4" />
              Simpan Pengaturan
            </>
          )}
        </button>
      </div>

      {/* Bot Status */}
      <div className="bg-dark-card rounded-xl border border-dark-border p-5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center">
              <SettingsIcon className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-white">Bot Status</h3>
              <p className="text-xs text-dark-muted">Aktifkan/nonaktifkan bot trading</p>
            </div>
          </div>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={settings.botEnabled}
              onChange={(e) => setSettings({ ...settings, botEnabled: e.target.checked })}
              className="sr-only peer"
            />
            <div className="w-11 h-6 bg-dark-border peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
          </label>
        </div>
        <div className="mt-4 flex items-center gap-3">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={settings.autoTrade}
              onChange={(e) => setSettings({ ...settings, autoTrade: e.target.checked })}
              className="w-4 h-4 rounded border-dark-border bg-dark-bg text-primary focus:ring-primary"
            />
            <span className="text-xs text-dark-muted">Auto-execute trades (Paper Trading only)</span>
          </label>
        </div>
      </div>

      {/* Trading Symbols */}
      <div className="bg-dark-card rounded-xl border border-dark-border p-5">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg bg-success/20 flex items-center justify-center">
            <TrendingUp className="w-5 h-5 text-success" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white">Trading Symbols</h3>
            <p className="text-xs text-dark-muted">Pilih aset crypto yang ingin di-trade</p>
          </div>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {Object.entries(settings.symbols).map(([symbol, enabled]) => (
            <label
              key={symbol}
              className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-colors ${
                enabled ? 'border-primary/50 bg-primary/5' : 'border-dark-border hover:border-dark-muted'
              }`}
            >
              <input
                type="checkbox"
                checked={enabled}
                onChange={() =>
                  setSettings({
                    ...settings,
                    symbols: { ...settings.symbols, [symbol]: !enabled },
                  })
                }
                className="sr-only"
              />
              <div className={`w-4 h-4 rounded border-2 flex items-center justify-center ${
                enabled ? 'border-primary bg-primary' : 'border-dark-muted'
              }`}>
                {enabled && <CheckCircle2 className="w-3 h-3 text-white" />}
              </div>
              <span className="text-sm font-medium text-white">{symbol}/USDT</span>
            </label>
          ))}
        </div>
      </div>

      {/* Timeframes */}
      <div className="bg-dark-card rounded-xl border border-dark-border p-5">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg bg-warning/20 flex items-center justify-center">
            <Info className="w-5 h-5 text-warning" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white">Timeframes</h3>
            <p className="text-xs text-dark-muted">Pilih interval waktu untuk analisis</p>
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          {Object.entries(settings.timeframes).map(([tf, enabled]) => (
            <button
              key={tf}
              onClick={() =>
                setSettings({
                  ...settings,
                  timeframes: { ...settings.timeframes, [tf]: !enabled },
                })
              }
              className={`px-4 py-2 rounded-lg text-sm font-medium border transition-colors ${
                enabled
                  ? 'border-primary/50 bg-primary/10 text-primary'
                  : 'border-dark-border text-dark-muted hover:border-dark-muted'
              }`}
            >
              {tf}
            </button>
          ))}
        </div>
      </div>

      {/* Risk Level */}
      <div className="bg-dark-card rounded-xl border border-dark-border p-5">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg bg-danger/20 flex items-center justify-center">
            <Shield className="w-5 h-5 text-danger" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white">Risk Level</h3>
            <p className="text-xs text-dark-muted">Atur tingkat risiko sesuai pengalaman Anda</p>
          </div>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {(['conservative', 'moderate', 'aggressive'] as const).map((level) => (
            <button
              key={level}
              onClick={() => setSettings({ ...settings, riskLevel: level })}
              className={`p-4 rounded-lg border text-left transition-all ${
                settings.riskLevel === level
                  ? level === 'conservative'
                    ? 'border-success/50 bg-success/5'
                    : level === 'moderate'
                    ? 'border-warning/50 bg-warning/5'
                    : 'border-danger/50 bg-danger/5'
                  : 'border-dark-border hover:border-dark-muted'
              }`}
            >
              <p className={`text-sm font-semibold capitalize ${
                level === 'conservative' ? 'text-success' : level === 'moderate' ? 'text-warning' : 'text-danger'
              }`}>
                {level}
              </p>
              <p className="text-xs text-dark-muted mt-1">{riskConfig[level].description}</p>
              <div className="mt-2 flex items-center gap-2 text-xs text-dark-muted">
                <span>Risk/trade: {riskConfig[level].riskPerTrade}%</span>
                <span>•</span>
                <span>Max positions: {riskConfig[level].maxPositions}</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Trading Parameters */}
      <div className="bg-dark-card rounded-xl border border-dark-border p-5">
        <h3 className="text-sm font-semibold text-white mb-4">Trading Parameters</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="text-xs text-dark-muted mb-1.5 block">Min. Confidence Threshold: {settings.confidenceThreshold}%</label>
            <input
              type="range"
              min={50}
              max={90}
              value={settings.confidenceThreshold}
              onChange={(e) => setSettings({ ...settings, confidenceThreshold: Number(e.target.value) })}
              className="w-full h-1.5 bg-dark-border rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary"
            />
            <div className="flex justify-between text-xs text-dark-muted mt-1">
              <span>50% (lebih banyak trade)</span>
              <span>90% (lebih selektif)</span>
            </div>
          </div>
          <div>
            <label className="text-xs text-dark-muted mb-1.5 block">Max Position Size: {settings.maxPositionSize}% of portfolio</label>
            <input
              type="range"
              min={5}
              max={25}
              value={settings.maxPositionSize}
              onChange={(e) => setSettings({ ...settings, maxPositionSize: Number(e.target.value) })}
              className="w-full h-1.5 bg-dark-border rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary"
            />
            <div className="flex justify-between text-xs text-dark-muted mt-1">
              <span>5%</span>
              <span>25%</span>
            </div>
          </div>
          <div>
            <label className="text-xs text-dark-muted mb-1.5 block">Stop Loss: {settings.stopLossPercent}%</label>
            <input
              type="range"
              min={1}
              max={5}
              step={0.5}
              value={settings.stopLossPercent}
              onChange={(e) => setSettings({ ...settings, stopLossPercent: Number(e.target.value) })}
              className="w-full h-1.5 bg-dark-border rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-danger"
            />
          </div>
          <div>
            <label className="text-xs text-dark-muted mb-1.5 block">Take Profit: {settings.takeProfitPercent}%</label>
            <input
              type="range"
              min={2}
              max={15}
              step={0.5}
              value={settings.takeProfitPercent}
              onChange={(e) => setSettings({ ...settings, takeProfitPercent: Number(e.target.value) })}
              className="w-full h-1.5 bg-dark-border rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-success"
            />
          </div>
        </div>
      </div>

      {/* Notifications */}
      <div className="bg-dark-card rounded-xl border border-dark-border p-5">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center">
            <Bell className="w-5 h-5 text-blue-400" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white">Notifikasi (Telegram)</h3>
            <p className="text-xs text-dark-muted">Atur notifikasi yang ingin Anda terima</p>
          </div>
        </div>
        <div className="space-y-3">
          {[
            { key: 'telegramNotifications', label: 'Telegram Bot Active', desc: 'Terima notifikasi via Telegram' },
            { key: 'signalAlerts', label: 'Signal Alerts', desc: 'Notifikasi saat bot menghasilkan sinyal baru' },
            { key: 'tradeExecuted', label: 'Trade Executed', desc: 'Notifikasi saat trade dieksekusi' },
            { key: 'dailyReport', label: 'Daily Report', desc: 'Laporan performa harian' },
          ].map((item) => (
            <div key={item.key} className="flex items-center justify-between py-2">
              <div>
                <p className="text-sm text-white">{item.label}</p>
                <p className="text-xs text-dark-muted">{item.desc}</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings[item.key as keyof typeof settings] as boolean}
                  onChange={(e) =>
                    setSettings({ ...settings, [item.key]: e.target.checked })
                  }
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-dark-border peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
              </label>
            </div>
          ))}
        </div>
      </div>

      {/* Save Button Bottom */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          className={`flex items-center gap-2 px-6 py-2.5 rounded-lg text-sm font-medium transition-all ${
            saved
              ? 'bg-success/10 text-success border border-success/30'
              : 'bg-primary text-white hover:bg-primary-dark'
          }`}
        >
          {saved ? (
            <>
              <CheckCircle2 className="w-4 h-4" />
              Pengaturan Tersimpan!
            </>
          ) : (
            <>
              <Save className="w-4 h-4" />
              Simpan Semua Pengaturan
            </>
          )}
        </button>
      </div>
    </div>
  );
}
