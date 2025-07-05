"use client";
import Link from "next/link";
import { ClipboardList, Brain, FileText } from "lucide-react";

export default function Home() {
  return (
    <main className="home-main">
      <h1 className="home-heading">Welcome to Smart Todo</h1>
      <p className="home-subheading">Your AI-powered task management assistant</p>

      <div className="home-cards">
        <Link href="/dashboard" className="home-card dashboard-card">
          <ClipboardList className="home-icon" />
          <h2 className="home-title">Task Dashboard</h2>
          <p className="home-description">Manage & prioritize tasks</p>
        </Link>

        <Link href="/ai-suggestions" className="home-card suggestion-card">
          <Brain className="home-icon" />
          <h2 className="home-title">AI Suggestions</h2>
          <p className="home-description">Get smart task ideas</p>
        </Link>

        <Link href="/context" className="home-card context-card">
          <FileText className="home-icon" />
          <h2 className="home-title">Context Input</h2>
          <p className="home-description">Provide notes & context</p>
        </Link>
      </div>
    </main>
  );
}
