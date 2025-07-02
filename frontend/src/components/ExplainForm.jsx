import { useState } from 'react';
import './form.css';
import { withStytchPermissions } from '@stytch/react/b2b';

const ExplainForm = (props) => {
  const { sessionToken, addTopic } = props;
  const [topic, setTopic] = useState('');
  const [response, setResponse] = useState('');
  const canSubmitTopic = props.stytchPermissions['explain.topic']['create'];

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const baseUrl = import.meta.env.VITE_REACT_APP_BASE_URL || 'http://localhost:8000';
      const res = await fetch(`${baseUrl}/explain`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${sessionToken}`,
        },
        body: JSON.stringify({ topic }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || 'Failed to fetch explanation');
      }

      addTopic(topic);
      setResponse(data.response);
    } catch (err) {
      console.error(err);
      setResponse('Error: Could not fetch explanation.');
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit}>
        {!canSubmitTopic && (
          <div className="error-message">
            You do not have permission to submit topics. Please contact your administrator.
          </div>
        )}
        <label htmlFor="topic">Topic:</label>
        <input
          disabled={!canSubmitTopic}
          type="text"
          placeholder="Enter a topic..."
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />
        <button disabled={!canSubmitTopic} type="submit">
          Explain it to me like I’m 5
        </button>
      </form>
      {response && <div className="response-box">{response}</div>}
    </div>
  );
};

export default withStytchPermissions(ExplainForm);
