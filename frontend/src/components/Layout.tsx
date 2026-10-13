import React, { useState } from 'react';
import { NavLink, Outlet, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  GitBranch,
  Network,
  Database,
  ListOrdered,
  DollarSign,
  Compass,
  FlaskConical,
  FileText,
  RotateCcw,
  ShieldAlert,
  Server,
  Activity
} from 'lucide-react';
import { api } from '../services/api';

export const Layout: React.FC = () => {
  const [resetting, setResetting] = useState(false);
  const [resetMessage, setResetMessage] = useState<string | null>(null);
  const location = useLocation();

  const handleResetData = async () => {
    if (!window.confirm('Reset all network nodes, records, and upgrade projects to hypothetical demonstration sample data?')) {
      return;
    }
    try {
      setResetting(true);
      const res = await api.resetNetwork();
      setResetMessage(res.disclaimer);
      setTimeout(() => {
        window.location.reload();
      }, 500);
    } catch (err: any) {
      alert('Failed to reset sample data: ' + err.message);
    } finally {
      setResetting(false);
    }
  };

  const navItems = [
    { to: '/', label: 'Overview Dashboard', icon: LayoutDashboard },
    { to: '/network-design', label: 'Module 1: Network Design (MST)', icon: GitBranch },
    { to: '/communication-cost', label: 'Module 2: Communication Cost (Floyd)', icon: Network },
    { to: '/record-management', label: 'Module 3: Record Management (Trees)', icon: Database },
    { to: '/maintenance-prioritization', label: 'Module 4: Maintenance Events (Heaps)', icon: ListOrdered },
    { to: '/budget-planner', label: 'Module 5: Budget Planner (Knapsack)', icon: DollarSign },
    { to: '/route-planner', label: 'Module 6: Route Planner (TSP)', icon: Compass },
    { to: '/experiment-lab', label: 'Experiment Lab (Benchmarks)', icon: FlaskConical },
    { to: '/project-report', label: 'DAA Project Report & Docs', icon: FileText },
  ];

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      {/* Top Enterprise Header Bar */}
      <header className="bg-slate-900 border-b border-slate-800 text-white sticky top-0 z-50">
        <div className="px-6 py-3.5 flex items-center justify-between">
          <div className="flex items-center space-x-3.5">
            <div className="p-2 bg-blue-600 rounded-lg text-white shadow-md">
              <Server className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h1 className="font-bold text-base tracking-tight text-white">
                  Adaptive Network Design & Optimization Framework
                </h1>
                <span className="bg-blue-500/20 text-blue-300 border border-blue-500/30 text-[10px] font-semibold px-2 py-0.5 rounded-full uppercase tracking-wider">
                  DAA Project 4
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                AI ML Leopards • Faculty: Professor Geeta Tripathi, Professor of Practice
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="hidden lg:flex items-center space-x-2 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/80 text-xs">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="text-slate-300 font-medium">Backend: FastAPI 1.0 (Python 3.9)</span>
            </div>

            <button
              onClick={handleResetData}
              disabled={resetting}
              className="text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-3 py-1.5 rounded-lg flex items-center space-x-1.5 transition-colors shadow-sm disabled:opacity-50"
              title="Restore clean demonstration data"
            >
              <RotateCcw className={`w-3.5 h-3.5 ${resetting ? 'animate-spin' : ''}`} />
              <span>{resetting ? 'Restoring...' : 'Restore Sample Data'}</span>
            </button>
          </div>
        </div>

        {/* Global Demonstration Notice Banner */}
        <div className="bg-blue-950/90 border-t border-b border-blue-900/60 px-6 py-1 text-[11px] text-blue-200 flex items-center justify-between">
          <span className="flex items-center space-x-1.5">
            <ShieldAlert className="w-3.5 h-3.5 text-blue-400 flex-shrink-0" />
            <span>
              <strong>Academic Demonstration Notice:</strong> All node locations, optical delays, hardware inventories, and project costs are hypothetical test data.
            </span>
          </span>
          <span className="text-blue-300 font-mono hidden md:inline">
            Status: Fully Integrated
          </span>
        </div>
      </header>

      {/* Main App Layout Grid */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar Navigation Menu */}
        <aside className="w-64 bg-white border-r border-slate-200/80 flex flex-col flex-shrink-0">
          <div className="p-4 border-b border-slate-100">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
              DAA Modules & Solvers
            </span>
          </div>

          <nav className="p-3 space-y-1 flex-1 overflow-y-auto">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.to === '/'}
                  className={({ isActive }) =>
                    `flex items-center space-x-3 px-3 py-2.5 rounded-lg text-xs font-semibold transition-colors ${
                      isActive
                        ? 'bg-blue-50 text-blue-700 font-bold border border-blue-200/60 shadow-xs'
                        : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                    }`
                  }
                >
                  <Icon className="w-4 h-4 flex-shrink-0" />
                  <span className="truncate">{item.label}</span>
                </NavLink>
              );
            })}
          </nav>

          {/* Academic Footer in Sidebar */}
          <div className="p-4 border-t border-slate-100 bg-slate-50/50 text-[11px] text-slate-500">
            <div className="font-semibold text-slate-700">Design & Analysis of Algorithms</div>
            <div className="text-[10px] text-slate-400 mt-0.5">Assignment 4 • Academic Release</div>
          </div>
        </aside>

        {/* Content Area */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8 bg-slate-50">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};
