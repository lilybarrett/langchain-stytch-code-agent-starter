import { useStytchMemberSession, useStytchOrganization } from '@stytch/react/b2b';
import { useStytchB2BClient } from '@stytch/react/b2b';
import { useEffect, useState } from 'react';
import ExplainForm from './ExplainForm';
import { useRecentTopics } from '../utils/useRecentTopics';

export const Dashboard = () => {
  const { session } = useStytchMemberSession();
  const { organization } = useStytchOrganization();
  const stytch = useStytchB2BClient();
  const [sessionTokens, setSessionTokens] = useState({});
  const { recentTopics, setRecentTopics, addTopic } = useRecentTopics([]);
  const isAuthorizedToViewRecentTopics = stytch.rbac.isAuthorizedSync('explain.topic', 'read');

  const handleGetTokens = () => {
    const tokens = stytch.session.getTokens();
    setSessionTokens(tokens);
  };

  const role = session?.roles.includes('stytch_admin') ? 'admin' : 'member';

  useEffect(() => {
    if (stytch?.session) {
      handleGetTokens();
    }
  }, []);

  useEffect(() => {
    if (!sessionTokens?.session_token) {
      console.warn('Session token not ready, skipping fetch');
      return;
    }

    const baseUrl = import.meta.env.VITE_REACT_APP_BASE_URL || 'http://localhost:8000';
    fetch(`${baseUrl}/cached-topics`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${sessionTokens.session_token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setRecentTopics(recentTopics.length > 0 ? recentTopics : data.topics);
      })
      .catch((error) => {
        console.error('Error fetching topics:', error);
      });
  }, [sessionTokens]);

  return (
    <div className="dashboard-container">
      <div className="dashboard-content">
        <div className="header-wrapper">
          <h1 className="page-heading">Welcome, {organization?.organization_name}!</h1>
          <p className="page-subheading">
            You’re logged in as an <strong>{role}</strong>. This space is private to your
            organization’s members.
          </p>
        </div>
      </div>
      <ExplainForm sessionToken={sessionTokens?.session_token} addTopic={addTopic} />
      {isAuthorizedToViewRecentTopics && (
        <div className="topics-list">
          <h2>Organization members' last 5 topics</h2>
          {recentTopics?.length > 0 ? (
            <ul>
              {recentTopics.map((topic, index) => (
                <li key={index}>{topic}</li>
              ))}
            </ul>
          ) : (
            <p>No recent topics searched</p>
          )}
        </div>
      )}
    </div>
  );
};
