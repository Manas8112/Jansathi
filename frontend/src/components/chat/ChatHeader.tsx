import React from "react";
import { Menu, FolderOpen, Download } from "lucide-react";
import Link from "next/link";
import { UserMenu } from "@/components/UserMenu";

interface ChatHeaderProps {
  setIsSidebarOpen: (v: boolean) => void;
  isSidebarCollapsed: boolean;
  setIsSidebarCollapsed: (v: boolean) => void;
  exportToPDF: () => void;
}

export function ChatHeader({
  setIsSidebarOpen,
  isSidebarCollapsed,
  setIsSidebarCollapsed,
  exportToPDF,
}: ChatHeaderProps) {
  return (
    <header className="h-[52px] bg-[color-mix(in_srgb,var(--color-bg-base)_85%,transparent)] backdrop-blur-md border-b border-[var(--color-border-dim)] flex items-center justify-between px-4 shrink-0 z-20 transition-colors">
      <div className="flex items-center gap-2">
        <button 
          className="md:hidden p-1.5 -ml-1.5 text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] transition-colors"
          onClick={() => setIsSidebarOpen(true)}
        >
          <Menu className="w-5 h-5" />
        </button>
        <button 
          className={`hidden md:block p-1.5 -ml-1.5 text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] transition-all ${isSidebarCollapsed ? 'opacity-100' : 'opacity-0 pointer-events-none -ml-8'}`}
          onClick={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
        >
          <Menu className="w-5 h-5" />
        </button>
      </div>
      
      <div className="flex items-center gap-3">
        <button
          onClick={exportToPDF}
          className="flex items-center gap-1.5 px-3 py-1.5 text-[13px] font-medium text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-bg-subtle)] rounded transition-colors"
          title="Export chat as PDF"
        >
          <Download className="w-4 h-4" /> Export PDF
        </button>
        
        <Link 
          href="/dashboard"
          className="flex items-center gap-1.5 px-3 py-1.5 text-[13px] font-medium text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-bg-subtle)] rounded transition-colors"
        >
          <FolderOpen className="w-4 h-4" /> Documents
        </Link>
        <div className="w-[1px] h-4 bg-[var(--color-border-strong)]" />
        <UserMenu />
      </div>
    </header>
  );
}
