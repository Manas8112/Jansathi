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
    <div className="absolute bottom-0 left-0 right-0 p-4 bg-[color-mix(in_srgb,var(--color-bg-base)_90%,transparent)] backdrop-blur-[8px] border-t border-[var(--color-border-dim)] z-30 transition-colors">
      <div className="max-w-[720px] mx-auto relative flex items-end gap-2 bg-[var(--color-bg-subtle)] border border-[var(--color-border-dim)] rounded-lg p-1 focus-within:border-[var(--color-accent)] transition-colors">
        
        <label className="shrink-0 p-2 text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)] cursor-pointer transition-colors self-end mb-0.5">
          <Paperclip className="w-5 h-5" />
          <input 
            type="file" 
            className="hidden" 
            onChange={handleFileUpload} 
            accept=".pdf,.txt,.docx"
            disabled={loading}
          />
        </label>
        
        <textarea
          ref={textareaRef}
          value={input}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder="Describe your legal situation…"
          className="flex-1 max-h-[120px] bg-transparent text-[14px] text-[var(--color-text-primary)] placeholder-[var(--color-text-muted)] resize-none outline-none py-3 overflow-y-auto scrollbar-thin"
          rows={1}
          disabled={loading}
        />
        
        <button
          onClick={sendMessage}
          disabled={!input.trim() || loading}
          className="shrink-0 w-8 h-8 rounded bg-[var(--color-accent)] flex items-center justify-center text-[#080808] self-end mb-1 mr-1 transition-colors disabled:bg-[var(--color-bg-elevated)] disabled:border disabled:border-[var(--color-border-strong)] disabled:text-[var(--color-text-muted)]"
        >
          <ArrowUp className="w-4 h-4 stroke-[2.5]" />
        </button>
        
      </div>
      <div className="max-w-[720px] mx-auto text-center mt-2">
        <span className="text-[10px] text-[var(--color-text-muted)]">JanSaathi can make mistakes. Verify important information.</span>
      </div>
    </div>
  );
}
