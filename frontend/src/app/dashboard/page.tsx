"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Cookies from 'js-cookie';
import Link from 'next/link';
import { UserMenu } from "@/components/UserMenu";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { DocumentModal, DocumentInfo } from "@/components/DocumentModal";
import { marked } from 'marked';
import { Download, Trash2, ArrowLeft, Search } from 'lucide-react';
import { useToast } from "@/hooks/useToast";

const DOC_TYPE_CONFIG: Record<string, { label: string; color: string }> = {
  rti: { label: 'RTI Application', color: 'var(--color-accent)' },
  legal_notice: { label: 'Legal Notice', color: 'var(--color-semantic-blue)' },
  consumer_complaint: { label: 'Consumer Complaint', color: 'var(--color-semantic-green)' },
  rera_complaint: { label: 'RERA Complaint', color: 'var(--color-semantic-purple)' },
  legal_advice: { label: 'Legal Advice', color: 'var(--color-semantic-slate)' },
};

function getDocConfig(type: string) {
  return DOC_TYPE_CONFIG[type] || { label: type, color: 'var(--color-text-secondary)' };
}

// Simple relative time formatter
function formatRelativeTime(isoString: string) {
  const date = new Date(isoString);
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
  
  if (diffInSeconds < 60) return "Just now";
  const diffInMinutes = Math.floor(diffInSeconds / 60);
  if (diffInMinutes < 60) return `${diffInMinutes} minute${diffInMinutes > 1 ? 's' : ''} ago`;
  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) return `${diffInHours} hour${diffInHours > 1 ? 's' : ''} ago`;
  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays < 30) return `${diffInDays} day${diffInDays > 1 ? 's' : ''} ago`;
  
  return date.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}

