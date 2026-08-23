"use client";

import { useToast } from "@/hooks/useToast";
import { X } from "lucide-react";
import { useEffect, useState } from "react";

export function ToastContainer() {
  const { toasts, dismissToast } = useToast();

  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-2 pointer-events-none">
      {toasts.map((t) => (
        <ToastItem key={t.id} toast={t} onDismiss={() => dismissToast(t.id)} />
      ))}
    </div>
  );
}

function ToastItem({ toast, onDismiss }: { toast: any; onDismiss: () => void }) {
  const [isShowing, setIsShowing] = useState(false);
  const [isLeaving, setIsLeaving] = useState(false);

  useEffect(() => {
    // Trigger entry animation
    requestAnimationFrame(() => {
      setIsShowing(true);
    });

    // Cleanup happens via the hook, but we want to trigger exit animation right before
    const timer = setTimeout(() => {
      setIsLeaving(true);
    }, 3850); // 150ms before the actual 4000ms dismissal

    return () => clearTimeout(timer);
  }, []);

  const handleClose = () => {
    setIsLeaving(true);
    setTimeout(onDismiss, 150);
  };

  const dotColors = {
    error: "bg-[var(--color-semantic-red)]",
    success: "bg-[var(--color-semantic-green)]",
    info: "bg-[var(--color-accent)]",
  };

  return (
    <div
      className={`
        pointer-events-auto flex items-center justify-between w-[320px] 
        bg-[var(--color-bg-elevated)] border border-[var(--color-border-strong)] 
        rounded-lg py-3 px-3.5 shadow-xl
        transition-all duration-150 ease-out
        ${isShowing && !isLeaving ? "translate-x-0 opacity-100" : "translate-x-8 opacity-0"}
      `}
    >
      <div className="flex items-center gap-3 overflow-hidden">
        <div className={`w-1.5 h-1.5 rounded-full shrink-0 ${dotColors[toast.type as keyof typeof dotColors]}`} />
        <p className="text-[13px] font-medium text-[var(--color-text-primary)] truncate">
          {toast.message}
        </p>
      </div>
      <button
        onClick={handleClose}
        className="ml-3 shrink-0 text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)] transition-colors"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
}
