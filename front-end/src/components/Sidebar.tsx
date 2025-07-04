import React from 'react';
import {
  FaHeartbeat,
  FaUser,
  FaHistory,
  FaFileAlt,
  FaCreditCard,
  FaBars,
  FaChevronLeft,
} from 'react-icons/fa';

import SidebarButton from './SidebarButton';
import HealthCheck from './HealthCheck';

interface SidebarProps {
  activeMenu: string;
  setActiveMenu: (menu: string) => void;
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
}

export default function Sidebar({
  activeMenu,
  setActiveMenu,
  sidebarOpen,
  setSidebarOpen,
}: SidebarProps) {
  return (
    <aside
      className={`bg-white shadow-lg flex flex-col pt-20 md:pt-6 px-4 space-y-6 transition-all duration-300
      ${sidebarOpen ? 'w-64' : 'w-20'} fixed md:relative z-40 h-screen`}
    >
      <div className="hidden md:flex justify-end mb-4">
        <button onClick={() => setSidebarOpen(!sidebarOpen)} className="text-blue-600">
          {sidebarOpen ? <FaChevronLeft size={20} /> : <FaBars size={20} />}
        </button>
      </div>

      <div className="flex justify-center">
        <HealthCheck />
      </div>

      <nav className="space-y-2">
        <SidebarButton
          icon={<FaHeartbeat />}
          label="Health Check"
          active={activeMenu === 'health'}
          expanded={sidebarOpen}
          onClick={() => setActiveMenu('health')}
        />
        <SidebarButton
          icon={<FaUser />}
          label="Usuário"
          active={activeMenu === 'user'}
          expanded={sidebarOpen}
          onClick={() => setActiveMenu('user')}
        />
        <SidebarButton
          icon={<FaHistory />}
          label="Histórico"
          active={activeMenu === 'history'}
          expanded={sidebarOpen}
          onClick={() => setActiveMenu('history')}
        />
        <SidebarButton
          icon={<FaFileAlt />}
          label="Contexto"
          active={activeMenu === 'context'}
          expanded={sidebarOpen}
          onClick={() => setActiveMenu('context')}
        />
        <SidebarButton
          icon={<FaCreditCard />}
          label="Transação"
          active={activeMenu === 'transaction'}
          expanded={sidebarOpen}
          onClick={() => setActiveMenu('transaction')}
        />
      </nav>
    </aside>
  );
}
