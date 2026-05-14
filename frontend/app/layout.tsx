import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'BioGuru AI — NEET Biology Tutor',
  description: 'AI-powered NEET Biology tutor. Ask in English, Hindi, Hinglish or Urdu.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600&family=Noto+Nastaliq+Urdu:wght@400;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-gray-50 text-gray-900 font-sans">{children}</body>
    </html>
  );
}
