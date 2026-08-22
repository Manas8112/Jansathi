"use client";

import { useState } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { Mail, Lock, User } from "lucide-react";

export default function LoginPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const endpoint = isLogin ? "/api/auth/login" : "/api/auth/register";
      const body = isLogin 
        ? JSON.stringify({ email, password })
        : JSON.stringify({ email, name, password });

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body,
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Authentication failed");
      }

      login(data.access_token, data.user);
      router.push("/chat");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[var(--color-bg-base)] flex items-center justify-center p-4 font-sans selection:bg-[var(--color-accent)] selection:text-[#080808]">
      
      <div className="w-full max-w-[400px] bg-[var(--color-bg-surface)] border border-[var(--color-border-strong)] rounded-xl p-8 shadow-2xl">
        
        {/* Header */}
        <div className="text-center pb-6 border-b border-[var(--color-border-dim)] mb-6">
          <h1 className="font-heading font-medium text-[18px] text-[var(--color-accent)] tracking-tight">
            JanSaathi
          </h1>
        </div>

        {/* Tabs */}
        <div className="flex relative mb-8">
          <button
            type="button"
            onClick={() => { setIsLogin(true); setError(""); }}
            className={`flex-1 pb-3 text-[14px] font-medium transition-colors ${
              isLogin ? "text-[var(--color-text-primary)]" : "text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]"
            }`}
          >
            Log in
          </button>
          <button
            type="button"
            onClick={() => { setIsLogin(false); setError(""); }}
            className={`flex-1 pb-3 text-[14px] font-medium transition-colors ${
              !isLogin ? "text-[var(--color-text-primary)]" : "text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]"
            }`}
          >
            Create account
          </button>
          {/* Animated Indicator */}
          <div 
            className="absolute bottom-0 h-[2px] bg-[var(--color-accent)] transition-all duration-150 ease-out"
            style={{ 
              width: "50%", 
              left: isLogin ? "0%" : "50%" 
            }} 
          />
          {/* Base border line */}
          <div className="absolute bottom-0 w-full h-[1px] bg-[var(--color-border-dim)] -z-10" />
        </div>

        {/* Form */}
        <form className="space-y-4" onSubmit={handleSubmit}>
          {!isLogin && (
            <div className="relative">
              <User className="absolute left-3.5 top-1/2 -translate-y-1/2 h-[18px] w-[18px] text-[var(--color-text-muted)]" />
              <input
                id="name"
                type="text"
                required
                placeholder="Full Name"
                className="w-full h-[44px] pl-11 pr-4 bg-[var(--color-bg-subtle)] border border-[var(--color-border-dim)] rounded-lg text-[14px] text-[var(--color-text-primary)] placeholder-[var(--color-text-muted)] focus:outline-none focus:border-[var(--color-accent)] focus:ring-0 transition-colors"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
          )}
          
          <div className="relative">
            <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 h-[18px] w-[18px] text-[var(--color-text-muted)]" />
            <input
              id="email-address"
              type="email"
              autoComplete="email"
              required
              placeholder="Email address"
              className="w-full h-[44px] pl-11 pr-4 bg-[var(--color-bg-subtle)] border border-[var(--color-border-dim)] rounded-lg text-[14px] text-[var(--color-text-primary)] placeholder-[var(--color-text-muted)] focus:outline-none focus:border-[var(--color-accent)] focus:ring-0 transition-colors"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          
          <div className="relative">
            <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 h-[18px] w-[18px] text-[var(--color-text-muted)]" />
            <input
              id="password"
              type="password"
              autoComplete={isLogin ? "current-password" : "new-password"}
              required
              placeholder="Password"
              className="w-full h-[44px] pl-11 pr-4 bg-[var(--color-bg-subtle)] border border-[var(--color-border-dim)] rounded-lg text-[14px] text-[var(--color-text-primary)] placeholder-[var(--color-text-muted)] focus:outline-none focus:border-[var(--color-accent)] focus:ring-0 transition-colors"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          {error && (
            <p className="text-[12px] font-medium text-[var(--color-semantic-red)] mt-1 animate-in fade-in slide-in-from-top-1">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full h-[44px] mt-6 bg-[var(--color-accent)] hover:bg-[var(--color-accent-dim)] text-[#080808] font-heading font-medium text-[15px] rounded-lg transition-colors disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {loading ? (
              <svg className="animate-spin h-4 w-4 text-[#080808]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : (
              isLogin ? "Sign In" : "Create Account"
            )}
          </button>
        </form>

      </div>
    </div>
  );
}
