'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { logout, getUser } from '@/lib/api';
import { MessageSquare, BookOpen, BarChart2, Settings, LogOut } from 'lucide-react';

const NAV = [
  { href: '/chat', icon: MessageSquare, label: 'Chat' },
  { href: '/neet', icon: BookOpen, label: 'NEET Practice' },
  { href: '/dashboard', icon: BarChart2, label: 'Dashboard' },
];

export function Sidebar() {
  const pathname = usePathname();
  const user = getUser();

  return (
    <div className="w-60 h-full bg-green-900 text-white flex flex-col">
      <div className="px-4 py-5 border-b border-green-800">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🧬</span>
          <div>
            <h1 className="font-bold text-base leading-tight">BioGuru AI</h1>
            <p className="text-xs text-green-300">NEET Biology Tutor</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1">
        {NAV.map(({ href, icon: Icon, label }) => {
          const active = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition ${
                active
                  ? 'bg-green-700 text-white'
                  : 'text-green-200 hover:bg-green-800 hover:text-white'
              }`}
            >
              <Icon size={16} />
              {label}
            </Link>
          );
        })}
      </nav>

      <div className="px-3 py-4 border-t border-green-800">
        {user && (
          <div className="px-3 py-2 mb-2">
            <p className="text-sm font-semibold truncate">{user.name}</p>
            <p className="text-xs text-green-300">Class {user.class_level}</p>
          </div>
        )}
        <button
          onClick={logout}
          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-green-200 hover:bg-green-800 hover:text-white transition"
        >
          <LogOut size={16} />
          Logout
        </button>
      </div>
    </div>
  );
}
