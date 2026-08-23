"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Network, ShieldCheck, Cpu, Database, ScanSearch } from "lucide-react";

const features = [
  {
    id: "multi-agent",
    title: "Multi-Agent Orchestration",
    subtitle: "LangGraph Powered",
    description: "Built on LangGraph, specialized AI agents (Analyzer, Drafter, Verifier) seamlessly pass state and context to execute complex legal workflows automatically.",
    icon: <Network className="w-10 h-10" />
  },
  {
    id: "reflexion",
    title: "Reflexion Self-Correction",
    subtitle: "Adversarial Evaluation Loop",
    description: "An adversarial Verifier Agent evaluates generated advice against 6 strict legal criteria, forcing internal re-drafts before you ever see the output.",
    icon: <ShieldCheck className="w-10 h-10" />
  },
  {
    id: "local-nlp",
    title: "Local Fine-Tuned NLP",
    subtitle: "Zero-Latency Intent Routing",
    description: "A dedicated HuggingFace Safetensors model runs locally in memory to classify legal intent with zero latency, bypassing external API bottlenecks.",
    icon: <Cpu className="w-10 h-10" />
  },
  {
    id: "hybrid-rag",
    title: "Hybrid Legal RAG",
    subtitle: "Dense + Sparse Retrieval",
    description: "Combines dense vector embeddings with BM25 sparse retrieval to accurately fetch citations from the Indian Penal Code and Bare Acts.",
    icon: <Database className="w-10 h-10" />
  },
  {
    id: "vision-ocr",
    title: "Computer Vision & OCR",
    subtitle: "Scanned PDF Fallback",
    description: "Graceful fallback to OCR APIs allows the system to effortlessly parse unstructured, image-based government PDFs and scanned contracts instantly.",
    icon: <ScanSearch className="w-10 h-10" />
  }
];

export function ArchitectureShowcase() {
  const [activeIndex, setActiveIndex] = useState(0);
  const activeFeature = features[activeIndex];

  return (
    <section id="features" className="py-32 w-full bg-[var(--color-bg-base)]">
      <div className="max-w-7xl mx-auto px-6">
        
        {/* Section Header */}
        <div className="mb-16">
          <div className="font-mono text-[11px] text-[var(--color-accent)] mb-3 uppercase tracking-widest">
            Under the Hood
          </div>
          <h2 className="font-heading font-medium text-3xl md:text-4xl text-[var(--color-text-primary)] tracking-tight">
            Built for Scale & Accuracy
          </h2>
          <p className="mt-4 text-[var(--color-text-secondary)] text-[16px] max-w-xl leading-relaxed">
            JanSaathi doesn't just pass your prompt to an LLM. It relies on a multi-stage, robust AI architecture to guarantee legal accuracy.
          </p>
        </div>

        {/* Interactive Layout */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-12 min-h-[400px]">
          
          {/* Left Panel: Feature List */}
          <div className="md:col-span-5 flex flex-col gap-2">
            {features.map((feature, idx) => {
              const isActive = idx === activeIndex;
              return (
                <button
                  key={feature.id}
                  onMouseEnter={() => setActiveIndex(idx)}
                  onClick={() => setActiveIndex(idx)}
                  className={`relative flex items-center text-left p-5 rounded-xl transition-all duration-300 ${
                    isActive 
                      ? "bg-[var(--color-bg-surface)] shadow-lg ring-1 ring-[var(--color-border-accent)] ring-opacity-50" 
                      : "hover:bg-[var(--color-bg-subtle)]"
                  }`}
                >
                  <div className="flex-1">
                    <h3 className={`font-heading font-medium text-[16px] transition-colors ${isActive ? "text-[var(--color-accent)]" : "text-[var(--color-text-primary)]"}`}>
                      {feature.title}
                    </h3>
                  </div>
                  
                  {/* Active Indicator Glow */}
                  {isActive && (
                    <motion.div 
                      layoutId="active-pill"
                      className="absolute inset-0 rounded-xl bg-gradient-to-r from-[var(--color-accent)]/5 to-transparent border-l-2 border-[var(--color-accent)] pointer-events-none"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.3 }}
                    />
                  )}
                </button>
              );
            })}
          </div>

          {/* Right Panel: Feature Details */}
          <div className="md:col-span-7 flex items-center justify-center p-8 lg:p-12 bg-[var(--color-bg-surface)] border border-[var(--color-border-dim)] rounded-2xl overflow-hidden relative">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeFeature.id}
                initial={{ opacity: 0, y: 20, filter: "blur(10px)" }}
                animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
                exit={{ opacity: 0, y: -20, filter: "blur(10px)" }}
                transition={{ duration: 0.4, ease: "easeOut" }}
                className="flex flex-col h-full justify-center w-full"
              >
                <div className="w-16 h-16 rounded-2xl bg-[var(--color-bg-subtle)] border border-[var(--color-border-strong)] flex items-center justify-center text-[var(--color-accent)] mb-8 shadow-inner">
                  {activeFeature.icon}
                </div>
                
                <div className="font-mono text-[12px] text-[var(--color-text-muted)] mb-3 uppercase tracking-wider">
                  {activeFeature.subtitle}
                </div>
                
                <h3 className="font-heading font-medium text-3xl text-[var(--color-text-primary)] mb-6 tracking-tight">
                  {activeFeature.title}
                </h3>
                
                <p className="text-[17px] text-[var(--color-text-secondary)] leading-[1.8] max-w-lg">
                  {activeFeature.description}
                </p>
              </motion.div>
            </AnimatePresence>
            
            {/* Subtle background decoration */}
            <div className="absolute right-0 bottom-0 opacity-[0.03] pointer-events-none translate-x-1/4 translate-y-1/4 scale-150">
               {activeFeature.icon}
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}
