import React from "react";
import { Menu, X, Trash2 } from "lucide-react";

export interface Conversation {
  id: string;
  title: string;
  updated_at: string;
}

interface ChatSidebarProps {
  isSidebarOpen: boolean;
  setIsSidebarOpen: (v: boolean) => void;
  isSidebarCollapsed: boolean;
  setIsSidebarCollapsed: (v: boolean) => void;
  fetchingSidebar: boolean;
  conversations: Conversation[];
  currentConversationId: string | null;
  loadConversation: (id: string) => void;
  startNewChat: () => void;
  deleteConversation: (e: React.MouseEvent, id: string) => void;
}

export function ChatSidebar({
  isSidebarOpen,
  setIsSidebarOpen,
  isSidebarCollapsed,
  setIsSidebarCollapsed,
  fetchingSidebar,
  conversations,
  currentConversationId,
  loadConversation,
  startNewChat,
  deleteConversation,
}: ChatSidebarProps) {
  const sidebarContent = (
    <div className="flex flex-col h-full bg-[var(--color-bg-surface)]">
      <div className="p-4 shrink-0 flex items-center justify-between md:mt-2 md:mb-2">
        <div className="flex items-center gap-2 md:gap-3">
          <button 
            className="hidden md:block p-1.5 -ml-1.5 text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] transition-colors"
            onClick={() => setIsSidebarCollapsed(true)}
          >
            <Menu className="w-5 h-5" />
          </button>
          <div className="font-heading font-semibold text-[20px] text-[var(--color-accent)] tracking-tight px-1">
            JanSaathi
          </div>
        </div>
        <button className="md:hidden p-1 text-[var(--color-text-muted)]" onClick={() => setIsSidebarOpen(false)}>
          <X className="w-5 h-5" />
        </button>
      </div>
      
      <div className="px-4 pb-6 shrink-0 mt-2">
        <button 
          onClick={startNewChat}
          className="group w-full flex items-center justify-start gap-3 h-[44px] px-4 bg-transparent border border-[var(--color-glass-border)] text-[var(--color-text-primary)] hover:text-[var(--color-text-primary)] rounded-xl transition-all font-medium hover:border-[var(--color-border-accent)] hover:bg-[var(--color-accent-glow)] relative overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/0 via-emerald-500/10 to-emerald-500/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
          <span className="text-[20px] font-light text-[var(--color-accent)] leading-none group-hover:scale-125 transition-transform">+</span> 
          <span className="text-[14px]">New Chat</span>
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto px-2 pb-4 scrollbar-thin">
        {fetchingSidebar ? (
          <div className="px-2 space-y-2 mt-2">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-[36px] w-full rounded flex items-center px-2">
                <div className="w-full flex flex-col gap-1.5 opacity-50">
                  <div className="h-2.5 bg-[var(--color-bg-elevated)] rounded-sm w-3/4 animate-pulse"></div>
                  <div className="h-2 bg-[var(--color-bg-elevated)] rounded-sm w-1/4 animate-pulse" style={{ animationDelay: '100ms' }}></div>
                </div>
              </div>
            ))}
          </div>
        ) : conversations.length === 0 ? (
          <div className="px-4 mt-4 text-[12px] text-[var(--color-text-muted)]">No past conversations.</div>
        ) : (
          <div className="space-y-0.5">
            {conversations.map((conv) => {
              const isActive = currentConversationId === conv.id;
              return (
                <div 
                  key={conv.id} 
                  className={`group flex items-center justify-between w-full h-[40px] px-3 rounded-lg transition-all cursor-pointer ${
                    isActive 
                      ? 'bg-gradient-to-r from-emerald-500/15 to-transparent border-l-[3px] border-[var(--color-accent)] pl-2.5' 
                      : 'border-l-[3px] border-transparent hover:bg-[var(--color-glass-hover)]'
                  }`}
                  onClick={() => loadConversation(conv.id)}
                >
                  <div className="flex flex-col justify-center w-full min-w-0 pr-2">
                    <span className={`text-[13px] truncate leading-tight ${isActive ? 'text-[var(--color-text-primary)] font-medium' : 'text-[var(--color-text-secondary)] font-normal group-hover:text-[var(--color-text-primary)]'}`}>
                      {conv.title || "New Chat"}
                    </span>
                  </div>
                  <button 
                    onClick={(e) => deleteConversation(e, conv.id)}
                    className="p-1 shrink-0 opacity-0 group-hover:opacity-100 text-[var(--color-text-muted)] hover:text-[var(--color-semantic-red)] transition-all"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  );

  return (
    <>
      {/* DESKTOP SIDEBAR */}
      <div className={`hidden md:block h-full shrink-0 border-r border-[var(--color-border-dim)] z-10 transition-all duration-300 ease-in-out ${isSidebarCollapsed ? 'w-0 overflow-hidden border-r-0' : 'w-[280px]'}`}>
        <div className="w-[280px] h-full">
          {sidebarContent}
        </div>
      </div>

      {/* MOBILE SIDEBAR & OVERLAY */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-[rgba(0,0,0,0.6)] z-40 md:hidden animate-in fade-in duration-150"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}
      <div 
        className={`fixed inset-y-0 left-0 w-[280px] z-50 transform transition-transform duration-200 ease-out border-r border-[var(--color-border-dim)] md:hidden ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {sidebarContent}
      </div>
    </>
  );
}
