'use client';
import { useEffect, useState } from 'react';
import { Clock } from 'lucide-react';

interface Props {
  totalSeconds: number;
  onTimeUp: () => void;
  running: boolean;
}

export function TimerBar({ totalSeconds, onTimeUp, running }: Props) {
  const [remaining, setRemaining] = useState(totalSeconds);

  useEffect(() => {
    setRemaining(totalSeconds);
  }, [totalSeconds]);

  useEffect(() => {
    if (!running) return;
    const interval = setInterval(() => {
      setRemaining(prev => {
        if (prev <= 1) { clearInterval(interval); onTimeUp(); return 0; }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [running, onTimeUp]);

  const pct = Math.max(0, (remaining / totalSeconds) * 100);
  const mins = Math.floor(remaining / 60).toString().padStart(2, '0');
  const secs = (remaining % 60).toString().padStart(2, '0');
  const color = pct > 50 ? 'bg-green-500' : pct > 25 ? 'bg-yellow-500' : 'bg-red-500';

  return (
    <div className="flex items-center gap-3">
      <Clock size={16} className={pct < 25 ? 'text-red-500 animate-pulse' : 'text-gray-500'} />
      <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
        <div className={`h-full ${color} transition-all duration-1000`} style={{ width: `${pct}%` }} />
      </div>
      <span className={`text-sm font-mono font-bold ${pct < 25 ? 'text-red-600' : 'text-gray-700'}`}>
        {mins}:{secs}
      </span>
    </div>
  );
}