// Strip markdown for preview
function stripMarkdown(md: string) {
  return md.replace(/[#*_>\[\]]/g, '').replace(/\n+/g, ' ').trim();
}

async function downloadPDF(doc: DocumentInfo) {
  const cfg = getDocConfig(doc.doc_type);
  const printableContent = doc.content.replace(/\[[^\]]+\](?!\()/g, '_________________________');
  const htmlContent = await Promise.resolve(marked.parse(printableContent));
  
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>${doc.title} - JanSaathi Document</title>
<style>
  @page { size: A4; margin: 20mm; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: Arial, sans-serif; background: #fff; color: #000; display: block; }
  .page { width: 100%; min-height: 100%; font-size: 12pt; line-height: 1.6; }
  .header { border-bottom: 2px solid #000; padding-bottom: 15px; margin-bottom: 25px; }
  .header-top { display: flex; justify-content: space-between; align-items: flex-start; }
  .app-name { font-size: 10pt; font-weight: 600; color: #555; text-transform: uppercase; }
  .doc-type-badge { font-size: 9pt; font-weight: 600; color: #000; border: 1px solid #000; padding: 3px 8px; text-transform: uppercase; }
  .title { font-size: 18pt; font-weight: 700; margin-top: 15px; text-align: center; }
  .content p { margin-bottom: 14pt; text-align: justify; }
  .content h1, .content h2 { margin: 20pt 0 12pt; font-size: 14pt; }
  .content ul, .content ol { margin-bottom: 14pt; padding-left: 24pt; }
  .content li { margin-bottom: 5pt; }
</style>
</head>
<body onload="window.print(); setTimeout(() => window.close(), 500)">
  <div class="page">
    <div class="header">
      <div class="header-top">
        <div class="app-name">JanSaathi AI Legal Assistant</div>
        <div class="doc-type-badge">${cfg.label}</div>
      </div>
      <div class="title">${doc.title}</div>
    </div>
    <div class="content">${htmlContent}</div>
  </div>
</body>
</html>`;

  const blob = new Blob([html], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  window.open(url, '_blank');
}

export default function Dashboard() {
  const [documents, setDocuments] = useState<DocumentInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDoc, setSelectedDoc] = useState<DocumentInfo | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeFilter, setActiveFilter] = useState<string>('all');
  
  const router = useRouter();
  const { toast } = useToast();

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const token = Cookies.get('token');
      const res = await fetch('http://127.0.0.1:8000/api/documents/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setDocuments(data);
      } else {
        toast("Failed to load documents", "error");
      }
    } catch (e) {
      toast("Connection error while loading documents", "error");
    } finally {
      setLoading(false);
    }
  };

  const deleteDocument = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this document?')) return;
    
    try {
      const token = Cookies.get('token');
      const res = await fetch(`http://127.0.0.1:8000/api/documents/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        setDocuments(prev => prev.filter(d => d.id !== id));
        toast("Document deleted successfully", "success");
      } else {
        toast("Failed to delete document", "error");
      }
    } catch (e) {
      toast("Connection error while deleting", "error");
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[var(--color-bg-base)] flex flex-col selection:bg-[var(--color-accent)] selection:text-[#080808]">
        
        {/* Navigation Bar */}
        <nav className="h-[60px] bg-[var(--color-bg-surface)] border-b border-[var(--color-border-dim)] shrink-0 flex items-center justify-between px-6 sticky top-0 z-10">
          <div className="flex items-center gap-4">
            <Link 
              href="/chat"
              className="flex items-center gap-2 text-[13px] font-medium text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] transition-colors"
            >
              <ArrowLeft className="w-4 h-4" /> Back to Chat
            </Link>
          </div>
          <div className="flex items-center gap-4">
            <div className="font-heading font-medium text-[15px] text-[var(--color-text-primary)] hidden sm:block">
              My Documents
            </div>
            <div className="w-[1px] h-4 bg-[var(--color-border-strong)] mx-2 hidden sm:block" />
            <UserMenu />
          </div>
        </nav>

        {/* Main Content */}
        <div className="flex-1 max-w-7xl w-full mx-auto p-6 md:p-8">
          
          <div className="mb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div>
              <h1 className="font-heading font-medium text-2xl text-[var(--color-text-primary)]">My Documents</h1>
              <p className="text-[14px] text-[var(--color-text-secondary)] mt-1">
                View and download your AI-generated legal drafts. {!loading && `(${documents.length} total)`}
              </p>
            </div>
            
            {!loading && documents.length > 0 && (
              <div className="flex flex-col sm:flex-row items-center gap-3 w-full md:w-auto">
                <div className="relative w-full sm:w-[260px]">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--color-text-muted)]" />
                  <input 
                    type="text"
                    placeholder="Search titles or contents..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full bg-[var(--color-bg-surface)] border border-[var(--color-border-dim)] rounded-lg pl-9 pr-3 py-2 text-[13px] text-[var(--color-text-primary)] focus:outline-none focus:border-[var(--color-accent)] transition-colors placeholder-[var(--color-text-muted)]"
                  />
                </div>
              </div>
            )}
          </div>

          {!loading && documents.length > 0 && (
            <div className="flex items-center gap-2 mb-8 overflow-x-auto pb-2 scrollbar-none" style={{ scrollbarWidth: 'none' }}>
              <button
                onClick={() => setActiveFilter('all')}
                className={`shrink-0 px-3 py-1.5 rounded-full text-[12px] font-medium transition-colors ${
                  activeFilter === 'all' 
                    ? 'bg-[var(--color-text-primary)] text-[var(--color-bg-base)]' 
                    : 'bg-[var(--color-bg-surface)] border border-[var(--color-border-dim)] text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:border-[var(--color-border-strong)]'
                }`}
              >
                All Documents
              </button>
              {Object.entries(DOC_TYPE_CONFIG).map(([key, config]) => (
                <button
                  key={key}
                  onClick={() => setActiveFilter(key)}
                  className={`shrink-0 px-3 py-1.5 rounded-full text-[12px] font-medium transition-colors ${
                    activeFilter === key 
                      ? 'bg-[var(--color-text-primary)] text-[var(--color-bg-base)]' 
                      : 'bg-[var(--color-bg-surface)] border border-[var(--color-border-dim)] text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:border-[var(--color-border-strong)]'
                  }`}
                >
                  {config.label}
                </button>
              ))}
            </div>
          )}

          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-[var(--color-bg-surface)] border border-[var(--color-border-dim)] rounded-xl p-5 h-[160px] flex flex-col justify-between">
                  <div>
                    <div className="w-24 h-3 bg-[var(--color-bg-elevated)] rounded-sm mb-3 animate-pulse"></div>
                    <div className="w-full h-4 bg-[var(--color-bg-elevated)] rounded-sm mb-2 animate-pulse" style={{ animationDelay: `${i * 100}ms` }}></div>
                    <div className="w-3/4 h-4 bg-[var(--color-bg-elevated)] rounded-sm animate-pulse" style={{ animationDelay: `${i * 100}ms` }}></div>
                  </div>
                  <div className="w-16 h-3 bg-[var(--color-bg-elevated)] rounded-sm animate-pulse"></div>
                </div>
              ))}
            </div>
          ) : documents.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-20 text-center border border-dashed border-[var(--color-border-strong)] rounded-xl">
              <div className="w-12 h-12 rounded-full bg-[var(--color-bg-subtle)] flex items-center justify-center mb-4">
                <span className="text-xl">📄</span>
              </div>
              <h3 className="font-heading font-medium text-[16px] text-[var(--color-text-primary)] mb-1">No documents yet</h3>
              <p className="text-[14px] text-[var(--color-text-secondary)] mb-6">Generated drafts will appear here.</p>
              <Link 
                href="/chat"
                className="px-4 py-2 bg-[var(--color-accent)] hover:bg-[var(--color-accent-dim)] text-[#080808] font-medium text-[13px] rounded transition-colors"
              >
                Start a New Chat
              </Link>
            </div>
          ) : (() => {
            const filteredDocuments = documents.filter(doc => {
              const matchesSearch = doc.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                                    doc.content.toLowerCase().includes(searchQuery.toLowerCase());
              const matchesFilter = activeFilter === 'all' || doc.doc_type === activeFilter;
              return matchesSearch && matchesFilter;
            });

            if (filteredDocuments.length === 0) {
              return (
                <div className="flex flex-col items-center justify-center py-20 text-center border border-dashed border-[var(--color-border-dim)] rounded-xl">
                  <div className="w-12 h-12 rounded-full bg-[var(--color-bg-surface)] flex items-center justify-center mb-4">
                    <Search className="w-5 h-5 text-[var(--color-text-muted)]" />
                  </div>
                  <h3 className="font-heading font-medium text-[16px] text-[var(--color-text-primary)] mb-1">No matches found</h3>
                  <p className="text-[14px] text-[var(--color-text-secondary)] mb-4 max-w-[260px]">
                    We couldn't find any documents matching your search or filter criteria.
                  </p>
                  <button 
                    onClick={() => { setSearchQuery(''); setActiveFilter('all'); }}
                    className="px-4 py-2 bg-[var(--color-bg-surface)] hover:bg-[var(--color-bg-elevated)] border border-[var(--color-border-dim)] text-[var(--color-text-primary)] font-medium text-[13px] rounded transition-colors"
                  >
                    Clear Filters
                  </button>
                </div>
              );
            }

            return (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredDocuments.map(doc => {
                  const cfg = getDocConfig(doc.doc_type);
                  const preview = stripMarkdown(doc.content).slice(0, 120) + (doc.content.length > 120 ? '...' : '');
                  
                  return (
                    <div 
                      key={doc.id}
                      onClick={() => setSelectedDoc(doc)}
                      className="group relative bg-[var(--color-bg-surface)] border border-[var(--color-border-dim)] hover:border-[var(--color-border-strong)] rounded-xl p-5 cursor-pointer transition-all hover:-translate-y-0.5 overflow-hidden flex flex-col h-[180px]"
                    >
                      {/* Left Accent Bar */}
                      <div 
                        className="absolute left-0 top-0 bottom-0 w-1 rounded-l-xl transition-colors"
                        style={{ backgroundColor: cfg.color }}
                      />
                      
                      <div className="pl-2 flex-1">
                        <div className="flex items-center justify-between mb-1.5">
                          <span 
                            className="text-[10px] font-sans font-medium uppercase tracking-[0.08em]"
                            style={{ color: cfg.color }}
                          >
                            {cfg.label}
                          </span>
                          <span className="text-[11px] text-[var(--color-text-muted)]">
                            {formatRelativeTime(doc.created_at)}
                          </span>
                        </div>
                        
                        <h3 className="font-heading font-medium text-[15px] text-[var(--color-text-primary)] line-clamp-2 leading-tight mb-3">
                          {doc.title}
                        </h3>
                        
                        <p className="text-[12px] text-[var(--color-text-secondary)] font-sans leading-[1.6] line-clamp-3">
                          {preview}
                        </p>
                      </div>

                      {/* Action buttons (appear on hover) */}
                      <div className="pl-2 mt-auto flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-150">
                        <button 
                          onClick={(e) => { e.stopPropagation(); downloadPDF(doc); }}
                          className="flex items-center gap-1.5 px-2.5 py-1.5 text-[12px] font-medium text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-bg-elevated)] rounded transition-colors"
                        >
                          <Download className="w-3.5 h-3.5" /> Download
                        </button>
                        <button 
                          onClick={(e) => deleteDocument(e, doc.id)}
                          className="flex items-center gap-1.5 px-2.5 py-1.5 text-[12px] font-medium text-[var(--color-text-secondary)] hover:text-[var(--color-semantic-red)] hover:bg-[color-mix(in_srgb,var(--color-semantic-red)_10%,transparent)] rounded transition-colors"
                        >
                          <Trash2 className="w-3.5 h-3.5" /> Delete
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            );
          })()}
        </div>
      </div>

      <DocumentModal 
        isOpen={!!selectedDoc}
        onClose={() => setSelectedDoc(null)}
        document={selectedDoc}
        onDownload={() => selectedDoc && downloadPDF(selectedDoc)}
      />
    </ProtectedRoute>
  );
}
