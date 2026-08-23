"use client";

import { useState, useRef, useEffect } from "react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { UserMenu } from "@/components/UserMenu";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { Paperclip, ArrowUp, Menu, X, FolderOpen, Scale, Trash2 } from "lucide-react";
import Link from "next/link";
import Cookies from "js-cookie";
import { useToast } from "@/hooks/useToast";

interface Message {
  role: "user" | "ai";
  content: string;
  intent?: string;
  timestamp?: Date;
}

interface Conversation {
  id: string;
  title: string;
  updated_at: string;
}

const SUGGESTED_PROMPTS = [
  "Draft an RTI application",
  "File a consumer complaint",
  "Send a legal notice",
  "Explain my tenant rights"
];

const LOADING_STATUSES = [
  "Reading your situation…",
  "Searching legal precedents…",
  "Checking applicable statutes…",
  "Drafting your document…"
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingStatusIdx, setLoadingStatusIdx] = useState(0);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); // Mobile sidebar
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false); // Desktop sidebar
  const [fetchingSidebar, setFetchingSidebar] = useState(true);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { toast } = useToast();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const fetchConversations = async () => {
    setFetchingSidebar(true);
    try {
      const token = Cookies.get("token");
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/chat/conversations`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setConversations(data);
      }
    } catch (e) {
      toast("Failed to load conversation history.", "error");
    } finally {
      setFetchingSidebar(false);
    }
  };

  useEffect(() => {
    fetchConversations();
  }, []);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (loading) {
      interval = setInterval(() => {
        setLoadingStatusIdx((prev) => (prev + 1) % LOADING_STATUSES.length);
      }, 2500);
    } else {
      setLoadingStatusIdx(0);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    // Auto-grow textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  };

  const loadConversation = async (id: string) => {
    setLoading(true);
    setIsSidebarOpen(false);
    try {
      const token = Cookies.get("token");
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/chat/conversations/${id}`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setMessages(data);
        setCurrentConversationId(id);
      } else {
        toast("Could not load the conversation.", "error");
      }
    } catch (e) {
      toast("Connection error.", "error");
    } finally {
      setLoading(false);
    }
  };

  const startNewChat = () => {
    setMessages([]);
    setCurrentConversationId(null);
    setIsSidebarOpen(false);
    setInput("");
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
  };

  const deleteConversation = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (!confirm("Are you sure you want to delete this chat history?")) return;
    
    try {
      const token = Cookies.get("token");
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/chat/conversations/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        if (currentConversationId === id) {
          startNewChat();
        }
        fetchConversations();
        toast("Chat deleted", "success");
      } else {
        toast("Failed to delete chat", "error");
      }
    } catch (e) {
      toast("Connection error", "error");
    }
  };

  const sendMessage = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    setInput("");
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
    
    setMessages((prev) => [...prev, { role: "user", content: userMsg, timestamp: new Date() }]);
    setLoading(true);

    try {
      const token = Cookies.get("token");
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/chat/`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}` 
        },
        body: JSON.stringify({ 
          message: userMsg,
          conversation_id: currentConversationId 
        }),
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        throw new Error(data.detail || "API Error");
      }

      setMessages((prev) => [
        ...prev,
        { role: "ai", content: data.reply || "Error: No reply generated.", intent: data.intent, timestamp: new Date() },
      ]);
      
      if (!currentConversationId && data.conversation_id) {
        setCurrentConversationId(data.conversation_id);
      }
      fetchConversations();
    } catch (error: any) {
      toast(error.message || "Failed to send message", "error");
      // Remove the optimistic user message or let them know it failed. For simplicity, we just toast the error.
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    e.target.value = '';
    setMessages((prev) => [...prev, { role: "user", content: `Uploaded document: ${file.name}`, timestamp: new Date() }]);
    setLoading(true);

    try {
      const token = Cookies.get("token");
      const formData = new FormData();
      formData.append("file", file);
      
      let targetId = currentConversationId;
      if (!targetId) {
        targetId = crypto.randomUUID();
        formData.append("conversation_id", targetId);
        setCurrentConversationId(targetId);
      } else {
        formData.append("conversation_id", targetId);
      }
      
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/documents/analyze`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` },
        body: formData,
      });

      if (!res.ok) throw new Error("Analysis failed");

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "ai", content: data.analysis, intent: "Document Analysis", timestamp: new Date() },
      ]);
      fetchConversations();
    } catch (error: any) {
      toast("Could not analyze this document. Ensure it is a valid PDF.", "error");
    } finally {
      setLoading(false);
    }
  };

  // Render Sidebar Content to be used in both desktop and mobile
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
          className="w-full flex items-center justify-center gap-2 h-[40px] bg-[var(--color-bg-base)] border border-[var(--color-border-dim)] text-[var(--color-accent)] hover:bg-[var(--color-accent-muted)] hover:border-[var(--color-border-accent)] rounded-lg transition-all text-[14px] font-medium shadow-sm"
        >
          <span className="text-[18px] leading-none">+</span> New chat
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
                  className={`group flex items-center justify-between w-full h-[36px] px-3 rounded transition-colors cursor-pointer ${
                    isActive 
                      ? 'bg-[var(--color-accent-muted)] border-l-2 border-[var(--color-accent)] pl-2.5' 
                      : 'border-l-2 border-transparent hover:bg-[var(--color-bg-elevated)]'
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
    <ProtectedRoute>
      <div className="flex h-screen bg-[var(--color-bg-base)] text-[var(--color-text-primary)] overflow-hidden selection:bg-[var(--color-accent)] selection:text-[#080808]">
        
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

        {/* MAIN CHAT AREA */}
        <div className="flex-1 flex flex-col relative min-w-0">
          
          {/* TOP BAR */}
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

          {/* MESSAGES */}
          <div className="flex-1 overflow-y-auto pt-8 pb-[100px] px-4 scrollbar-thin">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center max-w-[560px] mx-auto pb-12">
                <div className="w-12 h-12 flex items-center justify-center mb-6 text-[var(--color-accent)]">
                  <Scale className="w-10 h-10 stroke-[1.5]" />
                </div>
                <h2 className="font-heading font-medium text-[22px] text-[var(--color-text-primary)] text-center mb-2">
                  What legal matter can I help with?
                </h2>
                <p className="text-[14px] text-[var(--color-text-secondary)] text-center mb-10 max-w-[360px] leading-relaxed">
                  Describe your situation in plain language. I'll identify the right legal path and draft your documents.
                </p>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full">
                  {SUGGESTED_PROMPTS.map((prompt, idx) => (
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
                          {msg.timestamp ? msg.timestamp.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ''}
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
                              {msg.timestamp ? msg.timestamp.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ''}
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
                                code: ({node, inline, ...props}: any) => 
                                  inline 
                                    ? <code className="font-mono text-[13px] bg-[var(--color-bg-subtle)] px-1.5 py-0.5 rounded text-[var(--color-text-primary)]" {...props} />
                                    : <code className="block font-mono text-[13px] bg-[var(--color-bg-subtle)] p-4 rounded border border-[var(--color-border-dim)] overflow-x-auto my-4 whitespace-pre-wrap" {...props} />,
                              }}
                            >
                              {msg.content}
                            </ReactMarkdown>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}

                {/* LOADING INDICATOR */}
                {loading && (
                  <div className="flex items-start gap-3 w-full pl-4 border-l-2 border-[var(--color-border-accent)] opacity-80">
                    <div className="flex flex-col gap-2">
                      <div className="flex items-center gap-1.5 h-[20px]">
                        <div className="w-1.5 h-1.5 rounded-full bg-[var(--color-accent)] animate-pulse"></div>
                        <div className="w-1.5 h-1.5 rounded-full bg-[var(--color-accent)] animate-pulse" style={{ animationDelay: '150ms' }}></div>
                        <div className="w-1.5 h-1.5 rounded-full bg-[var(--color-accent)] animate-pulse" style={{ animationDelay: '300ms' }}></div>
                      </div>
                      <div className="text-[12px] font-medium text-[var(--color-text-secondary)] transition-opacity duration-300">
                        {LOADING_STATUSES[loadingStatusIdx]}
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} className="h-1" />
              </div>
            )}
          </div>

          {/* INPUT BAR */}
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

        </div>
      </div>
    </ProtectedRoute>
  );
}
