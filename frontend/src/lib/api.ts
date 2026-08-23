import Cookies from "js-cookie";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
  const token = Cookies.get("token");
  
  const headers = new Headers(options.headers || {});
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  
  // Set default Content-Type if not provided and body is a string
  if (!headers.has("Content-Type") && typeof options.body === "string") {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    // Handle unauthorized (token expired or invalid)
    Cookies.remove("token");
    if (typeof window !== "undefined") {
      window.location.href = "/login";
    }
    throw new Error("Authentication required");
  }

  return response;
}

// Conversation API
export async function getConversations() {
  const res = await fetchWithAuth("/api/auth/conversations");
  if (!res.ok) throw new Error("Failed to fetch conversations");
  return res.json();
}

export async function getMessages(conversationId: string) {
  const res = await fetchWithAuth(`/api/auth/conversations/${conversationId}/messages`);
  if (!res.ok) throw new Error("Failed to fetch messages");
  return res.json();
}

export async function deleteConversation(conversationId: string) {
  const res = await fetchWithAuth(`/api/auth/conversations/${conversationId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete conversation");
  return res.json();
}

// Document API
export async function getSavedDocuments() {
  const res = await fetchWithAuth("/api/auth/documents");
  if (!res.ok) throw new Error("Failed to fetch documents");
  return res.json();
}

export async function saveDocument(data: { doc_type: string; title: string; content: string }) {
  const res = await fetchWithAuth("/api/auth/documents", {
    method: "POST",
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to save document");
  return res.json();
}

// AI API (to be implemented further in Phase 8)
export async function sendMessage(message: string, conversationId: string, mode: string) {
  return fetchWithAuth("/api/chat", {
    method: "POST",
    body: JSON.stringify({ message, conversation_id: conversationId, mode }),
  });
}
