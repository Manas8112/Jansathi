import React from "react";
import { Paperclip, ArrowUp } from "lucide-react";

interface ChatInputProps {
  input: string;
  handleInput: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  handleKeyDown: (e: React.KeyboardEvent) => void;
  sendMessage: (e?: React.FormEvent) => void;
  loading: boolean;
  textareaRef: React.RefObject<HTMLTextAreaElement | null>;
  handleFileUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export function ChatInput({
  input,
  handleInput,
  handleKeyDown,
  sendMessage,
  loading,
  textareaRef,
  handleFileUpload,
}: ChatInputProps) {
  return (
    <div className="absolute bottom-0 left-0 right-0 p-6 z-30 pointer-events-none flex justify-center">
      <div className="w-full max-w-[720px] pointer-events-auto flex flex-col items-center">
        <div className="w-full relative flex items-end gap-2 bg-[var(--color-glass)] backdrop-blur-2xl border border-[var(--color-glass-border)] rounded-2xl p-1.5 shadow-[0_10px_40px_-10px_var(--color-accent-glow)] focus-within:border-[var(--color-border-accent)] focus-within:shadow-[0_10px_40px_-10px_rgba(16,185,129,0.25)] transition-all">
          
          <label className="shrink-0 p-2.5 text-[var(--color-text-secondary)] hover:text-[var(--color-accent)] cursor-pointer transition-colors self-end mb-0.5 rounded-xl hover:bg-[var(--color-glass-hover)]">
            <Paperclip className="w-5 h-5" />
            <input 
              type="file" 
              className="hidden" 
              onChange={handleFileUpload} 
              accept="application/pdf,image/jpeg,image/png,image/jpg,.md,.txt,.docx"
              disabled={loading}
            />
          </label>
          
          <textarea
            ref={textareaRef}
            value={input}
            onChange={handleInput}
            onKeyDown={handleKeyDown}
            placeholder="Ask me about contracts, regulations, research, or drafting..."
            className="flex-1 max-h-[120px] bg-transparent text-[15px] text-[var(--color-text-primary)] placeholder-slate-500 resize-none outline-none py-3 overflow-y-auto scrollbar-thin"
            rows={1}
            disabled={loading}
          />
          
          <button
            onClick={sendMessage}
            disabled={!input.trim() || loading}
            className="shrink-0 h-[38px] px-4 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-400 flex items-center justify-center text-white font-semibold self-end mb-1 mr-1 transition-all disabled:opacity-50 disabled:grayscale hover:scale-105 shadow-[0_0_15px_var(--color-border-accent)]"
          >
            <span className="hidden sm:inline mr-2">Send</span>
            <ArrowUp className="w-4 h-4 stroke-[3]" />
          </button>
          
        </div>
        <div className="text-center mt-3">
          <span className="text-[11px] text-[var(--color-text-muted)] font-medium tracking-wide">JanSaathi can make mistakes. Verify important information.</span>
        </div>
      </div>
    </div>
  );
}
