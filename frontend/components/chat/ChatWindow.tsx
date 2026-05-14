'use client';
import { useRef, useEffect, useState } from 'react';
import { useChat } from '@/hooks/useChat';
import { MessageBubble } from './MessageBubble';
import { VoiceRecorder } from './VoiceRecorder';
import { Send, StopCircle, Trash2 } from 'lucide-react';

const CHAPTERS_11 = [
  'All','The Living World','Biological Classification','Plant Kingdom',
  'Animal Kingdom','Cell: The Unit of Life','Biomolecules',
  'Cell Cycle and Cell Division','Photosynthesis','Respiration in Plants',
  'Digestion and Absorption','Breathing and Exchange of Gases',
  'Body Fluids and Circulation','Neural Control and Coordination',
];
const CHAPTERS_12 = [
  'All','Sexual Reproduction in Flowering Plants','Human Reproduction',
  'Principles of Inheritance and Variation','Molecular Basis of Inheritance',
  'Evolution','Human Health and Disease','Biotechnology: Principles and Processes',
  'Biotechnology and Its Applications','Ecosystem','Biodiversity and Conservation',
];

const LANGS = [
  { value: '', label: '🌐 Auto' },
  { value: 'en', label: '🇬🇧 English' },
  { value: 'hi', label: '🇮🇳 हिंदी' },
  { value: 'hinglish', label: '🤙 Hinglish' },
  { value: 'ur', label: '🇵🇰 اردو' },
];

const QUICK_PROMPTS = [
  'What is the powerhouse of the cell?',
  'Explain Mitosis vs Meiosis',
  'Photosynthesis ka process kya hai?',
  'DNA replication kaise hoti hai?',
];

export function ChatWindow() {
  const { messages, isLoading, sendMessage, stopStreaming, clearChat } = useChat();
  const [input, setInput] = useState('');
  const [chapter, setChapter] = useState('All');
  const [classLevel, setClassLevel] = useState(11);
  const [language, setLanguage] = useState('');
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    const text = input.trim();
    if (!text || isLoading) return;
    setInput('');
    sendMessage(text, {
      chapter: chapter === 'All' ? undefined : chapter,
      language: language || undefined,
    });
  };

  const chapters = classLevel === 11 ? CHAPTERS_11 : CHAPTERS_12;

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-2 px-4 py-2 border-b bg-white flex-wrap">
        <select value={classLevel} onChange={e => setClassLevel(Number(e.target.value))}
          className="text-xs border rounded-lg px-2 py-1.5 bg-white focus:outline-none focus:ring-1 focus:ring-green-500">
          <option value={11}>Class 11</option>
          <option value={12}>Class 12</option>
        </select>
        <select value={chapter} onChange={e => setChapter(e.target.value)}
          className="text-xs border rounded-lg px-2 py-1.5 bg-white focus:outline-none focus:ring-1 focus:ring-green-500 max-w-[180px]">
          {chapters.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
        <select value={language} onChange={e => setLanguage(e.target.value)}
          className="text-xs border rounded-lg px-2 py-1.5 bg-white focus:outline-none focus:ring-1 focus:ring-green-500">
          {LANGS.map(l => <option key={l.value} value={l.value}>{l.label}</option>)}
        </select>
        <button onClick={clearChat} title="Clear chat"
          className="ml-auto text-xs text-gray-400 hover:text-red-500 flex items-center gap-1 px-2 py-1 rounded-lg hover:bg-red-50 transition">
          <Trash2 size={13} /> Clear
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4 bg-gray-50">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center gap-4 py-16">
            <div className="text-5xl">🧬</div>
            <div>
              <h2 className="text-lg font-bold text-green-800 mb-1">Ask BioGuru AI!</h2>
              <p className="text-sm text-gray-500 max-w-xs">Ask about NCERT Biology in English, Hindi, Hinglish, or Urdu.</p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-md w-full">
              {QUICK_PROMPTS.map(q => (
                <button key={q} onClick={() => setInput(q)}
                  className="text-xs bg-white border border-green-200 text-green-700 rounded-xl px-3 py-2 text-left hover:bg-green-50 transition">
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map(msg => (
          <MessageBubble key={msg.id} role={msg.role} content={msg.content}
            language={msg.language} sources={msg.sources} streaming={msg.streaming} />
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="border-t bg-white px-4 py-3">
        <div className="flex items-end gap-2 max-w-4xl mx-auto">
          <textarea value={input} onChange={e => setInput(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); } }}
            placeholder="Ask about Biology... (English, Hindi, Hinglish, Urdu)"
            rows={1}
            className="flex-1 resize-none border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            style={{ minHeight: '44px', maxHeight: '128px' }}
          />
          <VoiceRecorder onTranscript={text => setInput(text)} />
          {isLoading ? (
            <button onClick={stopStreaming} className="bg-red-500 hover:bg-red-600 text-white p-2.5 rounded-xl transition">
              <StopCircle size={18} />
            </button>
          ) : (
            <button onClick={handleSend} disabled={!input.trim()}
              className="bg-green-700 hover:bg-green-800 text-white p-2.5 rounded-xl transition disabled:opacity-40">
              <Send size={18} />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
