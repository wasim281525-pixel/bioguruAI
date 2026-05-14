'use client';
import { useState } from 'react';

type Lang = 'en' | 'hi' | 'hinglish' | 'ur';

export function useLanguage(initial: Lang = 'en') {
  const [language, setLanguage] = useState<Lang>(initial);
  return { language, setLanguage };
}
