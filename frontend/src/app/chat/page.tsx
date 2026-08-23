"use client";

import { useState, useRef, useEffect } from "react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import Cookies from "js-cookie";
import { useToast } from "@/hooks/useToast";
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';

import { ChatSidebar, Conversation } from "@/components/chat/ChatSidebar";
import { ChatHeader } from "@/components/chat/ChatHeader";
import { ChatMessageList, Message } from "@/components/chat/ChatMessageList";
import { ChatInput } from "@/components/chat/ChatInput";

const SUGGESTED_PROMPTS = [
  "Draft an RTI application",
  "File a consumer complaint",
  "Send a legal notice",
  "Explain my tenant rights"
];
const API_URL = process.env.NEXT_PUBLIC_API_URL || (process.env.NODE_ENV === "development" ? "http://127.0.0.1:8000" : "https://jansathi-ahwr.onrender.com");

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [fetchingSidebar, setFetchingSidebar] = useState(true);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const exportRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const fetchConversations = async () => {
    setFetchingSidebar(true);
    try {
      const token = Cookies.get("token");
      const res = await fetch(`${API_URL}/api/chat/conversations`, {
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

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
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
      const res = await fetch(`${API_URL}/api/chat/conversations/${id}`, {
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
      const res = await fetch(`${API_URL}/api/chat/conversations/${id}`, {
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
      const res = await fetch(`${API_URL}/api/chat/`, {
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
      
      const res = await fetch(`${API_URL}/api/documents/analyze`, {
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

  const exportToPDF = async () => {
    if (!exportRef.current) return;
    if (messages.length === 0) {
      toast("No messages to export", "info");
      return;
    }
    
    try {
      toast("Generating PDF...", "info");
      const element = exportRef.current;
      const originalHeight = element.style.height;
      const originalOverflow = element.style.overflow;
      
      // Temporarily expand to prevent cutoff inside scroll container
      element.style.height = 'max-content';
      element.style.overflow = 'visible';

      const canvas = await html2canvas(element, {
        scale: 2,
        useCORS: true,
        logging: false,
        backgroundColor: document.documentElement.getAttribute('data-theme') === 'light' ? "#ffffff" : "#0a0a0a",
        windowWidth: element.scrollWidth,
        windowHeight: element.scrollHeight
      });

      element.style.height = originalHeight;
      element.style.overflow = originalOverflow;
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'px',
        format: [canvas.width, canvas.height]
      });
      pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);
      const filename = `JanSaathi_Chat_${new Date().toISOString().split('T')[0]}.pdf`;
      pdf.save(filename);
      toast("PDF exported successfully", "success");
    } catch (e) {
      console.error(e);
      toast("Failed to generate PDF", "error");
    }
  };

  return (
    <ProtectedRoute>
      <div className="flex h-screen bg-[var(--color-bg-base)] text-[var(--color-text-primary)] overflow-hidden selection:bg-[var(--color-accent)] selection:text-[#080808]">
        
        <ChatSidebar 
          isSidebarOpen={isSidebarOpen}
          setIsSidebarOpen={setIsSidebarOpen}
          isSidebarCollapsed={isSidebarCollapsed}
          setIsSidebarCollapsed={setIsSidebarCollapsed}
          fetchingSidebar={fetchingSidebar}
          conversations={conversations}
          currentConversationId={currentConversationId}
          loadConversation={loadConversation}
          startNewChat={startNewChat}
          deleteConversation={deleteConversation}
        />

        {/* MAIN CHAT AREA */}
        <div className="flex-1 flex flex-col relative min-w-0">
          
          <ChatHeader 
            setIsSidebarOpen={setIsSidebarOpen}
            isSidebarCollapsed={isSidebarCollapsed}
            setIsSidebarCollapsed={setIsSidebarCollapsed}
            exportToPDF={exportToPDF}
          />

          <ChatMessageList 
            messages={messages}
            loading={loading}
            setInput={setInput}
            textareaRef={textareaRef}
            messagesEndRef={messagesEndRef}
            suggestedPrompts={SUGGESTED_PROMPTS}
            exportRef={exportRef}
          />

          <ChatInput 
            input={input}
            handleInput={handleInput}
            handleKeyDown={handleKeyDown}
            sendMessage={sendMessage}
            loading={loading}
            textareaRef={textareaRef}
            handleFileUpload={handleFileUpload}
          />

        </div>
      </div>
    </ProtectedRoute>
  );
}
