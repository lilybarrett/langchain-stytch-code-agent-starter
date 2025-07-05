import ExplainForm from './ExplainForm';

export const Dashboard = () => {
  return (
    <div className="dashboard-container">
      <div className="dashboard-content">
        <div className="header-wrapper">
          <h1 className="page-heading">Welcome, Organization!</h1>
          <p className="page-subheading">Hello! You are viewing the Dashboard. Try out the form.</p>
        </div>
      </div>
      <ExplainForm />
    </div>
  );
};
