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
    <div className="flex min-h-screen items-center justify-center bg-[#050505] p-4 font-sans selection:bg-white selection:text-black relative overflow-hidden">
      
      {/* Background Ambient Glows */}
      <div className="absolute top-[-10%] left-[-10%] w-[40vw] h-[40vw] rounded-full bg-blue-900/20 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40vw] h-[40vw] rounded-full bg-purple-900/20 blur-[120px] pointer-events-none" />
      
      {/* Grid Pattern */}
      <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-overlay pointer-events-none" />
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_60%_60%_at_50%_50%,#000_10%,transparent_100%)] pointer-events-none" />

      <div className="w-full max-w-[420px] space-y-8 rounded-2xl bg-black/40 backdrop-blur-xl p-10 border border-white/10 shadow-2xl relative z-10">
        
        <div className="text-center space-y-3">
          <div className="inline-flex items-center justify-center px-3 py-1 mb-4 rounded-full bg-white/5 border border-white/10 text-xs font-medium text-gray-300">
            <span className="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></span>
            System Online
          </div>
          <h2 className="text-4xl font-bold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-white via-gray-200 to-gray-400">
            JanSaathi
          </h2>
          <p className="text-sm text-gray-400 font-medium">
            India's AI Legal & Civic Advisor
          </p>
        </div>

        <div className="flex border-b border-white/10 pb-4 gap-6 relative">
          <button
            onClick={() => setIsLogin(true)}
            className={`text-sm font-medium transition-all ${
              isLogin ? "text-white" : "text-gray-500 hover:text-gray-300"
            }`}
          >
            Log in
            {isLogin && <div className="absolute bottom-[-1px] left-0 h-[2px] w-10 bg-white rounded-t-full transition-all" />}
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`text-sm font-medium transition-all ${
              !isLogin ? "text-white" : "text-gray-500 hover:text-gray-300"
            }`}
          >
            Create account
            {!isLogin && <div className="absolute bottom-[-1px] left-[68px] h-[2px] w-24 bg-white rounded-t-full transition-all" />}
          </button>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="rounded-lg bg-red-500/10 p-4 border border-red-500/20 backdrop-blur-sm animate-in fade-in slide-in-from-top-2">
              <p className="text-sm text-red-400 flex items-center gap-2">
                <span className="text-lg">⚠️</span> {error}
              </p>
            </div>
          )}

          <div className="space-y-4">
            {!isLogin && (
              <div className="space-y-2">
                <label className="text-xs font-medium text-gray-400 uppercase tracking-wider">Full Name</label>
                <div className="relative">
                  <User className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
                  <input
                    id="name"
                    name="name"
                    type="text"
                    required
                    className="block w-full rounded-lg bg-white/5 py-2.5 pl-10 pr-3 text-sm text-white placeholder-gray-500 border border-white/10 focus:border-white focus:bg-white/10 focus:outline-none transition-all"
                    placeholder="John Doe"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                </div>
              </div>
            )}
            
            <div className="space-y-2">
              <label className="text-xs font-medium text-gray-400 uppercase tracking-wider">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="block w-full rounded-lg bg-white/5 py-2.5 pl-10 pr-3 text-sm text-white placeholder-gray-500 border border-white/10 focus:border-white focus:bg-white/10 focus:outline-none transition-all"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label className="text-xs font-medium text-gray-400 uppercase tracking-wider">Password</label>
              </div>
              <div className="relative">
                <Lock className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete={isLogin ? "current-password" : "new-password"}
                  required
                  className="block w-full rounded-lg bg-white/5 py-2.5 pl-10 pr-3 text-sm text-white placeholder-gray-500 border border-white/10 focus:border-white focus:bg-white/10 focus:outline-none transition-all"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>
          </div>

          <div className="pt-4">
            <button
              type="submit"
              disabled={loading}
              className="group flex w-full items-center justify-center gap-2 rounded-lg bg-white py-3 px-4 text-sm font-semibold text-black hover:bg-gray-200 disabled:opacity-50 transition-all active:scale-[0.98]"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <>
                  {isLogin ? "Access Dashboard" : "Create Account"}
                  <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
