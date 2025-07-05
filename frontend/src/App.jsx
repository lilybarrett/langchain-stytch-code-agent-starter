import { Route, Routes, useLocation, Navigate } from 'react-router-dom';
import { Dashboard } from './components/Dashboard';
import { SideNav } from './components/SideNav';
import { Authenticate } from './components/Authenticate';
import { ProtectedRoutes } from './components/ProtectedRoutes';
import { Members } from './components/Members';
import { Settings } from './components/Settings';
import './App.css';

export const App = () => {
  const location = useLocation();
  const showSidebar = ['/dashboard', '/members', '/settings'].includes(location.pathname);

  return (
    <div className={showSidebar ? 'in-app-container' : 'login-container'}>
      {showSidebar && <SideNav />}
      <div>
        <Routes>
          <Route path="/" element={<Navigate to="/authenticate" replace />} />
          <Route path="/authenticate" element={<Authenticate />} />
          <Route element={<ProtectedRoutes />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/members" element={<Members />} />
            <Route path="/settings" element={<Settings />} />
          </Route>
        </Routes>
      </div>
    </div>
  );
};
