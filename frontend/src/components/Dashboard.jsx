import {
  useStytchMemberSession,
  useStytchOrganization,
} from "@stytch/react/b2b";
import { useStytchB2BClient } from "@stytch/react/b2b";
import { useEffect, useState } from "react";
import { ExplainForm } from "./ExplainForm";

export const Dashboard = () => {
  const { session } = useStytchMemberSession();
  const { organization } = useStytchOrganization();
  const stytch = useStytchB2BClient();
  const [sessionTokens, setSessionTokens] = useState({});

  // Callback to retrieve session tokens on demand
  const handleGetTokens = () => {
    const tokens = stytch.session.getTokens();
    setSessionTokens(tokens);
  };

  const role = session?.roles.includes("stytch_admin") ? "admin" : "member";

  useEffect(() => {
    if (stytch?.session) {
      handleGetTokens();
    }
  }, []);

  return (
    <div className="dashboard-container">
      <div className="dashboard-content">
        <div className="header-wrapper">
          <h1 className="page-heading">
            Welcome, {organization?.organization_name}!
          </h1>
          <p className="page-subheading">
            You’re logged in as an <strong>{role}</strong>. This space is
            private to your organization’s members.
          </p>
        </div>
      </div>
      <ExplainForm sessionToken={sessionTokens?.session_token} />
    </div>
  );
};
