"use client";

import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, AlertTriangle, CheckCircle, FileText } from "lucide-react";

export function DocumentScanner() {
  const [stage, setStage] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setStage(s => (s < 3 ? s + 1 : s));
    }, 2000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="w-full flex items-center justify-center p-6 bg-[#0a0a0a] rounded-xl border border-[var(--color-border-dim)] shadow-inner my-4 relative overflow-hidden">
      
      {/* Background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 bg-emerald-500/10 rounded-full blur-[80px]"></div>

      <div className="flex w-full max-w-2xl gap-8 relative z-10">
        
        {/* Document Preview (Left) */}
        <div className="flex-1 max-w-[300px] relative">
          <div className="bg-[#121212] border border-[#2a2a2a] rounded-lg p-4 shadow-xl overflow-hidden relative min-h-[320px]">
            {/* Header */}
            <div className="flex items-center gap-2 mb-4 pb-2 border-b border-[#2a2a2a]">
              <FileText className="w-4 h-4 text-blue-400" />
              <div className="h-2 bg-[#2a2a2a] rounded w-2/3"></div>
            </div>

            {/* Skeleton text */}
            <div className="space-y-3">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="space-y-1.5">
                  <div className={`h-1.5 bg-[#1f1f1f] rounded ${i === 2 || i === 4 ? 'w-full' : 'w-5/6'}`}></div>
                  <div className={`h-1.5 bg-[#1f1f1f] rounded ${i === 3 ? 'w-4/5' : 'w-full'}`}></div>
                  <div className="h-1.5 bg-[#1f1f1f] rounded w-2/3"></div>
                </div>
              ))}
            </div>

            {/* Scanning Line Animation */}
            <motion.div
              className="absolute left-0 right-0 h-[2px] bg-emerald-400 shadow-[0_0_15px_rgba(52,211,153,0.8)] z-20"
              initial={{ top: "0%" }}
              animate={{ top: "100%" }}
              transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
            >
              <div className="absolute top-0 left-0 right-0 h-16 bg-gradient-to-t from-emerald-400/20 to-transparent -translate-y-full pointer-events-none"></div>
            </motion.div>

            {/* Highlighted regions as scanner passes */}
            <AnimatePresence>
              {stage >= 1 && (
                <motion.div 
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="absolute top-[35%] left-4 right-4 h-12 bg-amber-500/10 border border-amber-500/30 rounded z-10"
                />
              )}
              {stage >= 2 && (
                <motion.div 
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="absolute top-[65%] left-4 right-4 h-12 bg-red-500/10 border border-red-500/30 rounded z-10"
                />
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Extraction Cards (Right) */}
        <div className="flex-1 flex flex-col gap-3 justify-center">
          <div className="flex items-center gap-2 mb-2">
            <Search className="w-4 h-4 text-emerald-400 animate-pulse" />
            <span className="text-xs font-mono text-emerald-400 uppercase tracking-widest">Analyzing Clauses...</span>
          </div>

          <AnimatePresence>
            {stage >= 1 && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-[#121212] border border-amber-500/30 rounded-lg p-3 shadow-lg"
              >
                <div className="flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 text-amber-500 mt-0.5 shrink-0" />
                  <div>
                    <h4 className="text-[11px] font-semibold text-amber-500 uppercase tracking-wider mb-1">Unilateral Liability Cap</h4>
                    <p className="text-[12px] text-slate-400 leading-tight">Clause 4 heavily favors the counterparty. Requires mutual revision under Indian Contract Act.</p>
                  </div>
                </div>
              </motion.div>
            )}

            {stage >= 2 && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-[#121212] border border-red-500/30 rounded-lg p-3 shadow-lg"
              >
                <div className="flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 text-red-500 mt-0.5 shrink-0" />
                  <div>
                    <h4 className="text-[11px] font-semibold text-red-500 uppercase tracking-wider mb-1">Arbitrary Termination</h4>
                    <p className="text-[12px] text-slate-400 leading-tight">Clause 7 allows termination without notice. This violates standard employment practices.</p>
                  </div>
                </div>
              </motion.div>
            )}

            {stage >= 3 && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-emerald-500/10 border border-emerald-500/30 rounded-lg p-3 shadow-lg mt-2 flex items-center gap-2"
              >
                <CheckCircle className="w-4 h-4 text-emerald-500" />
                <span className="text-xs text-emerald-400 font-medium">Scan Complete. Generating Report...</span>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

      </div>
    </div>
  );
}
