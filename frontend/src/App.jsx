import { Route, Routes, useLocation } from "react-router-dom";
import { useStytchMemberSession } from "@stytch/react/b2b";

import { Dashboard } from "./components/Dashboard";
import { SideNav } from "./components/SideNav";
import { LogInOrSignUp } from "./components/LogInOrSignUp";
import { Authenticate } from "./components/Authenticate";
import { ProtectedRoutes } from "./components/ProtectedRoutes";
import "./App.css";

export const App = () => {
  const location = useLocation();
  const { session } = useStytchMemberSession();
  const showSidebar = session && ["/dashboard"].includes(location.pathname);

  return (
    <div
      className={
        showSidebar
          ? "authenticated-app-container"
          : "unauthenticated-app-container"
      }
    >
      {showSidebar && <SideNav />}
      <div>
        <Routes>
          <Route path="/" element={<LogInOrSignUp />} />
          <Route path="/authenticate" element={<Authenticate />} />
          <Route element={<ProtectedRoutes />}>
            <Route path="/dashboard" element={<Dashboard />} />
          </Route>
        </Routes>
      </div>
    </div>
  );
};
