
import { useEffect, useState } from "react";
import {
  FileText,
  Database,
  Layers,
  Activity,
  ArrowUpRight,
  Sparkles,
} from "lucide-react";

import api from "../services/api";
import DocumentUpload from "../components/DocumentUpload";
import RecentDocuments from "../components/RecentDocuments";
import type { DocumentListResponse } from "../types/document";

export default function Dashboard() {
  const [totalDocuments, setTotalDocuments] = useState(0);
  const [totalChunks, setTotalChunks] = useState(0);

  const fetchStats = async () => {
    try {
      const response = await api.get<DocumentListResponse>(
        "/documents/"
      );

      setTotalDocuments(response.data.total_documents);

      setTotalChunks(
        response.data.documents.reduce(
          (total, document) => total + document.total_chunks,
          0
        )
      );
    } catch (error) {
      console.error("Dashboard statistics failed:", error);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const stats = [
    {
      title: "Total Documents",
      value: totalDocuments,
      icon: FileText,
      color: "text-blue-400",
      bg: "bg-blue-500/10",
    },
    {
      title: "Indexed Chunks",
      value: totalChunks,
      icon: Database,
      color: "text-purple-400",
      bg: "bg-purple-500/10",
    },
    {
      title: "AI Queries",
      value: 0,
      icon: Activity,
      color: "text-green-400",
      bg: "bg-green-500/10",
    },
    {
      title: "Storage Status",
      value: "Local",
      icon: Layers,
      color: "text-orange-400",
      bg: "bg-orange-500/10",
    },
  ];

  return (
    <main className="flex-1 overflow-y-auto bg-slate-900 p-8 text-white">
      <header className="mb-8 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Dashboard</h2>
          <p className="mt-1 text-sm text-slate-400">
            Welcome to your AI document workspace.
          </p>
        </div>

        <div className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300">
          <Sparkles className="mr-2 inline text-blue-400" size={16} />
          Powered by Local AI
        </div>
      </header>

      <section className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => {
          const Icon = stat.icon;

          return (
            <div
              key={stat.title}
              className="rounded-xl border border-slate-800 bg-slate-950 p-5"
            >
              <div className="flex items-center justify-between">
                <div className={`rounded-lg p-3 ${stat.bg}`}>
                  <Icon className={stat.color} size={22} />
                </div>

                <ArrowUpRight size={17} className="text-slate-500" />
              </div>

              <p className="mt-5 text-sm text-slate-400">
                {stat.title}
              </p>

              <h3 className="mt-1 text-2xl font-bold">
                {stat.value}
              </h3>
            </div>
          );
        })}
      </section>

      <section className="mt-8">
        <DocumentUpload onUploadSuccess={fetchStats} />
      </section>

      <section className="mt-8 grid grid-cols-1 gap-5 lg:grid-cols-2">
        <RecentDocuments />

        <div className="rounded-xl border border-slate-800 bg-slate-950 p-6">
          <h3 className="font-semibold">AI Activity</h3>
          <p className="mt-2 text-sm text-slate-400">
            Your recent AI interactions will appear here.
          </p>
        </div>
      </section>
    </main>
  );
}
