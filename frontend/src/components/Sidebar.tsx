
import { NavLink } from "react-router-dom";

import {
  LayoutDashboard,
  Files,
  MessageSquare,
  FileText,
  GitCompareArrows,
  ScanSearch,
  Settings,
  BrainCircuit,
} from "lucide-react";

const menuItems = [
  { name: "Dashboard", icon: LayoutDashboard, path: "/" },
  { name: "Documents", icon: Files, path: "/documents" },
  { name: "AI Chat", icon: MessageSquare, path: "/chat" },
  { name: "Summarization", icon: FileText, path: "/summarize" },
  { name: "Comparison", icon: GitCompareArrows, path: "/compare" },
  { name: "Extraction", icon: ScanSearch, path: "/extract" },
];

export default function Sidebar() {
  return (
    <aside className="flex min-h-screen w-64 shrink-0 flex-col border-r border-slate-800 bg-slate-950 p-5 text-white">
      <div className="mb-10 flex items-center gap-3">
        <div className="rounded-xl bg-blue-600 p-2">
          <BrainCircuit size={25} />
        </div>

        <div>
          <h1 className="text-xl font-bold">DocuMind</h1>
          <p className="text-xs text-slate-400">AI Intelligence</p>
        </div>
      </div>

      <p className="mb-4 text-xs font-semibold uppercase tracking-wider text-slate-500">
        Workspace
      </p>

      <nav className="flex-1 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                `flex w-full items-center gap-3 rounded-lg px-4 py-3 text-sm transition ${
                  isActive
                    ? "bg-blue-600 text-white"
                    : "text-slate-400 hover:bg-slate-900 hover:text-white"
                }`
              }
            >
              <Icon size={19} />
              {item.name}
            </NavLink>
          );
        })}
      </nav>

      <div className="border-t border-slate-800 pt-5">
        <div className="flex items-center gap-3 px-4 py-3 text-sm text-slate-400">
          <Settings size={19} />
          Settings
        </div>

        <div className="mt-5 rounded-xl bg-slate-900 p-4">
          <p className="text-sm font-semibold">DocuMind AI</p>
          <p className="mt-1 text-xs text-slate-400">
            Powered by local AI
          </p>

          <div className="mt-3 flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-green-500" />
            <span className="text-xs text-green-400">
              Local workspace
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}
