"use client";

import { useAuth } from "@/lib/auth";
import { LogOut, User as UserIcon } from "lucide-react";
import { useState, useRef, useEffect } from "react";
import { ThemeToggle } from "@/components/ThemeToggle";

export function UserMenu() {
  const { user, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  if (!user) return null;

  return (
    <div className="flex items-center gap-2">
      <ThemeToggle />
      <div className="relative" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 rounded-full border border-[var(--color-border-dim)] bg-[var(--color-bg-surface)] p-1 pr-3 hover:bg-[var(--color-bg-elevated)] transition-colors focus:outline-none focus:ring-1 focus:ring-[var(--color-accent)]"
      >
        <div className="flex h-7 w-7 items-center justify-center rounded-full bg-[var(--color-accent-muted)] text-[var(--color-accent)]">
          {user.avatar_url ? (
            <img src={user.avatar_url} alt={user.name} className="h-full w-full rounded-full object-cover" />
          ) : (
            <UserIcon size={14} />
          )}
        </div>
        <span className="text-[13px] font-sans font-medium text-[var(--color-text-primary)] truncate max-w-[100px]">
          {user.name.split(" ")[0]}
        </span>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 origin-top-right rounded-lg bg-[var(--color-bg-surface)] py-1 shadow-2xl border border-[var(--color-border-strong)] z-50 animate-in fade-in slide-in-from-top-2 duration-150">
          <div className="px-4 py-3 border-b border-[var(--color-border-dim)]">
            <p className="text-[14px] font-medium text-[var(--color-text-primary)] truncate">{user.name}</p>
            <p className="text-[12px] text-[var(--color-text-secondary)] truncate">{user.email}</p>
          </div>
          
          <div className="p-1">
            <button
              onClick={() => {
                setIsOpen(false);
                logout();
              }}
              className="flex w-full items-center gap-2 px-3 py-2 text-[13px] font-medium text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-subtle)] hover:text-[var(--color-text-primary)] rounded transition-colors"
            >
              <LogOut size={14} />
              Sign Out
            </button>
          </div>
        </div>
      )}
      </div>
    </div>
  );
}
