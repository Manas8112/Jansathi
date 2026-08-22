"use client";

import Link from "next/link";
import { ArrowRight, Scale, Shield, FileText } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white flex flex-col items-center justify-center relative overflow-hidden">
      
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-600/20 blur-[120px] rounded-full pointer-events-none"></div>

      <div className="z-10 max-w-5xl mx-auto px-6 text-center">
        
        {/* Logo/Icon */}
        <div className="flex justify-center mb-8">
          <div className="p-4 bg-blue-500/10 rounded-2xl border border-blue-500/20">
            <Scale className="w-12 h-12 text-blue-400" />
          </div>
        </div>

        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6">
          Legal Empowerment, <br className="hidden md:block" />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400">
            Powered by AI.
          </span>
        </h1>
        
        <p className="text-lg md:text-xl text-gray-400 mb-10 max-w-2xl mx-auto leading-relaxed">
          JanSaathi is an intelligent legal assistant that drafts RTI applications, consumer complaints, and legal notices for you in seconds. Navigate the Indian legal system with confidence.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link 
            href="/chat"
            className="group px-8 py-4 bg-white text-black font-semibold rounded-full hover:bg-gray-100 transition-all flex items-center gap-2 hover:scale-105 active:scale-95"
          >
            Start Free Consultation
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
          <Link 
            href="/login"
            className="px-8 py-4 bg-[#1a1a1a] border border-[#333] text-white font-semibold rounded-full hover:bg-[#222] transition-colors"
          >
            Sign In
          </Link>
        </div>

        {/* Feature Grid */}
        <div className="grid md:grid-cols-3 gap-6 mt-24 text-left">
          <div className="p-6 bg-[#121212] border border-[#222] rounded-2xl">
            <Shield className="w-8 h-8 text-purple-400 mb-4" />
            <h3 className="text-xl font-bold mb-2">Intent Recognition</h3>
            <p className="text-gray-400 text-sm">Fine-tuned InLegalBERT models instantly route your case to the correct legal procedure.</p>
          </div>
          <div className="p-6 bg-[#121212] border border-[#222] rounded-2xl">
            <Scale className="w-8 h-8 text-blue-400 mb-4" />
            <h3 className="text-xl font-bold mb-2">Hybrid RAG</h3>
            <p className="text-gray-400 text-sm">Retrieves exact sections from Indian Bare Acts and Supreme Court precedents using vector search.</p>
          </div>
          <div className="p-6 bg-[#121212] border border-[#222] rounded-2xl">
            <FileText className="w-8 h-8 text-green-400 mb-4" />
            <h3 className="text-xl font-bold mb-2">Document Generation</h3>
            <p className="text-gray-400 text-sm">Automatically drafts perfectly formatted RTI and Court complaints ready for download.</p>
          </div>
        </div>

      </div>
    </div>
  );
}
