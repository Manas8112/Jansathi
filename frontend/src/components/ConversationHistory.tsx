"use client";

import { useEffect, useState } from "react";
import { getConversations, deleteConversation } from "@/lib/api";
import { MessageSquare, Trash2, Clock, Loader2 } from "lucide-react";

type Conversation = {
  id: string;
  title: string;
  mode: string;
  updated_at: string;
};

export function ConversationHistory({ onSelect }: { onSelect: (id: string) => void }) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const data = await getConversations();
      setConversations(data);
    } catch (error) {
      console.error("Failed to fetch history:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    try {
      await deleteConversation(id);
      setConversations((prev) => prev.filter((c) => c.id !== id));
    } catch (error) {
      console.error("Failed to delete conversation:", error);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center p-4">
        <Loader2 className="h-5 w-5 animate-spin text-[#8888a0]" />
      </div>
    );
  }

  if (conversations.length === 0) {
    return (
      <div className="p-4 text-center text-sm text-[#55556a]">
        No previous conversations
      </div>
    );
  }

  return (
    <div className="space-y-1 p-2">
      <h3 className="mb-2 px-2 text-xs font-semibold uppercase tracking-wider text-[#55556a]">
        Recent Activity
      </h3>
      {conversations.map((conv) => (
        <div
          key={conv.id}
          onClick={() => onSelect(conv.id)}
          className="group flex cursor-pointer items-center justify-between rounded-lg p-2 hover:bg-[#1a1a2e] transition-colors"
        >
          <div className="flex items-center gap-3 overflow-hidden">
            <MessageSquare size={16} className="text-[#8888a0] shrink-0" />
            <div className="flex flex-col overflow-hidden">
              <span className="truncate text-sm font-medium text-[#d0d0e0] group-hover:text-white">
                {conv.title}
              </span>
              <span className="flex items-center gap-1 text-[10px] text-[#55556a]">
                <Clock size={10} />
                {new Date(conv.updated_at).toLocaleDateString()}
              </span>
            </div>
          </div>
          
          <button
            onClick={(e) => handleDelete(e, conv.id)}
            className="opacity-0 group-hover:opacity-100 p-1 text-[#55556a] hover:text-red-400 transition-all rounded-md hover:bg-[#22223a]"
          >
            <Trash2 size={14} />
          </button>
        </div>
      ))}
    </div>
  );
}
