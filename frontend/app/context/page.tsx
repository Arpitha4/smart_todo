"use client";

import { useState, useEffect } from "react";
import "../../styles/context.css";

const BASE_URL = "http://127.0.0.1:8000/api";

interface ContextEntry {
  id: number;
  content: string;
  timestamp: string;
  source_type?: string;
}

export default function ContextPage() {
  const [newContext, setNewContext] = useState("");
  const [contextEntries, setContextEntries] = useState<ContextEntry[]>([]);

  useEffect(() => {
    fetch(`${BASE_URL}/context/`)
      .then((res) => res.json())
      .then(setContextEntries);
  }, []);

  const addContext = async () => {
    if (!newContext.trim()) return;

    const response = await fetch(`${BASE_URL}/context/add/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: newContext }),
    });

    if (response.ok) {
      const newEntry = await response.json();
      setContextEntries((prev) => [newEntry, ...prev]);
      setNewContext("");
    }
  };

  return (
    <main className="context-container">
      <div className="context-header">
        <h1 className="context-title">Daily Context</h1>
        <p className="context-subtitle">
          Record thoughts, messages, or notes for smarter task planning.
        </p>
      </div>

      {/* Input Section */}
      <section className="context-input-section">
        <textarea
          placeholder="Enter your thoughts or context..."
          value={newContext}
          onChange={(e) => setNewContext(e.target.value)}
          className="context-textarea"
        />
        <button onClick={addContext} className="context-add-button">
          ➕ Add Context
        </button>
      </section>

      {/* History Section */}
      <section>
        <h2 className="context-history-title">📜 Past Entries</h2>
        <div className="context-list">
          {contextEntries.length === 0 ? (
            <p className="context-empty-message">No entries yet. Start writing!</p>
          ) : (
            contextEntries.map((entry) => (
              <div key={entry.id} className="context-card">
                <p className="context-card-text">{entry.content}</p>
                <p className="context-card-timestamp">
                  {new Date(entry.timestamp).toLocaleString()}
                </p>
              </div>
            ))
          )}
        </div>
      </section>
    </main>
  );
}
