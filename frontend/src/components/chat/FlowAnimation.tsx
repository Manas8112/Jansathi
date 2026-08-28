"use client";

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Database, FileText, Cpu, ShieldCheck, Activity } from "lucide-react";

const nodes = [
  { id: "intent", label: "Intent Router", desc: "Analyzing Query", icon: FileText, color: "text-blue-400", bg: "bg-blue-500/10", border: "border-blue-500/30", x: 10, y: 50 },
  { id: "rag", label: "Legal KB (RAG)", desc: "Retrieving Statutes", icon: Database, color: "text-emerald-400", bg: "bg-emerald-500/10", border: "border-emerald-500/30", x: 45, y: 20 },
  { id: "drafter", label: "Multi-Agent Drafter", desc: "Generating Response", icon: Cpu, color: "text-purple-400", bg: "bg-purple-500/10", border: "border-purple-500/30", x: 45, y: 80 },
  { id: "verifier", label: "Reflexion Verifier", desc: "Validating Compliance", icon: ShieldCheck, color: "text-amber-400", bg: "bg-amber-500/10", border: "border-amber-500/30", x: 80, y: 50 },
];

const edges = [
  { id: "e1", from: "intent", to: "rag", path: "M 10 50 C 30 50, 30 20, 45 20", delay: 0 },
  { id: "e2", from: "intent", to: "drafter", path: "M 10 50 C 30 50, 30 80, 45 80", delay: 1 },
  { id: "e3", from: "rag", to: "verifier", path: "M 45 20 C 65 20, 65 50, 80 50", delay: 2 },
  { id: "e4", from: "drafter", to: "verifier", path: "M 45 80 C 65 80, 65 50, 80 50", delay: 3 },
];

export function FlowAnimation() {
  const [activeNode, setActiveNode] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveNode((prev) => (prev + 1) % 4);
    }, 1200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full h-[260px] flex items-center justify-center bg-[#0a0a0a] rounded-xl border border-[var(--color-border-dim)] shadow-inner my-4 relative overflow-hidden group">
      
      {/* Background Glows */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-20">
        <div className="absolute top-[20%] left-[20%] w-32 h-32 bg-blue-500 rounded-full blur-[70px]"></div>
        <div className="absolute bottom-[20%] right-[20%] w-32 h-32 bg-emerald-500 rounded-full blur-[70px]"></div>
      </div>

      <div className="relative w-[100%] max-w-[600px] h-[80%]">
        
        {/* SVG Edges */}
        <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
          {edges.map((edge, idx) => (
            <g key={edge.id}>
              {/* Static Path */}
              <path
                d={edge.path}
                fill="none"
                stroke="rgba(255,255,255,0.1)"
                strokeWidth="0.5"
              />
              {/* Animated Pulse */}
              <motion.circle
                r="1"
                fill={idx === 0 || idx === 1 ? "#3b82f6" : idx === 2 ? "#10b981" : "#a855f7"}
                initial={{ offsetDistance: "0%" }}
                animate={{ offsetDistance: "100%" }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "linear",
                  delay: edge.delay * 0.5,
                }}
                style={{
                  offsetPath: `path('${edge.path}')`,
                  filter: "drop-shadow(0px 0px 4px currentColor)",
                }}
              />
            </g>
          ))}
        </svg>

        {/* Nodes */}
        {nodes.map((node, index) => {
          const isActive = index === activeNode;
          const isProcessing = index <= activeNode;
          const Icon = node.icon;

          return (
            <motion.div
              key={node.id}
              className={`absolute flex flex-col items-center gap-2 transform -translate-x-1/2 -translate-y-1/2`}
              style={{ left: `${node.x}%`, top: `${node.y}%` }}
              animate={isActive ? { scale: [1, 1.05, 1] } : { scale: 1 }}
              transition={{ duration: 1.5, repeat: Infinity }}
            >
              <div className={`relative w-12 h-12 rounded-xl border flex items-center justify-center backdrop-blur-md transition-all duration-500 z-10 ${
                isActive 
                  ? `${node.bg} ${node.border} shadow-[0_0_20px_rgba(255,255,255,0.05)]` 
                  : isProcessing 
                    ? "bg-[rgba(255,255,255,0.02)] border-[rgba(255,255,255,0.1)]" 
                    : "bg-transparent border-[rgba(255,255,255,0.05)] opacity-40"
              }`}>
                <Icon className={`w-5 h-5 ${isActive ? node.color : isProcessing ? "text-gray-400" : "text-gray-600"}`} />
                
                {isActive && (
                  <motion.div 
                    className={`absolute inset-0 rounded-xl ${node.border} border-2 opacity-50`}
                    initial={{ scale: 1, opacity: 0.5 }}
                    animate={{ scale: 1.4, opacity: 0 }}
                    transition={{ duration: 1.5, repeat: Infinity, ease: "easeOut" }}
                  />
                )}
              </div>
              
              <div className="flex flex-col items-center pointer-events-none">
                <span className={`text-[10px] font-mono tracking-wider uppercase transition-colors duration-500 ${
                  isActive ? "text-slate-200 font-semibold" : isProcessing ? "text-slate-400" : "text-slate-600"
                }`}>
                  {node.label}
                </span>
                <span className={`text-[8px] font-sans transition-colors duration-500 ${
                  isActive ? node.color : "text-transparent"
                }`}>
                  {node.desc}
                </span>
              </div>
            </motion.div>
          );
        })}
      </div>

      <div className="absolute bottom-4 right-4 flex items-center gap-2">
        <Activity className="w-3.5 h-3.5 text-blue-400 animate-pulse" />
        <span className="text-[10px] text-slate-400 font-mono tracking-widest uppercase">
          Agentic Reasoning
        </span>
      </div>
    </div>
  );
}
