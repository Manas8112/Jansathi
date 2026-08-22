"use client";

import { useState, useRef, useEffect } from "react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { UserMenu } from "@/components/UserMenu";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { Paperclip, Send, Terminal, User as UserIcon, Trash2 } from "lucide-react";
import Link from "next/link";
import Cookies from "js-cookie";

interface Message {
  role: "user" | "ai";
  content: string;
  intent?: string;
}

interface Conversation {
  id: string;
  title: string;
  updated_at: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingStatus, setLoadingStatus] = useState("Analyzing legal context...");
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Fetch conversation history on mount
  const fetchConversations = async () => {
    try {
      const token = Cookies.get("token");
      const res = await fetch("http://127.0.0.1:8000/api/chat/conversations", {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setConversations(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchConversations();
  }, []);

  const loadConversation = async (id: string) => {
    setLoading(true);
    try {
      const token = Cookies.get("token");
      const res = await fetch(`http://127.0.0.1:8000/api/chat/conversations/${id}`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setMessages(data);
        setCurrentConversationId(id);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const startNewChat = () => {
    setMessages([]);
    setCurrentConversationId(null);
  };

  const deleteConversation = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (!confirm("⚠️ Are you sure you want to delete this ENTIRE chat?\n\n(If you just want to delete a saved PDF, please go to the 'My Documents' page instead. Deleting this chat will erase all message history!)")) return;
    
    try {
      const token = Cookies.get("token");
      const res = await fetch(`http://127.0.0.1:8000/api/chat/conversations/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        if (currentConversationId === id) {
          startNewChat();
        }
        fetchConversations();
      }
    } catch (e) {
      console.error("Failed to delete chat", e);
    }
  };

  // Cycle loading status text
  useEffect(() => {
    if (loading) {
      const statuses = [
        "Analyzing legal context...",
        "Searching knowledge graph...",
        "Evaluating jurisdiction...",
        "Drafting response..."
      ];
      let i = 0;
      setLoadingStatus(statuses[0]);
      const interval = setInterval(() => {
        i = (i + 1) % statuses.length;
        setLoadingStatus(statuses[i]);
      }, 2500);
      return () => clearInterval(interval);
    }
  }, [loading]);



  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);

    try {
      const token = Cookies.get("token");
      const res = await fetch("http://127.0.0.1:8000/api/chat/", {
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
        { role: "ai", content: data.reply || "Error: No reply generated.", intent: data.intent },
      ]);
      
      if (!currentConversationId) {
        setCurrentConversationId(data.conversation_id);
      }
      // Refresh the sidebar
      fetchConversations();
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { role: "ai", content: "Sorry, I am having trouble connecting to the backend right now." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    // Clear the input
    e.target.value = '';
    
    setMessages((prev) => [...prev, { role: "user", content: `Uploaded document: ${file.name}` }]);
    setLoading(true);

    try {
      const token = Cookies.get("token");
      const formData = new FormData();
      formData.append("file", file);
      if (currentConversationId) {
        formData.append("conversation_id", currentConversationId);
      } else {
        // If no conversation exists yet, create an ID to bind the file to
        const newId = crypto.randomUUID();
        formData.append("conversation_id", newId);
        setCurrentConversationId(newId);
      }
      
      const res = await fetch("http://127.0.0.1:8000/api/documents/analyze", {
        method: "POST",
        headers: { 
          "Authorization": `Bearer ${token}` 
        },
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Analysis failed");
      }

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "ai", content: data.analysis, intent: "Contract Analysis" },
      ]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { role: "ai", content: "Sorry, I could not analyze this document. Ensure it is a valid PDF." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ProtectedRoute>
      <div className="flex h-screen bg-black text-white overflow-hidden selection:bg-white selection:text-black">
        
        {/* Sidebar (Roadmap & Documents preview) */}
        <div className="w-80 bg-black border-r border-[#1a1a1a] p-6 hidden md:flex flex-col">
          <div className="text-xl font-semibold tracking-tight mb-8 text-white">JanSaathi</div>
          
          <button 
            onClick={startNewChat}
            className="w-full flex items-center justify-center gap-2 mb-6 px-4 py-3 bg-white text-black hover:bg-gray-200 rounded font-medium transition-colors"
          >
            <span className="text-lg">+</span> New Chat
          </button>
          
          <div className="flex-1 overflow-y-auto mb-4 scrollbar-thin scrollbar-thumb-[#333] pr-2">
            <h3 className="text-xs font-semibold text-[#888] uppercase tracking-wider mb-4 sticky top-0 bg-black pt-2 pb-2 z-10">Recent Chats</h3>
            {conversations.length === 0 ? (
              <div className="text-sm text-[#555] italic">No past conversations.</div>
            ) : (
              <div className="space-y-1">
                {conversations.map((conv) => (
                  <div key={conv.id} className={`flex items-center justify-between w-full rounded transition-colors group ${currentConversationId === conv.id ? 'bg-[#222] text-white' : 'text-[#888] hover:bg-[#111] hover:text-white'}`}>
                    <button
                      onClick={() => loadConversation(conv.id)}
                      className="flex-1 text-left px-3 py-2.5 text-sm truncate"
                    >
                      {conv.title || "New Chat"}
                    </button>
                    <button 
                      onClick={(e) => deleteConversation(e, conv.id)}
                      className="p-2 opacity-0 group-hover:opacity-100 hover:text-red-400 transition-opacity"
                      title="Delete chat"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
          
          <div className="mb-4">
            <Link href="/dashboard" className="flex items-center gap-3 w-full px-4 py-3 bg-black hover:bg-[#111] border border-[#222] rounded text-white transition-colors cursor-pointer">
              <span className="text-lg">📄</span>
              <span className="font-medium text-sm">My Documents</span>
            </Link>
          </div>
          
          <div className="mt-auto pb-4">
            <UserMenu />
          </div>
        </div>

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col relative bg-black">
          
          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto p-4 md:p-8 scrollbar-thin scrollbar-thumb-[#333] scrollbar-track-transparent">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center max-w-2xl mx-auto">
                <div className="w-12 h-12 rounded bg-white flex items-center justify-center mb-6">
                  <Terminal size={24} className="text-black" />
                </div>
                <h1 className="text-2xl font-medium mb-4 text-white tracking-tight">
                  How can I help you today?
                </h1>
                <p className="text-[#888] text-[15px] leading-relaxed max-w-md">
                  Analyze legal contracts, draft RTI applications, and get guidance on consumer complaints in plain language.
                </p>
              </div>
            ) : (
              <div className="max-w-3xl mx-auto space-y-10 pb-4">
                {messages.map((msg, i) => (
                  <div key={i} className="flex gap-5 group">
                    <div className="flex-shrink-0 mt-1">
                      {msg.role === "user" ? (
                        <div className="h-7 w-7 rounded bg-[#222] flex items-center justify-center text-[#ccc]">
                          <UserIcon size={14} />
                        </div>
                      ) : (
                        <div className="h-7 w-7 rounded bg-white flex items-center justify-center text-black">
                          <Terminal size={14} />
                        </div>
                      )}
                    </div>
                    
                    <div className="flex-1 space-y-2 overflow-hidden min-w-0">
                      <div className="flex items-center gap-3">
                        <span className="font-semibold text-[13px] text-white">
                          {msg.role === "user" ? "You" : "JanSaathi"}
                        </span>
                        {msg.intent && (
                          <span className="font-mono text-[10px] px-1.5 py-0.5 rounded bg-[#111] text-[#888] border border-[#222]">
                            {msg.intent}
                          </span>
                        )}
                      </div>
                      
                      <div className={msg.role === "user" ? "text-[#eee] text-[15px] leading-relaxed whitespace-pre-wrap" : "prose prose-invert prose-p:leading-relaxed prose-pre:bg-[#111] prose-pre:border prose-pre:border-[#222] prose-td:border-[#222] prose-th:border-[#222] prose-a:text-white prose-a:underline max-w-none text-[#eee] text-[15px]"}>
                        {msg.role === "user" ? (
                          msg.content
                        ) : (
                          <ReactMarkdown 
                            remarkPlugins={[remarkGfm]}
                            rehypePlugins={[rehypeRaw]}
                            components={{
                              a: ({node, ...props}) => {
                                let href = props.href;
                                if (href) {
                                  // Clean up any markdown asterisks the AI accidentally put inside the URL
                                  href = href.replace(/%2A/gi, '').replace(/\*/g, '');
                                  if (!href.startsWith('http') && !href.startsWith('/')) {
                                    href = `https://${href}`;
                                  }
                                }
                                return <a {...props} href={href} target={href?.startsWith('/') ? undefined : "_blank"} rel="noopener noreferrer" className="text-white font-medium hover:text-[#ccc] underline decoration-[#555] underline-offset-4 transition-colors cursor-pointer" />;
                              }
                            }}
                          >
                            {msg.content.replace(/(?<!\]\()(https?:\/\/[^\s)]+)/g, '[$1]($1)')}
                          </ReactMarkdown>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                
                {loading && (
                  <div className="flex gap-5">
                    <div className="flex-shrink-0 mt-1">
                      <div className="h-7 w-7 rounded bg-[#111] border border-[#222] flex items-center justify-center text-[#888]">
                        <Terminal size={14} />
                      </div>
                    </div>
                    <div className="flex items-center gap-3 h-7">
                      <span className="text-[#666] font-mono text-xs">{loadingStatus}</span>
                      <div className="flex space-x-1">
                        <div className="w-1 h-1 bg-[#666] rounded-full animate-bounce"></div>
                        <div className="w-1 h-1 bg-[#666] rounded-full animate-bounce delay-150"></div>
                        <div className="w-1 h-1 bg-[#666] rounded-full animate-bounce delay-300"></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Input Box - Strict Flex Column (No absolute overlap) */}
          <div className="w-full bg-black shrink-0 px-4 pt-2 pb-6 border-t border-[#111]">
            <div className="max-w-3xl mx-auto">
              <form onSubmit={sendMessage} className="relative flex items-center bg-[#0a0a0a] border border-[#222] rounded focus-within:border-[#555] transition-colors">
                <input
                  type="file"
                  id="file-upload"
                  accept="application/pdf"
                  className="hidden"
                  onChange={handleFileUpload}
                  disabled={loading}
                />
                <label htmlFor="file-upload" className="p-3 ml-1 rounded hover:bg-[#111] cursor-pointer text-[#666] hover:text-white transition-colors z-10" title="Upload contract or lease">
                  <Paperclip size={18} />
                </label>
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Message JanSaathi..."
                  className="w-full bg-transparent border-none py-3.5 px-2 text-white placeholder-[#555] focus:outline-none focus:ring-0 text-[15px]"
                  disabled={loading}
                  autoComplete="off"
                />
                <button 
                  type="submit" 
                  disabled={!input.trim() || loading}
                  className="p-1.5 mr-2 rounded bg-white text-black hover:bg-gray-200 disabled:opacity-50 disabled:bg-[#222] disabled:text-[#666] transition-colors"
                >
                  <Send size={16} className={input.trim() ? "translate-x-0.5" : ""} />
                </button>
              </form>
              <div className="text-center mt-2 text-[10px] text-[#555] font-mono">
                JanSaathi is an AI and can make mistakes. Verify critical legal information.
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </ProtectedRoute>
  );
}
