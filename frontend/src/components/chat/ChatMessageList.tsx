import React from "react";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { Scale, ThumbsUp, ThumbsDown, Copy, ShieldCheck } from "lucide-react";
import { motion } from "framer-motion";
import { FlowAnimation } from "./FlowAnimation";
import { DocumentScanner } from "./DocumentScanner";

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
                            // eslint-disable-next-line @typescript-eslint/no-explicit-any
                            p: ({node, ...props}: any) => <motion.p initial={{opacity: 0, y: 10}} animate={{opacity: 1, y: 0}} transition={{duration: 0.4}} className="mb-4 last:mb-0" {...props} />,
                            // eslint-disable-next-line @typescript-eslint/no-explicit-any
                            h1: ({node, ...props}: any) => <motion.h1 initial={{opacity: 0, y: 10}} animate={{opacity: 1, y: 0}} transition={{duration: 0.4}} className="font-heading font-medium text-xl mt-6 mb-3" {...props} />,
                            // eslint-disable-next-line @typescript-eslint/no-explicit-any
                            h2: ({node, ...props}: any) => <motion.h2 initial={{opacity: 0, y: 10}} animate={{opacity: 1, y: 0}} transition={{duration: 0.4}} className="font-heading font-medium text-lg mt-5 mb-2" {...props} />,
                            // eslint-disable-next-line @typescript-eslint/no-explicit-any
                            h3: ({node, ...props}: any) => <motion.h3 initial={{opacity: 0, y: 10}} animate={{opacity: 1, y: 0}} transition={{duration: 0.4}} className="font-heading font-medium text-[16px] mt-4 mb-2" {...props} />,
                            // eslint-disable-next-line @typescript-eslint/no-explicit-any
                            ul: ({node, ...props}: any) => <motion.ul initial={{opacity: 0}} animate={{opacity: 1}} transition={{duration: 0.5}} className="list-disc pl-5 mb-4" {...props} />,
                            // eslint-disable-next-line @typescript-eslint/no-explicit-any
                            ol: ({node, ...props}: any) => <motion.ol initial={{opacity: 0}} animate={{opacity: 1}} transition={{duration: 0.5}} className="list-decimal pl-5 mb-4" {...props} />,
                            // eslint-disable-next-line @typescript-eslint/no-explicit-any
                            li: ({node, ...props}: any) => <motion.li initial={{opacity: 0, x: -5}} animate={{opacity: 1, x: 0}} transition={{duration: 0.3}} className="mb-1" {...props} />,
                            // eslint-disable-next-line @typescript-eslint/no-explicit-any
                            code: ({node, inline, ...props}: any) => 
                              inline 
                                ? <code className="font-mono text-[13px] bg-[var(--color-bg-subtle)] px-1.5 py-0.5 rounded text-[var(--color-text-primary)]" {...props} />
                                : <motion.code initial={{opacity: 0}} animate={{opacity: 1}} className="block font-mono text-[13px] bg-[var(--color-bg-subtle)] p-4 rounded border border-[var(--color-border-dim)] overflow-x-auto my-4 whitespace-pre-wrap" {...props} />,
                          }}
                        >
                          {msg.content}
                        </ReactMarkdown>
                      </div>
                      
                      {/* Action Buttons for AI Message */}
                      <AIMessageActions content={msg.content} />
                      
                      {/* Reflexion Verified Badge */}
                      {!loading && (msg.intent?.includes("Draft") || msg.intent?.includes("Advice") || msg.intent?.includes("RTI") || msg.intent?.includes("Notice")) && (
                        <motion.div 
                          initial={{ scale: 1.5, opacity: 0 }}
                          animate={{ scale: 1, opacity: 1 }}
                          transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0.5 }}
                          className="mt-4 inline-flex items-center gap-1.5 px-3 py-1.5 bg-[var(--color-accent-glass)] border border-[var(--color-accent-glass)] rounded-full text-[var(--color-accent)] text-[11px] font-semibold tracking-wide uppercase shadow-sm"
                        >
                          <ShieldCheck className="w-3.5 h-3.5" />
                          Reflexion Verified
                        </motion.div>
                      )}

                      {msg.referenced_nodes && msg.referenced_nodes.length > 0 && (
                        <div className="mt-5 flex flex-wrap gap-2" data-html2canvas-ignore="true">
                          {msg.referenced_nodes.map((node, idx) => (
                            <motion.div 
                              key={idx} 
                              initial={{ opacity: 0, scale: 0.8, y: 10 }}
                              animate={{ opacity: 1, scale: 1, y: 0 }}
                              transition={{ delay: 0.1 * idx, type: "spring", stiffness: 100 }}
                              className="group/chip relative flex items-center gap-2 px-3 py-1.5 bg-[var(--color-bg-subtle)] border border-[var(--color-border-dim)] hover:border-[var(--color-accent)] rounded-full transition-all cursor-default"
                            >
                              <div className="w-1.5 h-1.5 rounded-full bg-[var(--color-accent)] animate-pulse"></div>
                              <span className="text-[11px] font-medium text-[var(--color-text-primary)]">{node.name}</span>
                              
                              {/* Tooltip on hover */}
                              {node.description && (
                                <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-48 p-2 bg-[#1a1a1a] border border-[#333] rounded-md shadow-xl opacity-0 invisible group-hover/chip:opacity-100 group-hover/chip:visible transition-all text-[10px] text-[var(--color-text-primary)]/80 z-10 pointer-events-none">
                                  {node.description}
                                </div>
                              )}
                            </motion.div>
                          ))}
                        </div>
                      )}

                    </div>
                  </div>
                )}
              </div>
            ))}

            {/* LOADING INDICATOR */}
            {loading && (
              <div className="flex items-start gap-3 w-full" data-html2canvas-ignore="true">
                {messages.length > 0 && messages[messages.length - 1].content.includes("Uploaded document:") ? (
                  <DocumentScanner />
                ) : (
                  <FlowAnimation />
                )}
              </div>
            )}
            
            <div ref={messagesEndRef} className="h-[150px] shrink-0" data-html2canvas-ignore="true" />
          </div>
        )}
      </div>
    </div>
  );
}
