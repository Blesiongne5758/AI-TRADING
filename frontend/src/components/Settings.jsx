import { useState } from 'react';
import { Save } from 'lucide-react';

export default function Settings() {
  const [settings, setSettings] = useState({
    maxRiskPerTrade: 2.0,
    maxOpenPositions: 5,
    maxPositionSize: 20.0,
    maxDailyLoss: 5.0,
    minConfidence: 55.0,
    tradingFee: 0.1,
  });

  const handleChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: parseFloat(value) }));
  };

  const handleSave = () => {
    // TODO: Save to backend
    alert('Settings saved! (TODO: implement backend save)');
  };

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-white mb-8">Settings</h1>

      <div className="bg-slate-800 rounded-lg p-6 max-w-2xl">
        <h2 className="text-xl font-bold text-white mb-6">Risk Management</h2>

        <div className="space-y-6">
          <SettingInput
            label="Max Risk Per Trade (%)"
            value={settings.maxRiskPerTrade}
            onChange={(v) => handleChange('maxRiskPerTrade', v)}
            min={0.5}
            max={10}
            step={0.5}
            description="Persentase maksimal risiko dari total portfolio per trade"
          />

          <SettingInput
            label="Max Open Positions"
            value={settings.maxOpenPositions}
            onChange={(v) => handleChange('maxOpenPositions', v)}
            min={1}
            max={20}
            step={1}
            description="Jumlah maksimal posisi terbuka bersamaan"
          />

          <SettingInput
            label="Max Position Size (%)"
            value={settings.maxPositionSize}
            onChange={(v) => handleChange('maxPositionSize', v)}
            min={5}
            max={50}
            step={5}
            description="Persentase maksimal portfolio untuk satu posisi"
          />

          <SettingInput
            label="Max Daily Loss (%)"
            value={settings.maxDailyLoss}
            onChange={(v) => handleChange('maxDailyLoss', v)}
            min={1}
            max={20}
            step={1}
            description="Stop trading jika loss harian melebihi persentase ini"
          />

          <SettingInput
            label="Min Confidence Threshold (%)"
            value={settings.minConfidence}
            onChange={(v) => handleChange('minConfidence', v)}
            min={40}
            max={90}
            step={5}
            description="Confidence minimal untuk eksekusi trade"
          />

          <SettingInput
            label="Trading Fee (%)"
            value={settings.tradingFee}
            onChange={(v) => handleChange('tradingFee', v)}
            min={0}
            max={1}
            step={0.01}
            description="Fee simulasi per trade (seperti Binance 0.1%)"
          />
        </div>

        <button
          onClick={handleSave}
          className="mt-8 flex items-center gap-2 px-6 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600"
        >
          <Save className="w-5 h-5" />
          Save Settings
        </button>
      </div>
    </div>
  );
}

function SettingInput({ label, value, onChange, min, max, step, description }) {
  return (
    <div>
      <label className="block text-white font-medium mb-2">{label}</label>
      <input
        type="number"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        min={min}
        max={max}
        step={step}
        className="w-full bg-slate-900 text-white px-4 py-2 rounded-lg border border-slate-700 focus:outline-none focus:border-primary-500"
      />
      <p className="text-slate-400 text-sm mt-1">{description}</p>
    </div>
  );
}
