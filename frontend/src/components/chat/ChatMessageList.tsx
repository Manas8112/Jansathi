import React from "react";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { Scale, ThumbsUp, ThumbsDown, Copy } from "lucide-react";
import { FlowAnimation } from "./FlowAnimation";

const AIMessageActions = ({ content }: { content: string }) => {
  const [copied, setCopied] = React.useState(false);
  const [feedback, setFeedback] = React.useState<'up' | 'down' | null>(null);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex items-center gap-2 mt-3 opacity-0 group-hover:opacity-100 transition-opacity" data-html2canvas-ignore="true">
      <button 
        onClick={handleCopy}
        className="p-1.5 rounded bg-[var(--color-bg-subtle)] text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-bg-surface)] transition-colors border border-[var(--color-border-dim)]" title="Copy Message">
        <Copy className={`w-3.5 h-3.5 ${copied ? 'text-emerald-500' : ''}`} />
      </button>
      <button 
        onClick={() => setFeedback('up')}
        className={`p-1.5 rounded bg-[var(--color-bg-subtle)] hover:bg-[var(--color-bg-surface)] transition-colors border border-[var(--color-border-dim)] ${feedback === 'up' ? 'text-[var(--color-accent)]' : 'text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)]'}`} title="Helpful">
        <ThumbsUp className={`w-3.5 h-3.5 ${feedback === 'up' ? 'fill-current' : ''}`} />
      </button>
      <button 
        onClick={() => setFeedback('down')}
        className={`p-1.5 rounded bg-[var(--color-bg-subtle)] hover:bg-[var(--color-bg-surface)] transition-colors border border-[var(--color-border-dim)] ${feedback === 'down' ? 'text-red-500' : 'text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)]'}`} title="Not Helpful">
        <ThumbsDown className={`w-3.5 h-3.5 ${feedback === 'down' ? 'fill-current' : ''}`} />
      </button>
    </div>
  );
};

export interface Message {
  role: "user" | "ai";
  content: string;
  intent?: string;
  timestamp?: Date;
  referenced_nodes?: { name: string, type: string, description: string }[];
}

interface ChatMessageListProps {
  messages: Message[];
  loading: boolean;
  setInput: (v: string) => void;
  textareaRef: React.RefObject<HTMLTextAreaElement | null>;
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
  suggestedPrompts: string[];
  exportRef: React.RefObject<HTMLDivElement | null>;
}

