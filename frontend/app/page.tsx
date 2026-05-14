'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();
  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    if (token) {
      router.replace('/chat');
    } else {
      router.replace('/login');
    }
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-green-50">
      <div className="flex flex-col items-center gap-3">
        <div className="text-5xl animate-bounce">🧬</div>
        <p className="text-green-700 font-semibold text-lg">Loading BioGuru AI...</p>
      </div>
    </div>
  );
}
