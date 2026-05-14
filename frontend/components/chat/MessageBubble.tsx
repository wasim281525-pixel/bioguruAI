'use client';
import ReactMarkdown from 'react-markdown';
import { getFontFamily, RTL_LANGS } from '@/lib/langDetect';

interface Props {
  role: 'user' | 'assistant';
  content: string;
  language?: string;
  sources?: string[];
  streaming?: boolean;
}

export function MessageBubble({ role, content, language = 'en', sources, streaming }: Props) {
  const isRTL = RTL_LANGS.includes(language);
  const fontFamily = getFontFamily(language);
  const isAI = role === 'assistant';

  return (
    <div className={`flex gap-3 ${isAI ? '' : 'flex-row-reverse'} animate-fadeIn`}>
      {isAI && (
        <div className="w-8 h-8 rounded-lg bg-green-700 flex items-center justify-center text-lg flex-shrink-0 mt-1">
          🧬
        </div>
      )}
      <div
        className={`max-w-[78%] ${
          isAI
            ? 'bg-white border border-gray-200 rounded-tl-sm rounded-tr-2xl rounded-br-2xl rounded-bl-2xl shadow-sm'
            : 'bg-green-700 text-white rounded-tl-2xl rounded-tr-sm rounded-br-2xl rounded-bl-2xl'
        } px-4 py-3 text-sm leading-relaxed`}
        style={{ fontFamily, direction: isRTL ? 'rtl' : 'ltr', textAlign: isRTL ? 'right' : 'left' }}
      >
        {isAI ? (
          <div className="prose prose-sm max-w-none text-gray-800">
            <ReactMarkdown>{content || (streaming ? '' : '...')}</ReactMarkdown>
          </div>
        ) : (
          <span>{content}</span>
        )}
        {streaming && (
          <span className="inline-block w-1.5 h-4 bg-green-500 ml-0.5 animate-pulse align-middle" />
        )}
        {sources && sources.length > 0 && !streaming && (
          <div className="mt-2 pt-2 border-t border-gray-100 flex flex-wrap gap-1">
            {[...new Set(sources)].map((src, i) => (
              <span key={i} className="inline-flex items-center gap-1 text-xs bg-teal-50 text-teal-700 px-2 py-0.5 rounded-full border border-teal-100">
                📖 {src}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
