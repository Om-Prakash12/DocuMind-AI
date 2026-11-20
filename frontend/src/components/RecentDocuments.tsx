
import { useEffect, useState } from "react";
import { FileText, RefreshCw } from "lucide-react";
import api from "../services/api";
import type { DocumentListResponse } from "../types/document";

export default function RecentDocuments() {
  const [data, setData] = useState<DocumentListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get<DocumentListResponse>(
        "/documents/"
      );

      setData(response.data);
    } catch (err) {
      console.error("Document fetching failed:", err);
      setError("Unable to load documents. Check your backend connection.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-950 p-6">
      <div className="mb-5 flex items-center justify-between">
        <h3 className="font-semibold text-white">
          Recent Documents
        </h3>

        <button
          onClick={fetchDocuments}
          disabled={loading}
          className="text-slate-400 hover:text-blue-400"
          title="Refresh documents"
        >
          <RefreshCw size={17} />
        </button>
      </div>

      {loading ? (
        <p className="text-sm text-slate-400">
          Loading documents...
        </p>
      ) : error ? (
        <p className="text-sm text-red-400">{error}</p>
      ) : data && data.documents.length > 0 ? (
        <div className="space-y-4">
          {data.documents.map((document) => (
            <div
              key={document.filename}
              className="flex items-center justify-between gap-4 rounded-lg border border-slate-800 p-4"
            >
              <div className="flex min-w-0 items-center gap-3">
                <div className="rounded-lg bg-blue-500/10 p-3">
                  <FileText className="text-blue-400" size={20} />
                </div>

                <div className="min-w-0">
                  <p className="truncate text-sm font-medium text-white">
                    {document.filename}
                  </p>

                  <p className="text-xs text-slate-400">
                    {document.total_chunks} indexed chunks
                  </p>
                </div>
              </div>

              <span className="shrink-0 rounded-full bg-green-500/10 px-3 py-1 text-xs text-green-400">
                Indexed
              </span>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-sm text-slate-400">
          No documents uploaded yet.
        </p>
      )}
    </div>
  );
}
