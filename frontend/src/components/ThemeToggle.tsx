"use client";

import { useTheme } from "@/components/ThemeProvider";
import { Moon, Sun } from "lucide-react";

export function ThemeToggle({ className = "" }: { className?: string }) {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className={`relative flex items-center justify-center p-2 rounded-full text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-bg-elevated)] transition-colors ${className}`}
      aria-label="Toggle theme"
    >
      {/* Sun icon for dark mode (click to switch to light) */}
      <Sun 
        className={`w-[18px] h-[18px] transition-all absolute ${theme === 'dark' ? 'scale-100 opacity-100 rotate-0' : 'scale-50 opacity-0 -rotate-90'}`} 
      />
      {/* Moon icon for light mode (click to switch to dark) */}
      <Moon 
        className={`w-[18px] h-[18px] transition-all absolute ${theme === 'light' ? 'scale-100 opacity-100 rotate-0' : 'scale-50 opacity-0 rotate-90'}`} 
      />
      {/* Placeholder to maintain button size */}
      <div className="w-[18px] h-[18px]" aria-hidden="true" />
    </button>
  );
}
