import { useState } from 'react';
import { Save, RotateCcw } from 'lucide-react';

export default function Settings() {
  const [settings, setSettings] = useState({
    // Trading Settings
    initialBalance: 10000,
    maxRiskPerTrade: 2,
    maxOpenPositions: 5,
    stopLossPercent: 2,
    takeProfitPercent: 4,
    
    // Analysis Settings
    minConfidence: 55,
    rsiPeriod: 14,
    macdFast: 12,
    macdSlow: 26,
    macdSignal: 9,
    
    // Notification Settings
    enableNotifications: true,
    enableSound: false,
    enableEmail: false,
    
    // Display Settings
    theme: 'dark',
    language: 'id',
    timezone: 'Asia/Jakarta',
  });

  const [saved, setSaved] = useState(false);

  const handleChange = (key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value,
    }));
    setSaved(false);
  };

  const handleSave = () => {
    // TODO: Save to backend API
    console.log('Saving settings:', settings);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const handleReset = () => {
    setSettings({
      initialBalance: 10000,
      maxRiskPerTrade: 2,
      maxOpenPositions: 5,
      stopLossPercent: 2,
      takeProfitPercent: 4,
      minConfidence: 55,
      rsiPeriod: 14,
      macdFast: 12,
      macdSlow: 26,
      macdSignal: 9,
      enableNotifications: true,
      enableSound: false,
      enableEmail: false,
      theme: 'dark',
      language: 'id',
      timezone: 'Asia/Jakarta',
    });
    setSaved(false);
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Settings</h1>
          <p className="text-slate-400 mt-1">Configure your trading preferences</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={handleReset}
            className="flex items-center gap-2 px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white hover:bg-slate-700 transition-colors"
          >
            <RotateCcw className="w-4 h-4" />
            Reset
          </button>
          <button
            onClick={handleSave}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-white transition-colors ${
              saved
                ? 'bg-green-600 hover:bg-green-700'
                : 'bg-primary-600 hover:bg-primary-700'
            }`}
          >
            <Save className="w-4 h-4" />
            {saved ? 'Saved!' : 'Save'}
          </button>
        </div>
      </div>

      {/* Trading Settings */}
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
        <h2 className="text-xl font-bold text-white mb-4">Trading Settings</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">
              Initial Balance ($)
            </label>
            <input
              type="number"
              value={settings.initialBalance}
              onChange={(e) => handleChange('initialBalance', Number(e.target.value))}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-600"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">
              Max Risk per Trade (%)
            </label>
            <input
              type="number"
              value={settings.maxRiskPerTrade}
              onChange={(e) => handleChange('maxRiskPerTrade', Number(e.target.value))}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-600"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">
              Max Open Positions
            </label>
            <input
              type="number"
              value={settings.maxOpenPositions}
              onChange={(e) => handleChange('maxOpenPositions', Number(e.target.value))}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-600"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">
              Stop Loss (%)
            </label>
            <input
              type="number"
              value={settings.stopLossPercent}
              onChange={(e) => handleChange('stopLossPercent', Number(e.target.value))}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-600"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">
              Take Profit (%)
            </label>
            <input
              type="number"
              value={settings.takeProfitPercent}
              onChange={(e) => handleChange('takeProfitPercent', Number(e.target.value))}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-600"
            />
          </div>
        </div>
      </div>

      {/* Analysis Settings */}
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
        <h2 className="text-xl font-bold text-white mb-4">Analysis Settings</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">
              Min Confidence (%)
            </label>
            <input
              type="number"
              value={settings.minConfidence}
              onChange={(e) => handleChange('minConfidence', Number(e.target.value))}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-600"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">
              RSI Period
            </label>
            <input
              type="number"
              value={settings.rsiPeriod}
              onChange={(e) => handleChange('rsiPeriod', Number(e.target.value))}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-600"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">
              MACD Fast
            </label>
            <input
              type="number"
              value={settings.macdFast}
              onChange={(e) => handleChange('macdFast', Number(e.target.value))}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-600"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">
              MACD Slow
            </label>
            <input
              type="number"
              value={settings.macdSlow}
              onChange={(e) => handleChange('macdSlow', Number(e.target.value))}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-600"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">
              MACD Signal
            </label>
            <input
              type="number"
              value={settings.macdSignal}
              onChange={(e) => handleChange('macdSignal', Number(e.target.value))}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-600"
            />
          </div>
        </div>
      </div>

      {/* Notification Settings */}
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
        <h2 className="text-xl font-bold text-white mb-4">Notification Settings</h2>
        <div className="space-y-3">
          <label className="flex items-center justify-between">
            <span className="text-white">Enable Notifications</span>
            <input
              type="checkbox"
              checked={settings.enableNotifications}
              onChange={(e) => handleChange('enableNotifications', e.target.checked)}
              className="w-5 h-5 rounded border-slate-700 bg-slate-900 text-primary-600 focus:ring-primary-600"
            />
          </label>
          <label className="flex items-center justify-between">
            <span className="text-white">Enable Sound</span>
            <input
              type="checkbox"
              checked={settings.enableSound}
              onChange={(e) => handleChange('enableSound', e.target.checked)}
              className="w-5 h-5 rounded border-slate-700 bg-slate-900 text-primary-600 focus:ring-primary-600"
            />
          </label>
          <label className="flex items-center justify-between">
            <span className="text-white">Enable Email Alerts</span>
            <input
              type="checkbox"
              checked={settings.enableEmail}
              onChange={(e) => handleChange('enableEmail', e.target.checked)}
              className="w-5 h-5 rounded border-slate-700 bg-slate-900 text-primary-600 focus:ring-primary-600"
            />
          </label>
        </div>
      </div>

      {/* Display Settings */}
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
        <h2 className="text-xl font-bold text-white mb-4">Display Settings</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">
              Theme
            </label>
            <select
              value={settings.theme}
              onChange={(e) => handleChange('theme', e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-600"
            >
              <option value="dark">Dark</option>
              <option value="light">Light</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">
              Language
            </label>
            <select
              value={settings.language}
              onChange={(e) => handleChange('language', e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-600"
            >
              <option value="id">Bahasa Indonesia</option>
              <option value="en">English</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">
              Timezone
            </label>
            <select
              value={settings.timezone}
              onChange={(e) => handleChange('timezone', e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary-600"
            >
              <option value="Asia/Jakarta">Asia/Jakarta (WIB)</option>
              <option value="Asia/Makassar">Asia/Makassar (WITA)</option>
              <option value="Asia/Jayapura">Asia/Jayapura (WIT)</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
}
