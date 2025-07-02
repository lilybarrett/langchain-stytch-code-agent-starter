import { useState, useCallback } from 'react';

export const useRecentTopics = (initialTopics = []) => {
  const [recentTopics, setRecentTopics] = useState(initialTopics);

  // TODO get this working again
  const addTopic = useCallback((topic) => {
    setRecentTopics((prevTopics = []) => {
      const updatedTopics = [topic, ...prevTopics].slice(0, 5); // Keep only the last 5 topics
      return updatedTopics;
    });
  }, []);

  return {
    recentTopics,
    setRecentTopics,
    addTopic,
  };
};
