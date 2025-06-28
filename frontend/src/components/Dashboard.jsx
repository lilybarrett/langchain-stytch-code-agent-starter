import { ExplainForm } from './ExplainForm';

export const Dashboard = () => {
  return (
    <div className="dashboard-container">
      <div className="dashboard-content">
        <div className="header-wrapper">
          <h1 className="page-heading">Welcome!</h1>
          <p className="page-subheading">You are viewing the Dashboard.</p>
        </div>
        <ExplainForm />
      </div>
    </div>
  );
};
