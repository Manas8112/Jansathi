"use client";

import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { X, Download } from "lucide-react";

export interface DocumentInfo {
  id: string;
  title: string;
  doc_type: string;
  content: string;
  created_at: string;
}

interface DocumentModalProps {
  isOpen: boolean;
  onClose: () => void;
  document: DocumentInfo | null;
  onDownload: () => void;
}

const DOC_TYPE_CONFIG: Record<string, { label: string; color: string }> = {
  rti: { label: "RTI Application", color: "var(--color-accent)" },
  legal_notice: { label: "Legal Notice", color: "var(--color-semantic-blue)" },
  consumer_complaint: { label: "Consumer Complaint", color: "var(--color-semantic-green)" },
  rera_complaint: { label: "RERA Complaint", color: "var(--color-semantic-purple)" },
  legal_advice: { label: "Legal Advice", color: "var(--color-semantic-slate)" },
};

export function DocumentModal({ isOpen, onClose, document, onDownload }: DocumentModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);

  // Handle Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    if (isOpen) {
      window.addEventListener("keydown", handleKeyDown);
      window.document.body.style.overflow = "hidden"; // Prevent background scrolling
    }
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.document.body.style.overflow = "unset";
    };
  }, [isOpen, onClose]);

  // Basic focus trap - focus modal when opened
  useEffect(() => {
    if (isOpen && modalRef.current) {
      modalRef.current.focus();
    }
  }, [isOpen]);

  if (!isOpen || !document) return null;

  const cfg = DOC_TYPE_CONFIG[document.doc_type] || { label: document.doc_type, color: "var(--color-text-secondary)" };

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[rgba(0,0,0,0.75)] backdrop-blur-sm animate-in fade-in duration-200"
      onClick={onClose}
    >
      <div 
        ref={modalRef}
        tabIndex={-1}
        className="w-full max-w-[760px] h-[90vh] bg-[var(--color-bg-surface)] border border-[var(--color-border-strong)] rounded-xl flex flex-col overflow-hidden shadow-2xl animate-in zoom-in-95 duration-200 outline-none"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="h-[56px] px-6 border-b border-[var(--color-border-dim)] flex items-center justify-between shrink-0 bg-[var(--color-bg-surface)]">
          <div className="flex items-center gap-3 overflow-hidden">
            <span 
              className="text-[10px] font-sans font-medium uppercase tracking-[0.08em] px-2 py-0.5 rounded-sm border"
              style={{ color: cfg.color, borderColor: cfg.color, backgroundColor: `color-mix(in srgb, ${cfg.color} 10%, transparent)` }}
            >
              {cfg.label}
            </span>
            <h2 className="font-heading font-medium text-[15px] text-[var(--color-text-primary)] truncate">
              {document.title}
            </h2>
          </div>
          
          <div className="flex items-center gap-4 shrink-0 pl-4">
            <button
              onClick={onDownload}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-[var(--color-accent)] hover:bg-[var(--color-accent-dim)] text-[#080808] text-[13px] font-medium rounded transition-colors"
            >
              <Download className="w-3.5 h-3.5" /> Download PDF
            </button>
            <button
              onClick={onClose}
              className="p-1.5 text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-bg-subtle)] rounded transition-colors"
              aria-label="Close modal"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto px-6 py-8 sm:px-10">
          <div className="prose prose-invert max-w-none">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                p: ({node, ...props}) => <p className="text-[15px] font-sans font-normal text-[var(--color-text-primary)] leading-[1.8] mb-4" {...props} />,
                h1: ({node, ...props}) => <h1 className="font-heading font-medium text-2xl text-[var(--color-text-primary)] mt-8 mb-4" {...props} />,
                h2: ({node, ...props}) => <h2 className="font-heading font-medium text-xl text-[var(--color-text-primary)] mt-6 mb-3" {...props} />,
                h3: ({node, ...props}) => <h3 className="font-heading font-medium text-lg text-[var(--color-text-primary)] mt-5 mb-2" {...props} />,
                ul: ({node, ...props}) => <ul className="list-disc pl-5 mb-4 text-[15px] font-sans font-normal text-[var(--color-text-primary)] leading-[1.8]" {...props} />,
                ol: ({node, ...props}) => <ol className="list-decimal pl-5 mb-4 text-[15px] font-sans font-normal text-[var(--color-text-primary)] leading-[1.8]" {...props} />,
                li: ({node, ...props}) => <li className="mb-1" {...props} />,
                code: ({node, inline, ...props}: any) => 
                  inline 
                    ? <code className="font-mono text-[13px] bg-[var(--color-bg-subtle)] px-1.5 py-0.5 rounded text-[var(--color-text-primary)]" {...props} />
                    : <code className="block font-mono text-[13px] bg-[var(--color-bg-subtle)] p-4 rounded border border-[var(--color-border-dim)] text-[var(--color-text-primary)] overflow-x-auto whitespace-pre-wrap" {...props} />,
              }}
            >
              {document.content}
            </ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  );
}
