"use client";

import Link from "next/link";
import { ArrowRight, Scale, Shield, FileText } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";

export default function Home() {
  return (
    <div className="min-h-screen bg-[var(--color-bg-base)] text-[var(--color-text-primary)] selection:bg-[var(--color-accent)] selection:text-[#080808]">
      
      {/* NAVBAR */}
      <nav className="fixed top-0 left-0 right-0 h-[60px] bg-[rgba(8,8,8,0.85)] backdrop-blur-md border-b border-[var(--color-border-accent)] border-opacity-40 z-50">
        <div className="max-w-7xl mx-auto px-6 h-full flex items-center justify-between">
          <Link href="/" className="font-heading font-medium text-lg text-[var(--color-accent)] tracking-tight">
            JanSaathi
          </Link>
          <div className="flex items-center gap-4">
            <ThemeToggle />
            <Link 
              href="/login" 
              className="text-sm font-medium text-[var(--color-text-primary)] hover:text-[var(--color-accent)] transition-colors"
            >
              Sign in
            </Link>
            <Link 
              href="/chat" 
              className="h-[34px] px-4 flex items-center justify-center bg-[var(--color-accent)] hover:bg-[var(--color-accent-dim)] text-[#080808] text-sm font-medium rounded transition-colors"
            >
              Get started
            </Link>
          </div>
        </div>
      </nav>

      {/* HERO SECTION */}
      <section className="relative min-h-screen pt-[60px] flex items-center overflow-hidden">
        <div className="max-w-7xl mx-auto px-6 w-full grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          
          <div className="max-w-[560px] z-10">
            {/* Eyebrow badge */}
            <div className="inline-flex items-center px-2.5 py-1 mb-6 rounded bg-[var(--color-accent-muted)] border border-[var(--color-accent)] border-opacity-20">
              <span className="text-[10px] font-medium text-[var(--color-accent)] uppercase tracking-wider">
                AI-Powered Legal Assistant
              </span>
            </div>
            
            <h1 className="font-heading font-medium text-[52px] text-[var(--color-text-primary)] leading-[1.1] tracking-[-0.03em] mb-4">
              Your legal rights, explained. Your documents, drafted.
            </h1>
            
            <p className="text-[18px] text-[var(--color-text-secondary)] leading-[1.65] max-w-[440px] mb-8">
              Describe your situation in plain language — RTI applications, consumer complaints, legal notices — generated in seconds.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <Link 
                href="/chat"
                className="w-full sm:w-auto px-6 py-3.5 bg-[var(--color-accent)] hover:bg-[var(--color-accent-dim)] text-[#080808] font-medium rounded-lg flex items-center justify-center gap-2 transition-colors"
              >
                Start a consultation <ArrowRight className="w-4 h-4" />
              </Link>
              <Link 
                href="#features"
                className="w-full sm:w-auto px-6 py-3.5 bg-transparent border border-[var(--color-border-strong)] text-[var(--color-text-primary)] hover:bg-[var(--color-bg-elevated)] font-medium rounded-lg text-center transition-colors"
              >
                See how it works
              </Link>
            </div>
          </div>

          {/* Right side Document Preview (Desktop only) */}
          <div className="hidden lg:block relative z-0 perspective-[1000px]">
            <div 
              className="bg-[var(--color-bg-surface)] border border-[var(--color-border-strong)] rounded-xl p-8 shadow-2xl w-full max-w-[500px] ml-auto overflow-hidden"
              style={{ transform: "rotate(2deg)" }}
            >
              <div className="flex items-center gap-2 mb-6 pb-4 border-b border-[var(--color-border-dim)]">
                <div className="w-3 h-3 rounded-full bg-[var(--color-border-strong)]"></div>
                <div className="w-3 h-3 rounded-full bg-[var(--color-border-strong)]"></div>
                <div className="w-3 h-3 rounded-full bg-[var(--color-border-strong)]"></div>
              </div>
              <div className="font-mono text-[13px] text-[var(--color-text-secondary)] leading-[1.8] space-y-4">
                <p><span className="text-[var(--color-text-primary)]">FORM A</span></p>
                <p>Application under section 6(1) of the Right to Information Act, 2005.</p>
                <p>
                  <span className="text-[var(--color-text-muted)]">To:</span><br/>
                  The Public Information Officer,<br/>
                  Municipal Corporation Department.
                </p>
                <p>
                  <span className="text-[var(--color-text-muted)]">Subject:</span><br/>
                  Information regarding budget allocation and expenditure for road repairs in Ward 42.
                </p>
                <p className="mt-8 border-t border-[var(--color-border-dim)] pt-4 text-[var(--color-accent)]">
                  &gt; AI processing complete. Ready for download.
                </p>
              </div>
            </div>
          </div>
          
        </div>
      </section>

      {/* SOCIAL PROOF BAR */}
      <section className="w-full bg-[var(--color-bg-surface)] border-y border-[var(--color-border-dim)] py-8">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-8 text-center divide-y md:divide-y-0 md:divide-x divide-[var(--color-border-dim)]">
          <div className="pt-4 md:pt-0">
            <div className="text-[13px] font-medium text-[var(--color-text-secondary)] tracking-wider uppercase mb-1">RTI Applications</div>
            <div className="font-heading font-medium text-3xl text-[var(--color-text-primary)]">1,420+</div>
          </div>
          <div className="pt-4 md:pt-0">
            <div className="text-[13px] font-medium text-[var(--color-text-secondary)] tracking-wider uppercase mb-1">Consumer Complaints</div>
            <div className="font-heading font-medium text-3xl text-[var(--color-text-primary)]">850+</div>
          </div>
          <div className="pt-4 md:pt-0">
            <div className="text-[13px] font-medium text-[var(--color-text-secondary)] tracking-wider uppercase mb-1">Legal Notices</div>
            <div className="font-heading font-medium text-3xl text-[var(--color-text-primary)]">2,100+</div>
          </div>
        </div>
      </section>

      {/* FEATURES SECTION */}
      <section id="features" className="py-32">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
            
            <div className="relative pl-6 border-l-2 border-[var(--color-border-accent)]">
              <div className="font-mono text-[11px] text-[var(--color-accent)] mb-3">01 / KNOW YOUR RIGHTS</div>
              <h3 className="font-heading font-medium text-[18px] text-[var(--color-text-primary)] tracking-tight mb-2">Intent Recognition</h3>
              <p className="text-[var(--color-text-secondary)] text-[15px] leading-relaxed">
                Describe your problem in your own words. Our AI instantly identifies whether you need an RTI, a legal notice, or a consumer forum complaint.
              </p>
            </div>
            
            <div className="relative pl-6 border-l-2 border-[var(--color-border-accent)]">
              <div className="font-mono text-[11px] text-[var(--color-accent)] mb-3">02 / HYBRID RAG</div>
              <h3 className="font-heading font-medium text-[18px] text-[var(--color-text-primary)] tracking-tight mb-2">Legal Precedents</h3>
              <p className="text-[var(--color-text-secondary)] text-[15px] leading-relaxed">
                The AI grounds its responses in Indian Bare Acts and Supreme Court rulings. It retrieves exact sections using vector search so you get accurate advice.
              </p>
            </div>
            
            <div className="relative pl-6 border-l-2 border-[var(--color-border-accent)]">
              <div className="font-mono text-[11px] text-[var(--color-accent)] mb-3">03 / DOCUMENT GENERATION</div>
              <h3 className="font-heading font-medium text-[18px] text-[var(--color-text-primary)] tracking-tight mb-2">Ready to File</h3>
              <p className="text-[var(--color-text-secondary)] text-[15px] leading-relaxed">
                Automatically draft perfectly formatted documents. Save them to your dashboard and download them as print-ready PDFs in one click.
              </p>
            </div>

          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="w-full border-t border-[var(--color-border-dim)] py-8 bg-[var(--color-bg-base)]">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="font-heading font-medium text-[var(--color-text-primary)]">JanSaathi</span>
            <span className="text-[var(--color-border-strong)]">|</span>
            <span className="text-sm text-[var(--color-text-secondary)]">Built for Indian citizens</span>
          </div>
          <div className="flex items-center gap-6 text-sm font-medium text-[var(--color-text-secondary)]">
            <Link href="#" className="hover:text-[var(--color-text-primary)] transition-colors">Privacy</Link>
            <Link href="#" className="hover:text-[var(--color-text-primary)] transition-colors">Terms</Link>
            <Link href="/login" className="hover:text-[var(--color-text-primary)] transition-colors">Sign in</Link>
          </div>
        </div>
      </footer>

    </div>
  );
}
