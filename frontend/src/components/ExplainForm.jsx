import { useState } from "react";
import "./form.css";

export const ExplainForm = ({ sessionToken }) => {
  const [topic, setTopic] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const baseUrl =
        import.meta.env.VITE_REACT_APP_BASE_URL || "http://localhost:8000";
      const res = await fetch(`${baseUrl}/explain`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${sessionToken}`,
        },
        body: JSON.stringify({ topic }),
      });
      const data = await res.json();
      setResponse(data.response || "No response");
    } catch (err) {
      console.error(err);
      setResponse("Error: Could not fetch explanation.");
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter a topic..."
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />
        <button type="submit">Explain it to me like I’m 5</button>
      </form>
      {response && <div className="response-box">{response}</div>}
    </div>
  );
};
