"use client";

import { useAuth } from "../lib/auth";
import { LogOut, User as UserIcon } from "lucide-react";
import { useState, useRef, useEffect } from "react";

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
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 rounded-full border border-[#2a2a3d] bg-[#12121e] p-1 pr-3 hover:bg-[#1a1a2e] transition-colors focus:outline-none focus:ring-1 focus:ring-[#e6a336]"
      >
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-[#e6a336]/20 text-[#e6a336]">
          {user.avatar_url ? (
            <img src={user.avatar_url} alt={user.name} className="h-full w-full rounded-full object-cover" />
          ) : (
            <UserIcon size={16} />
          )}
        </div>
        <span className="text-sm font-medium text-white truncate max-w-[100px]">
          {user.name.split(" ")[0]}
        </span>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 origin-top-right rounded-lg bg-[#1a1a2e] py-1 shadow-lg ring-1 ring-black ring-opacity-5 border border-[#2a2a3d] z-50">
          <div className="px-4 py-2 border-b border-[#2a2a3d]">
            <p className="text-sm font-medium text-white truncate">{user.name}</p>
            <p className="text-xs text-[#8888a0] truncate">{user.email}</p>
          </div>
          
          <button
            onClick={() => {
              setIsOpen(false);
              logout();
            }}
            className="flex w-full items-center gap-2 px-4 py-2 text-sm text-[#8888a0] hover:bg-[#22223a] hover:text-white transition-colors"
          >
            <LogOut size={16} />
            Sign Out
          </button>
        </div>
      )}
    </div>
  );
}
