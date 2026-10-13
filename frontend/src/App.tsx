import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { NetworkDesign } from './pages/NetworkDesign';
import { CommunicationCost } from './pages/CommunicationCost';
import { RecordManagement } from './pages/RecordManagement';
import { MaintenancePrioritization } from './pages/MaintenancePrioritization';
import { BudgetPlanner } from './pages/BudgetPlanner';
import { RoutePlanner } from './pages/RoutePlanner';
import { ExperimentLab } from './pages/ExperimentLab';
import { ProjectReport } from './pages/ProjectReport';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="network-design" element={<NetworkDesign />} />
          <Route path="communication-cost" element={<CommunicationCost />} />
          <Route path="record-management" element={<RecordManagement />} />
          <Route path="maintenance-prioritization" element={<MaintenancePrioritization />} />
          <Route path="budget-planner" element={<BudgetPlanner />} />
          <Route path="route-planner" element={<RoutePlanner />} />
          <Route path="experiment-lab" element={<ExperimentLab />} />
          <Route path="project-report" element={<ProjectReport />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
