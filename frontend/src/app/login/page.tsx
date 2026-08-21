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
      router.push("/");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#0a0a12] p-4 font-sans">
      <div className="w-full max-w-md space-y-8 rounded-2xl bg-[#1a1a2e] p-8 shadow-2xl border border-[#2a2a3d]">
        <div className="text-center">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-[#e6a336]/10 mb-4">
            <span className="text-3xl text-[#e6a336]">🏛️</span>
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-[#f0f0f5]">
            JanSaathi
          </h2>
          <p className="mt-2 text-sm text-[#8888a0]">
            AI for Civic & Legal Empowerment
          </p>
        </div>

        <div className="flex rounded-lg bg-[#12121e] p-1">
          <button
            onClick={() => setIsLogin(true)}
            className={`flex-1 rounded-md py-2 text-sm font-medium transition-all ${
              isLogin 
                ? "bg-[#22223a] text-white shadow" 
                : "text-[#8888a0] hover:text-white"
            }`}
          >
            Login
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`flex-1 rounded-md py-2 text-sm font-medium transition-all ${
              !isLogin 
                ? "bg-[#22223a] text-white shadow" 
                : "text-[#8888a0] hover:text-white"
            }`}
          >
            Register
          </button>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="rounded-md bg-red-500/10 p-4 border border-red-500/20">
              <p className="text-sm text-red-400">{error}</p>
            </div>
          )}

          <div className="space-y-4 rounded-md shadow-sm">
            {!isLogin && (
              <div className="relative">
                <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <User className="h-5 w-5 text-[#55556a]" />
                </div>
                <input
                  id="name"
                  name="name"
                  type="text"
                  required
                  className="block w-full rounded-lg border border-[#2a2a3d] bg-[#12121e] py-3 pl-10 pr-3 text-white placeholder-[#55556a] focus:border-[#e6a336] focus:outline-none focus:ring-1 focus:ring-[#e6a336] sm:text-sm"
                  placeholder="Full Name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>
            )}
            
            <div className="relative">
              <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <Mail className="h-5 w-5 text-[#55556a]" />
              </div>
              <input
                id="email-address"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="block w-full rounded-lg border border-[#2a2a3d] bg-[#12121e] py-3 pl-10 pr-3 text-white placeholder-[#55556a] focus:border-[#e6a336] focus:outline-none focus:ring-1 focus:ring-[#e6a336] sm:text-sm"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            
            <div className="relative">
              <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <Lock className="h-5 w-5 text-[#55556a]" />
              </div>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete={isLogin ? "current-password" : "new-password"}
                required
                className="block w-full rounded-lg border border-[#2a2a3d] bg-[#12121e] py-3 pl-10 pr-3 text-white placeholder-[#55556a] focus:border-[#e6a336] focus:outline-none focus:ring-1 focus:ring-[#e6a336] sm:text-sm"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative flex w-full justify-center rounded-lg bg-[#e6a336] py-3 px-4 text-sm font-medium text-black hover:bg-[#f5c563] focus:outline-none focus:ring-2 focus:ring-[#e6a336] focus:ring-offset-2 focus:ring-offset-[#0a0a12] disabled:opacity-70 transition-all"
            >
              {loading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <>
                  {isLogin ? "Sign In" : "Create Account"}
                  <ArrowRight className="ml-2 h-4 w-4 opacity-0 transition-opacity group-hover:opacity-100" />
                </>
              )}
            </button>
          </div>
        </form>

        <div className="mt-6">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-[#2a2a3d]" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="bg-[#1a1a2e] px-2 text-[#8888a0]">
                Or continue with
              </span>
            </div>
          </div>

          <div className="mt-6">
            <button
              type="button"
              className="flex w-full items-center justify-center gap-3 rounded-lg border border-[#2a2a3d] bg-[#12121e] py-3 px-4 text-sm font-medium text-white hover:bg-[#22223a] transition-all"
            >
              <svg className="h-5 w-5" aria-hidden="true" viewBox="0 0 24 24">
                <path
                  d="M12.0003 4.75C13.7703 4.75 15.3553 5.36002 16.6053 6.54998L20.0303 3.125C17.9502 1.19 15.2353 0 12.0003 0C7.31028 0 3.25527 2.69 1.28027 6.60998L5.27028 9.70498C6.21525 6.86002 8.87028 4.75 12.0003 4.75Z"
                  fill="#EA4335"
                />
                <path
                  d="M23.49 12.275C23.49 11.49 23.415 10.73 23.3 10H12V14.51H18.47C18.18 15.99 17.34 17.25 16.08 18.1L19.945 21.1C22.2 19.01 23.49 15.92 23.49 12.275Z"
                  fill="#4285F4"
                />
                <path
                  d="M5.26498 14.2949C5.02498 13.5699 4.88501 12.7999 4.88501 11.9999C4.88501 11.1999 5.01998 10.4299 5.26498 9.7049L1.275 6.60986C0.46 8.22986 0 10.0599 0 11.9999C0 13.9399 0.46 15.7699 1.28 17.3899L5.26498 14.2949Z"
                  fill="#FBBC05"
                />
                <path
                  d="M12.0004 24.0001C15.2404 24.0001 17.9654 22.935 19.9454 21.095L16.0804 18.095C15.0054 18.82 13.6204 19.245 12.0004 19.245C8.8704 19.245 6.21537 17.135 5.2654 14.29L1.27539 17.385C3.25539 21.31 7.3104 24.0001 12.0004 24.0001Z"
                  fill="#34A853"
                />
              </svg>
              <span>Google</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
