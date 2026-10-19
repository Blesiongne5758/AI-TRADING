import { HashRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import ChartPage from './pages/ChartPage';
import LogPage from './pages/LogPage';
import EducationPage from './pages/EducationPage';
import SettingsPage from './pages/SettingsPage';
import SystemStatus from './pages/SystemStatus';

export default function App() {
  return (
    <HashRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/chart" element={<ChartPage />} />
          <Route path="/log" element={<LogPage />} />
          <Route path="/education" element={<EducationPage />} />
          <Route path="/system" element={<SystemStatus />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </Layout>
    </HashRouter>
  );
}
