"use client";

import { useState, useEffect, useCallback } from "react";

export type ToastType = "error" | "success" | "info";

export interface ToastMessage {
  id: string;
  message: string;
  type: ToastType;
}

// Simple event emitter for global toast state without needing context wrappers everywhere
type Listener = (toast: ToastMessage) => void;
const listeners = new Set<Listener>();

export const toast = (message: string, type: ToastType = "info") => {
  const id = Math.random().toString(36).substring(2, 9);
  const newToast = { id, message, type };
  listeners.forEach((listener) => listener(newToast));
};

export function useToast() {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  useEffect(() => {
    const handleToast = (newToast: ToastMessage) => {
      setToasts((prev) => [...prev, newToast]);
      // Auto-dismiss after 4000ms
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== newToast.id));
      }, 4000);
    };

    listeners.add(handleToast);
    return () => {
      listeners.delete(handleToast);
    };
  }, []);

  const dismissToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return { toasts, toast, dismissToast };
}