export function ChatMessageList({
  messages,
  loading,
  setInput,
  textareaRef,
  messagesEndRef,
  suggestedPrompts,
  exportRef,
}: ChatMessageListProps) {
  return (
    <div className="flex-1 overflow-y-auto pt-8 pb-4 px-4 scrollbar-thin bg-[var(--color-bg-base)]">
      <div ref={exportRef} className="w-full min-h-full flex flex-col p-4 bg-[var(--color-bg-base)]">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center max-w-[560px] mx-auto pb-12">
            <div className="w-12 h-12 flex items-center justify-center mb-6 text-[var(--color-accent)]">
              <Scale className="w-10 h-10 stroke-[1.5]" />
            </div>
            <h2 className="font-heading font-medium text-[22px] text-[var(--color-text-primary)] text-center mb-2">
              What legal matter can I help with?
            </h2>
            <p className="text-[14px] text-[var(--color-text-secondary)] text-center mb-10 max-w-[360px] leading-relaxed">
              Describe your situation in plain language. I&apos;ll identify the right legal path and draft your documents.
            </p>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full" data-html2canvas-ignore="true">
              {suggestedPrompts.map((prompt, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setInput(prompt);
                    textareaRef.current?.focus();
                  }}
                  className="group flex items-center gap-3 bg-[var(--color-bg-surface)] border border-[var(--color-border-strong)] rounded-lg p-3.5 text-left transition-colors hover:border-[var(--color-border-accent)] hover:bg-[var(--color-accent-muted)]"
                >
                  <div className="w-1 h-1 rounded-sm bg-[var(--color-accent)] shrink-0 opacity-70 group-hover:opacity-100" />
                  <span className="text-[13px] font-sans font-normal text-[var(--color-text-primary)] leading-tight">{prompt}</span>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="max-w-[720px] mx-auto w-full flex flex-col gap-8">
            {messages.map((msg, i) => (
              <div key={i} className={`flex w-full group ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                
                {msg.role === "user" ? (
                  <div className="flex items-end gap-2 max-w-[70%]">
                    <span className="text-[10px] text-[var(--color-text-muted)] opacity-0 group-hover:opacity-100 transition-opacity mb-1 shrink-0">
                      {msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ''}
                    </span>
                    <div className="bg-[var(--color-accent)] text-[#080808] px-3.5 py-2.5 rounded-t-xl rounded-bl-xl rounded-br-[2px] text-[13px] font-sans font-normal leading-relaxed whitespace-pre-wrap shadow-sm">
                      {msg.content}
                    </div>
                  </div>
                ) : (
                  <div className="flex items-start gap-3 w-full pl-4 border-l-2 border-[var(--color-border-accent)]">
                    <div className="flex-1 min-w-0">
                      
                      <div className="flex items-center gap-2 mb-2">
                        {msg.intent && (
                          <span className="inline-flex items-center px-2 py-1 rounded bg-[var(--color-accent-muted)] border border-[var(--color-border-accent)] border-opacity-30 text-[10px] font-sans font-medium text-[var(--color-accent)] tracking-wide uppercase">
                            {msg.intent}
                          </span>
                        )}
                        <span className="text-[10px] text-[var(--color-text-muted)] opacity-0 group-hover:opacity-100 transition-opacity">
                          {msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ''}
                        </span>
                      </div>
                      
                      <div className="text-[15px] font-sans leading-[1.8] text-[var(--color-text-primary)]">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          rehypePlugins={[rehypeRaw]}
                          components={{
                            p: ({node, ...props}) => <p className="mb-4 last:mb-0" {...props} />,
                            h1: ({node, ...props}) => <h1 className="font-heading font-medium text-xl mt-6 mb-3" {...props} />,
                            h2: ({node, ...props}) => <h2 className="font-heading font-medium text-lg mt-5 mb-2" {...props} />,
                            h3: ({node, ...props}) => <h3 className="font-heading font-medium text-[16px] mt-4 mb-2" {...props} />,
                            ul: ({node, ...props}) => <ul className="list-disc pl-5 mb-4" {...props} />,
                            ol: ({node, ...props}) => <ol className="list-decimal pl-5 mb-4" {...props} />,
                            li: ({node, ...props}) => <li className="mb-1" {...props} />,
                            // eslint-disable-next-line @typescript-eslint/no-explicit-any
                            code: ({node, inline, ...props}: any) => 
                              inline 
                                ? <code className="font-mono text-[13px] bg-[var(--color-bg-subtle)] px-1.5 py-0.5 rounded text-[var(--color-text-primary)]" {...props} />
                                : <code className="block font-mono text-[13px] bg-[var(--color-bg-subtle)] p-4 rounded border border-[var(--color-border-dim)] overflow-x-auto my-4 whitespace-pre-wrap" {...props} />,
                          }}
                        >
                          {msg.content}
                        </ReactMarkdown>
                      </div>
                      
                      {/* Action Buttons for AI Message */}
                      <AIMessageActions content={msg.content} />
                      
                      {msg.referenced_nodes && msg.referenced_nodes.length > 0 && (
                        <details className="mt-4 border border-[var(--color-border-dim)] rounded-md bg-[var(--color-bg-subtle)]" data-html2canvas-ignore="true">
                          <summary className="cursor-pointer text-[12px] text-[var(--color-text-muted)] p-2 font-medium hover:text-[var(--color-text-primary)] transition-colors">
                            📚 Knowledge Sources ({msg.referenced_nodes.length})
                          </summary>
                          <ul className="px-4 pb-3 pt-1 text-[11px] text-[var(--color-text-secondary)] space-y-2">
                            {msg.referenced_nodes.map((node, idx) => (
                              <li key={idx} className="border-l-2 border-[var(--color-accent)] pl-2">
                                <span className="font-semibold block text-[var(--color-text-primary)]">{node.name}</span>
                                {node.description && <span className="block mt-0.5 opacity-80">{node.description}</span>}
                              </li>
                            ))}
                          </ul>
                        </details>
                      )}

                    </div>
                  </div>
                )}
              </div>
            ))}

            {/* LOADING INDICATOR: Using FlowAnimation */}
            {loading && (
              <div className="flex items-start gap-3 w-full" data-html2canvas-ignore="true">
                <FlowAnimation />
              </div>
            )}
            
            <div ref={messagesEndRef} className="h-[150px] shrink-0" data-html2canvas-ignore="true" />
          </div>
        )}
      </div>
    </div>
  );
}
