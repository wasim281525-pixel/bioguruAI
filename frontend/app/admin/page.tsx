'use client';
import { useState, useEffect } from 'react';
import AppLayout from '@/components/common/AppLayout';
import { apiFetch } from '@/lib/api';
import { Upload, FileText, Loader2 } from 'lucide-react';

export default function AdminPage() {
  const [file, setFile] = useState<File | null>(null);
  const [sourceType, setSourceType] = useState('ncert');
  const [classLevel, setClassLevel] = useState(11);
  const [chapter, setChapter] = useState('');
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [docs, setDocs] = useState<any[]>([]);

  useEffect(() => {
    apiFetch('/api/upload/documents').then(r => r.json()).then(setDocs).catch(() => setDocs([]));
  }, []);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setUploading(true);
    setMessage('');

    const form = new FormData();
    form.append('file', file);
    form.append('source_type', sourceType);
    form.append('class_level', String(classLevel));
    form.append('chapter', chapter);

    try {
      const res = await fetch(`/api/upload/pdf?source_type=${sourceType}&class_level=${classLevel}&chapter=${encodeURIComponent(chapter)}`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        body: form,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Upload failed');
      setMessage(`✅ Uploaded and ingestion started for: ${data.filename}`);
      setFile(null);
      apiFetch('/api/upload/documents').then(r => r.json()).then(setDocs).catch(() => {});
    } catch (err: any) {
      setMessage(`❌ ${err.message}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <AppLayout>
      <div className="flex-1 overflow-y-auto bg-gray-50 px-6 py-6">
        <div className="max-w-2xl mx-auto space-y-6">
          <div>
            <h1 className="text-xl font-bold text-gray-800">Admin Panel</h1>
            <p className="text-sm text-gray-500">Upload PDFs to the RAG knowledge base</p>
          </div>

          <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
            <h2 className="font-semibold text-gray-700 mb-4 flex items-center gap-2">
              <Upload size={18} /> Upload PDF
            </h2>
            <form onSubmit={handleUpload} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">PDF File</label>
                <input type="file" accept=".pdf" required
                  onChange={e => setFile(e.target.files?.[0] || null)}
                  className="w-full text-sm text-gray-500 file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-green-50 file:text-green-700 file:font-medium hover:file:bg-green-100" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Source Type</label>
                  <select value={sourceType} onChange={e => setSourceType(e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500">
                    <option value="ncert">NCERT</option>
                    <option value="pyq">PYQ (Previous Year)</option>
                    <option value="notes">Study Notes</option>
                    <option value="reference">Reference</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Class Level</label>
                  <select value={classLevel} onChange={e => setClassLevel(Number(e.target.value))}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500">
                    <option value={11}>Class 11</option>
                    <option value={12}>Class 12</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Chapter Name</label>
                <input type="text" value={chapter} onChange={e => setChapter(e.target.value)}
                  placeholder="e.g. Cell: The Unit of Life"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500" />
              </div>
              {message && (
                <div className={`text-sm px-3 py-2 rounded-lg ${message.startsWith('✅') ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-red-50 text-red-600 border border-red-200'}`}>
                  {message}
                </div>
              )}
              <button type="submit" disabled={uploading || !file}
                className="w-full bg-green-700 hover:bg-green-800 text-white font-semibold py-2.5 rounded-xl flex items-center justify-center gap-2 transition disabled:opacity-50">
                {uploading ? <><Loader2 size={16} className="animate-spin" /> Uploading...</> : <><Upload size={16} /> Upload & Ingest</>}
              </button>
            </form>
          </div>

          {docs.length > 0 && (
            <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
              <h2 className="font-semibold text-gray-700 mb-4 flex items-center gap-2">
                <FileText size={18} /> Uploaded Documents
              </h2>
              <div className="space-y-2">
                {docs.map((doc: any) => (
                  <div key={doc.id} className="flex items-center gap-3 py-2 border-b border-gray-50 last:border-0 text-sm">
                    <FileText size={16} className="text-gray-400 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-gray-700 truncate">{doc.filename}</div>
                      <div className="text-xs text-gray-400">{doc.source_type} | Class {doc.class_level} {doc.chapter && `| ${doc.chapter}`}</div>
                    </div>
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                      doc.status === 'done' ? 'bg-green-100 text-green-700' :
                      doc.status === 'processing' ? 'bg-yellow-100 text-yellow-700' :
                      doc.status === 'error' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-600'
                    }`}>{doc.status}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
