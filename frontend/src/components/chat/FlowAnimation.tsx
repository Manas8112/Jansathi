"use client";

import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Database, FileText, Cpu, ShieldCheck, Zap } from "lucide-react";

const steps = [
  { id: "input", label: "Intent Classification", icon: FileText, color: "text-slate-600 dark:text-slate-300", bg: "bg-slate-200 dark:bg-slate-800" },
  { id: "graph", label: "Vector Retrieval", icon: Database, color: "text-blue-600 dark:text-blue-400", bg: "bg-blue-200/50 dark:bg-blue-900/30" },
  { id: "llm", label: "Multi-Agent Drafter", icon: Cpu, color: "text-purple-600 dark:text-purple-400", bg: "bg-purple-200/50 dark:bg-purple-900/30" },
  { id: "verify", label: "Finalize Output", icon: ShieldCheck, color: "text-emerald-600 dark:text-emerald-400", bg: "bg-emerald-200/50 dark:bg-emerald-900/30" },
];

export function FlowAnimation() {
  const [activeStepIndex, setActiveStepIndex] = useState(0);

  useEffect(() => {
    // Cycle through steps to simulate a rigorous pipeline processing
    const interval = setInterval(() => {
      setActiveStepIndex((prev) => (prev + 1) % steps.length);
    }, 1800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full flex flex-col items-center justify-center p-6 bg-[var(--color-bg-surface)] rounded-xl border border-[var(--color-border-dim)] shadow-inner mt-4 relative overflow-hidden">
      
      {/* Background abstract gradients for trust/tech feel */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-20">
        <div className="absolute top-1/2 left-1/4 w-32 h-32 bg-blue-500 rounded-full blur-[80px] -translate-y-1/2"></div>
        <div className="absolute top-1/2 right-1/4 w-32 h-32 bg-emerald-500 rounded-full blur-[80px] -translate-y-1/2"></div>
      </div>

      <div className="relative z-10 w-full max-w-2xl">
        <div className="flex items-center justify-between relative">
          
          {/* Animated Connecting Line Background */}
          <div className="absolute top-1/2 left-[10%] right-[10%] h-0.5 bg-[var(--color-border-strong)] -translate-y-1/2 z-0"></div>
          
          {/* Animated Glowing Path */}
          <motion.div 
            className="absolute top-1/2 left-[10%] h-0.5 bg-gradient-to-r from-blue-500 via-emerald-500 to-transparent -translate-y-1/2 z-0 shadow-[0_0_8px_rgba(59,130,246,0.5)]"
            initial={{ width: "0%" }}
            animate={{ width: `${(activeStepIndex / (steps.length - 1)) * 80}%` }}
            transition={{ duration: 0.8, ease: "easeInOut" }}
          />

          {steps.map((step, index) => {
            const isActive = index === activeStepIndex;
            const isPast = index < activeStepIndex;
            const Icon = step.icon;

            return (
              <div key={step.id} className="relative z-10 flex flex-col items-center gap-3">
                <motion.div 
                  className={`w-12 h-12 rounded-xl border flex items-center justify-center backdrop-blur-md transition-colors duration-500 ${
                    isActive 
                      ? `${step.bg} border-[var(--color-border-accent)] shadow-[0_0_15px_rgba(var(--color-accent-rgb),0.1)]` 
                      : isPast 
                        ? "bg-[var(--color-bg-subtle)] border-[var(--color-border-dim)]" 
                        : "bg-[var(--color-bg-base)] border-[var(--color-border-strong)] opacity-50"
                  }`}
                  animate={isActive ? { scale: [1, 1.1, 1] } : { scale: 1 }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                >
                  <Icon className={`w-5 h-5 ${isActive ? step.color : isPast ? "text-slate-400" : "text-slate-600"}`} />
                  
                  {/* Ping effect when active */}
                  {isActive && (
                    <span className="absolute flex h-full w-full">
                      <span className={`animate-ping absolute inline-flex h-full w-full rounded-xl opacity-20 ${step.bg}`}></span>
                    </span>
                  )}
                </motion.div>
                
                <span className={`text-[10px] font-mono tracking-widest uppercase transition-colors duration-500 ${
                  isActive ? "text-slate-200 font-bold" : isPast ? "text-slate-500" : "text-slate-700"
                }`}>
                  {step.label}
                </span>
              </div>
            );
          })}
        </div>

        <div className="mt-8 flex justify-center items-center gap-2">
          <Zap className="w-3.5 h-3.5 text-yellow-500/80 animate-pulse" />
          <span className="text-xs text-slate-400 font-mono">
            {activeStepIndex === 0 && "Parsing user intent & routing to agent..."}
            {activeStepIndex === 1 && "Retrieving legal precedents & Acts..."}
            {activeStepIndex === 2 && "Agents drafting response context..."}
            {activeStepIndex === 3 && "Verifying tone and formatting..."}
          </span>
        </div>
      </div>
    </div>
  );
}
