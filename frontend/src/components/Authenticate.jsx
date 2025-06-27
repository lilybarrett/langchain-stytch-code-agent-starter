import { useStytchMemberSession } from '@stytch/react/b2b';
import { Navigate } from 'react-router-dom';
import { LogInOrSignUp } from './LogInOrSignUp';

export const Authenticate = () => {
  const { session } = useStytchMemberSession();

  // Redirect immediately if there's a session
  if (session) {
    return <Navigate to="/dashboard" replace />;
  }

  // Otherwise, render the login/signup form
  return <LogInOrSignUp />;
};
