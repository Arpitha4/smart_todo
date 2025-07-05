"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import "../../styles/suggestion.css";

const BASE_URL = "http://127.0.0.1:8000/api";
const CATEGORY_OPTIONS = ["Frontend", "Backend"];
const PRIORITY_OPTIONS = ["High", "Medium", "Low"];

interface ContextEntry {
  content: string;
}

export default function AISuggestions() {
  const [contextList, setContextList] = useState<string[]>([]);
  const [newContext, setNewContext] = useState("");
  const [savedContext, setSavedContext] = useState<ContextEntry[]>([]);
  const [aiTask, setAiTask] = useState<any | null>(null);

  useEffect(() => {
    const fetchSavedContext = async () => {
      try {
        const res = await axios.get(`${BASE_URL}/context/`);
        setSavedContext(res.data);
      } catch (err) {
        console.error("Failed to load saved context:", err);
      }
    };
    fetchSavedContext();
  }, []);

  const handleAddContext = () => {
    if (newContext.trim()) {
      setContextList([...contextList, newContext.trim()]);
      setNewContext("");
    }
  };

  const handleUseSavedContext = (content: string) => {
    setNewContext(content);
  };

  const handleAutoCreate = async () => {
    try {
      const allContext = [
        ...contextList.map((content) => ({ content })),
        ...savedContext.map((entry) => ({ content: entry.content })),
      ];

      const response = await axios.post(`${BASE_URL}/tasks/auto-create/`, {
        context: allContext,
      });

      setAiTask(response.data);
    } catch (err) {
      console.error("AI Task creation failed:", err);
    }
  };

  const handleSaveTask = async () => {
    try {
      await axios.post(`${BASE_URL}/tasks/create/`, aiTask);
      alert("Task saved successfully!");
      setAiTask(null);
      setContextList([]);
    } catch (err) {
      console.error("Error saving task:", err);
      alert("Failed to save task.");
    }
  };

  return (
    <main className="suggestion-container">
      <h1 className="suggestion-title">Smart AI Task Creator</h1>

      <div className="context-section">
        <label className="context-label">
          Add Daily Context (emails, messages, notes)
        </label>
        <textarea
          rows={3}
          className="context-textarea"
          placeholder="Enter context message..."
          value={newContext}
          onChange={(e) => setNewContext(e.target.value)}
        />
        <button onClick={handleAddContext} className="context-add-btn">
          ➕ Add Context
        </button>

        {contextList.length > 0 && (
          <ul className="context-list">
            {contextList.map((ctx, idx) => (
              <li key={idx}>{ctx}</li>
            ))}
          </ul>
        )}

        <button onClick={handleAutoCreate} className="generate-btn">
          🤖 Generate Task with AI
        </button>
      </div>

      <div className="saved-context-section">
        <h1 className="saved-context-title">Past Entries</h1>
        {savedContext.length === 0 ? (
          <p>No saved context entries yet.</p>
        ) : (
          <ul className="saved-context-list">
            {savedContext.map((entry, index) => (
              <li key={index} className="saved-context-item">
                <span>{entry.content}</span>
                <button
                  onClick={() => handleUseSavedContext(entry.content)}
                  className="use-context-btn"
                >
                  Add Context
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      {aiTask && (
        <div className="ai-task">
          <h2 className="ai-title">✏️ Edit AI-Generated Task</h2>

          <div>
            <label className="ai-label">Title</label>
            <input
              className="ai-input"
              value={aiTask.title}
              onChange={(e) =>
                setAiTask({ ...aiTask, title: e.target.value })
              }
            />
          </div>

          <div>
            <label className="ai-label">Description</label>
            <textarea
              rows={3}
              className="ai-textarea"
              value={aiTask.description}
              onChange={(e) =>
                setAiTask({ ...aiTask, description: e.target.value })
              }
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="ai-label">Category</label>
              <select
                className="ai-select"
                value={aiTask.category}
                onChange={(e) =>
                  setAiTask({ ...aiTask, category: e.target.value })
                }
              >
                {CATEGORY_OPTIONS.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="ai-label">Priority</label>
              <select
                className="ai-select"
                value={aiTask.priority}
                onChange={(e) =>
                  setAiTask({ ...aiTask, priority: e.target.value })
                }
              >
                {PRIORITY_OPTIONS.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="ai-label">Deadline</label>
            <input
              type="date"
              className="ai-date"
              value={aiTask.deadline}
              onChange={(e) =>
                setAiTask({ ...aiTask, deadline: e.target.value })
              }
            />
          </div>

          <button onClick={handleSaveTask} className="save-btn">
            💾 Save Task
          </button>
        </div>
      )}
    </main>
  );
}
