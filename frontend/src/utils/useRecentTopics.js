import { useState, useCallback } from 'react';

export const useRecentTopics = (initialTopics = []) => {
  const [recentTopics, setRecentTopics] = useState(initialTopics);

  const addTopic = (newTopic) => {
    setRecentTopics((prev) => {
      console.log('Previous topics:', prev);
      return [newTopic, ...prev.slice(0, 4)];
    });
  };

  return {
    recentTopics,
    addTopic,
  };
};
