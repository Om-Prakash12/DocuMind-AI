
import { useState, useRef, useEffect } from "react";
import {
  Send,
  Bot,
  User,
  Sparkles,
  FileText,
  Loader2,
} from "lucide-react";
import api from "../services/api";

interface ChatSource {
  document?: string;
  chunk_id?: string | number;
  score?: number;
  references?: unknown;
}

interface ChatResponse {
  question: string;
  answer: string;
  sources: ChatSource[];
}

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: ChatSource[];
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const sendMessage = async () => {
    const question = query.trim();

    if (!question || loading) return;

    setMessages((previous) => [
      ...previous,
      { role: "user", content: question },
    ]);

    setQuery("");
    setLoading(true);

    try {
      const response = await api.post<{
        status: string;
        data: ChatResponse;
      }>("/chat/", {
        query: question,
        limit: 5,
      });

      const result = response.data.data;

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: result.answer,
          sources: result.sources || [],
        },
      ]);
    } catch (error) {
      console.error("Chat request failed:", error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't process your question. Please check that the backend and Ollama are running.",
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex h-screen flex-1 flex-col bg-slate-900 text-white">
      {/* Header */}
      <header className="border-b border-slate-800 p-6">
        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-blue-600 p-3">
            <Sparkles size={23} />
          </div>

          <div>
            <h2 className="text-xl font-bold">AI Document Chat</h2>
            <p className="text-sm text-slate-400">
              Ask questions about your uploaded documents
            </p>
          </div>
        </div>
      </header>

      {/* Messages */}
      <section className="flex-1 space-y-6 overflow-y-auto p-6">
        {messages.length === 0 && (
          <div className="flex h-full flex-col items-center justify-center text-center">
            <div className="mb-5 rounded-2xl bg-blue-500/10 p-5">
              <Bot size={42} className="text-blue-400" />
            </div>

            <h3 className="text-xl font-semibold">
              Chat with your documents
            </h3>

            <p className="mt-2 max-w-md text-sm text-slate-400">
              Ask questions and get answers grounded in your
              uploaded documents, with source references.
            </p>

            <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950 p-4 text-sm text-slate-400">
              Try asking: "What is Python?"
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex gap-3 ${
              message.role === "user"
                ? "justify-end"
                : "justify-start"
            }`}
          >
            {message.role === "assistant" && (
              <div className="h-9 w-9 shrink-0 rounded-lg bg-blue-600 p-2">
                <Bot size={20} />
              </div>
            )}

            <div className="max-w-3xl">
              <div
                className={`rounded-2xl p-4 text-sm leading-7 ${
                  message.role === "user"
                    ? "bg-blue-600 text-white"
                    : "border border-slate-800 bg-slate-950 text-slate-200"
                }`}
              >
                {message.content}
              </div>

              {message.role === "assistant" &&
                message.sources &&
                message.sources.length > 0 && (
                  <div className="mt-3 rounded-xl border border-slate-800 bg-slate-950 p-4">
                    <p className="mb-3 flex items-center gap-2 text-xs font-semibold text-blue-400">
                      <FileText size={15} />
                      SOURCES ({message.sources.length})
                    </p>

                    {message.sources.map((source, sourceIndex) => (
                      <div
                        key={sourceIndex}
                        className="mb-2 text-xs text-slate-400"
                      >
                        <p>
                          {source.document || "Document"}
                        </p>
                        <p>
                          Chunk: {source.chunk_id ?? "N/A"}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
            </div>

            {message.role === "user" && (
              <div className="h-9 w-9 shrink-0 rounded-lg bg-slate-700 p-2">
                <User size={20} />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-3 text-sm text-blue-400">
            <Loader2 size={20} className="animate-spin" />
            AI is thinking...
          </div>
        )}

        <div ref={messagesEndRef} />
      </section>

      {/* Input */}
      <footer className="border-t border-slate-800 bg-slate-950 p-5">
        <form
          onSubmit={(event) => {
            event.preventDefault();
            sendMessage();
          }}
          className="mx-auto flex max-w-4xl items-center gap-3"
        >
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Ask anything about your documents..."
            disabled={loading}
            className="flex-1 rounded-xl border border-slate-700 bg-slate-900 px-5 py-4 text-sm text-white outline-none placeholder:text-slate-500 focus:border-blue-500"
          />

          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="rounded-xl bg-blue-600 p-4 text-white hover:bg-blue-700 disabled:opacity-50"
          >
            <Send size={20} />
          </button>
        </form>

        <p className="mt-3 text-center text-xs text-slate-500">
          Powered by local LLM · Answers grounded in your documents
        </p>
      </footer>
    </main>
  );
}
