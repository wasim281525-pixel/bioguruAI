const HINGLISH_WORDS = new Set([
  'kya','hai','mein','karo','batao','samjhao','bolo','hota','kaise',
  'yaar','bhai','aur','nahi','dekho','isko','uska','ye','woh','toh',
  'phir','ab','sab','bahut','accha','theek','matlab','lekin','kyunki'
]);

export function detectLanguage(text: string): 'en' | 'hi' | 'hinglish' | 'ur' {
  if (/[\u0600-\u06FF]/.test(text)) return 'ur';
  if (/[\u0900-\u097F]/.test(text)) return 'hi';
  const words = text.toLowerCase().split(/\s+/);
  const hinglishCount = words.filter(w => HINGLISH_WORDS.has(w)).length;
  if (hinglishCount >= 1) return 'hinglish';
  return 'en';
}

export const RTL_LANGS = ['ur'];
export const DEVANAGARI_LANGS = ['hi'];

export function getFontFamily(lang: string): string {
  if (lang === 'ur') return "'Noto Nastaliq Urdu', serif";
  if (lang === 'hi') return "'Noto Sans Devanagari', sans-serif";
  return "'Baloo 2', sans-serif";
}

export function getLangLabel(lang: string): string {
  const map: Record<string, string> = {
    en: '🇬🇧 English',
    hi: '🇮🇳 हिंदी',
    hinglish: '🤙 Hinglish',
    ur: '🇵🇰 اردو',
  };
  return map[lang] || lang;
}
