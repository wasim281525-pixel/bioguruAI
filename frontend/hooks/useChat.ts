'use client';
import { useState, useCallback, useRef } from 'react';
import { detectLanguage } from '@/lib/langDetect';
import { streamChat } from '@/lib/api';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  language?: string;
  sources?: string[];
  streaming?: boolean;
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(async (
    text: string,
    options: { chapter?: string; language?: string } = {},
  ) => {
    const lang = options.language || detectLanguage(text);

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      language: lang,
    };
    setMessages(prev => [...prev, userMsg]);

    const assistantId = (Date.now() + 1).toString();
    setMessages(prev => [...prev, {
      id: assistantId, role: 'assistant', content: '', streaming: true,
    }]);

    setIsLoading(true);
    abortRef.current = new AbortController();

    streamChat(
      {
        message: text,
        history: messages.slice(-8).map(m => ({ role: m.role, content: m.content })),
        chapter: options.chapter || null,
        language: lang,
        stream: true,
      },
      (token) => {
        setMessages(prev => prev.map(m =>
          m.id === assistantId ? { ...m, content: m.content + token } : m,
        ));
      },
      (sources) => {
        setMessages(prev => prev.map(m =>
          m.id === assistantId ? { ...m, streaming: false, sources } : m,
        ));
        setIsLoading(false);
      },
      (err) => {
        if (err.name !== 'AbortError') {
          setMessages(prev => prev.map(m =>
            m.id === assistantId
              ? { ...m, content: 'Error fetching response. Please try again.', streaming: false }
              : m,
          ));
        }
        setIsLoading(false);
      },
      abortRef.current.signal,
    );
  }, [messages]);

  const stopStreaming = () => {
    abortRef.current?.abort();
    setIsLoading(false);
  };

  const clearChat = () => setMessages([]);

  return { messages, isLoading, sendMessage, stopStreaming, clearChat };
}
