"use client";

import { useState } from "react";
import { saveDocument } from "@/lib/api";
import { Save, Check, Loader2 } from "lucide-react";

type SaveDocumentButtonProps = {
  docType: string;
  title: string;
  content: string;
};

export function SaveDocumentButton({ docType, title, content }: SaveDocumentButtonProps) {
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleSave = async () => {
    setSaving(true);
    try {
      await saveDocument({ doc_type: docType, title, content });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (error) {
      console.error("Failed to save document:", error);
    } finally {
      setSaving(false);
    }
  };

  return (
    <button
      onClick={handleSave}
      disabled={saving || saved}
      className={`flex items-center gap-2 rounded-md px-3 py-1.5 text-sm font-medium transition-all ${
        saved
          ? "bg-green-500/10 text-green-400 border border-green-500/20"
          : "bg-[#1a1a2e] text-[#d0d0e0] border border-[#2a2a3d] hover:bg-[#22223a] hover:text-white"
      }`}
    >
      {saving ? (
        <Loader2 size={16} className="animate-spin" />
      ) : saved ? (
        <Check size={16} />
      ) : (
        <Save size={16} />
      )}
      {saving ? "Saving..." : saved ? "Saved!" : "Save to My Documents"}
    </button>
  );
}
