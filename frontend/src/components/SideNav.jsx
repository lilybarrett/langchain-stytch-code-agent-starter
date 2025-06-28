import { NavLink } from 'react-router-dom';

export const SideNav = () => {
  return (
    <nav className="sidebar">
      <div className="nav-links">
        <NavLink to="/dashboard" className={({ isActive }) => (isActive ? 'active-link' : '')}>
          Home
        </NavLink>
        <NavLink to="/members" className={({ isActive }) => (isActive ? 'active-link' : '')}>
          Members
        </NavLink>
        <NavLink to="/settings" className={({ isActive }) => (isActive ? 'active-link' : '')}>
          Settings
        </NavLink>
      </div>
    </nav>
  );
};
