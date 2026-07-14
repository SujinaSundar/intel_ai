"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Bot,
  Building2,
  BarChart3,
  Landmark,
  Info,
} from "lucide-react";

const menuItems = [
  {
    title: "AI Assistant",
    href: "/",
    icon: Bot,
  },
  {
    title: "Company Explorer",
    href: "/company",
    icon: Building2,
  },
  {
    title: "Compare Companies",
    href: "/compare",
    icon: BarChart3,
  },
  {
    title: "Sector Analysis",
    href: "/sector",
    icon: Landmark,
  },
  {
    title: "About",
    href: "/about",
    icon: Info,
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-950 flex flex-col">
      {/* Logo */}
      <div className="border-b border-slate-800 p-6">
        <h1 className="text-xl font-bold text-white">
          Intel AI
        </h1>

        <p className="text-sm text-slate-400">
          Trading Research
        </p>
      </div>

      {/* Menu */}
      <nav className="flex-1 p-4">
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`mb-2 flex items-center gap-3 rounded-lg px-4 py-3 transition ${
                pathname === item.href
                  ? "bg-blue-600 text-white"
                  : "text-slate-400 hover:bg-slate-800 hover:text-white"
              }`}
            >
              <Icon size={18} />
              {item.title}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="border-t border-slate-800 p-4">
        <div className="rounded-lg bg-slate-900 p-3 text-sm">
          <p className="text-green-400">● LangGraph Ready</p>
          <p className="mt-1 text-slate-400">
            GraphRAG • Groq
          </p>
        </div>
      </div>
    </aside>
  );
}