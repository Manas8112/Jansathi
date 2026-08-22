"use client";

import { useState } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { Loader2, Mail, Lock, User, ArrowRight } from "lucide-react";

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
    <div className="flex min-h-screen items-center justify-center bg-black p-4 font-sans selection:bg-white selection:text-black">
      <div className="w-full max-w-[400px] space-y-8 rounded-lg bg-black p-10 border border-[#1a1a1a]">
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-bold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-white to-[#888]">
            JanSaathi
          </h2>
          <p className="text-sm text-[#888] font-medium">
            India's AI Legal & Civic Advisor
          </p>
        </div>

        <div className="flex border-b border-[#1a1a1a] pb-4 gap-6">
          <button
            onClick={() => setIsLogin(true)}
            className={`text-sm font-medium transition-colors ${
              isLogin ? "text-white" : "text-[#666] hover:text-white"
            }`}
          >
            Log in
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`text-sm font-medium transition-colors ${
              !isLogin ? "text-white" : "text-[#666] hover:text-white"
            }`}
          >
            Create account
          </button>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="rounded-md bg-red-500/10 p-4 border border-red-500/20">
              <p className="text-sm text-red-400">{error}</p>
            </div>
          )}

          <div className="space-y-4">
            {!isLogin && (
              <div className="space-y-1.5">
                <label className="text-xs font-medium text-[#888]">Full Name</label>
                <input
                  id="name"
                  name="name"
                  type="text"
                  required
                  className="block w-full rounded bg-black py-2.5 px-3 text-sm text-white placeholder-[#444] border border-[#222] focus:border-white focus:outline-none transition-colors"
                  placeholder="John Doe"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>
            )}
            
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-[#888]">Email Address</label>
              <input
                id="email-address"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="block w-full rounded bg-black py-2.5 px-3 text-sm text-white placeholder-[#444] border border-[#222] focus:border-white focus:outline-none transition-colors"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            
            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <label className="text-xs font-medium text-[#888]">Password</label>
              </div>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete={isLogin ? "current-password" : "new-password"}
                required
                className="block w-full rounded bg-black py-2.5 px-3 text-sm text-white placeholder-[#444] border border-[#222] focus:border-white focus:outline-none transition-colors"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <div className="pt-2">
            <button
              type="submit"
              disabled={loading}
              className="flex w-full items-center justify-center gap-2 rounded bg-white py-2.5 px-4 text-sm font-medium text-black hover:bg-gray-200 disabled:opacity-50 transition-colors"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <>
                  {isLogin ? "Continue" : "Sign up"}
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
