'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Sidebar } from '@/components/common/Sidebar';

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    if (!token) router.replace('/login');
  }, [router]);

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-hidden flex flex-col">{children}</main>
    </div>
  );
}
