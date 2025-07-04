import React, { useState } from 'react';
import { FaBars } from 'react-icons/fa';

import ChatBox from './components/ChatBox';
import ContextViewer from './components/ContextViewer';

import HealthCheck from './components/HealthCheck';
import Sidebar from './components/Sidebar';

export default function App() {
  const [activeMenu, setActiveMenu] = useState<string>('health');
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(false);

  const renderActivePanel = () => {
    switch (activeMenu) {
      case 'health': return <HealthCheck />;
      case 'context': return <ContextViewer />;
      default: return null;
    }
  };

  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-gray-100 text-gray-800">
      {/* Header - mobile only */}
      <header className="w-full p-4 bg-white shadow-md flex items-center justify-between fixed top-0 z-50 md:hidden">
        <h1 className="text-lg font-semibold text-blue-700">AsaSense</h1>
        <button onClick={() => setSidebarOpen(!sidebarOpen)} className="text-blue-600">
          <FaBars size={24} />
        </button>
      </header>

      {/* Sidebar modularizado */}
      <Sidebar
        activeMenu={activeMenu}
        setActiveMenu={setActiveMenu}
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
      />

      {/* Main content */}
      <main className="flex-1 mt-20 md:mt-0 p-4 md:p-8 ml-0 md:ml-0 overflow-y-auto space-y-6">
        <div className="text-center">
          <h1 className="text-2xl md:text-3xl font-bold text-blue-800">AsaSense API Frontend</h1>
          <p className="text-sm text-gray-500 mt-1">Interface elegante para integração com API</p>
        </div>
        <div className="bg-white shadow rounded-lg p-6">{renderActivePanel()}</div>
        <ChatBox />
      </main>
    </div>
  );
}
