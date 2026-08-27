"use client";

import { useAuth } from "../lib/auth";
import { useRouter, usePathname } from "next/navigation";
import { useEffect, ReactNode } from "react";
import { Loader2 } from "lucide-react";

export function ProtectedRoute({ children }: { children: ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!isLoading && !isAuthenticated && pathname !== "/login") {
      router.push("/login");
    }
  }, [isLoading, isAuthenticated, pathname, router]);

  if (isLoading) {
    return (
      <div className="flex h-screen w-full items-center justify-center bg-[var(--color-bg-base)] overflow-hidden relative">
        {/* Top indeterminate progress bar */}
        <div className="absolute top-0 left-0 right-0 h-[2px] bg-[var(--color-bg-elevated)] overflow-hidden">
          <div className="h-full bg-[var(--color-accent)] w-1/3 animate-[progress_1.5s_ease-in-out_infinite]" style={{ transformOrigin: 'left' }} />
        </div>
        
        {/* Wordmark */}
        <div className="font-heading font-medium text-[22px] text-[var(--color-accent)] tracking-tight animate-pulse">
          JanSaathi
        </div>
        
        {/* Progress animation keyframes injected here for simplicity */}
        <style dangerouslySetInnerHTML={{__html: `
          @keyframes progress {
            0% { transform: translateX(-100%); }
            50% { transform: translateX(100%); width: 2/3; }
            100% { transform: translateX(300%); }
          }
        `}} />
      </div>
    );
  }

  if (!isAuthenticated && pathname !== "/login") {
    return null;
  }

  return <>{children}</>;
}
