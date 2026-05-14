'use client';

interface Props {
  correct: number;
  wrong: number;
  skipped: number;
  total: number;
  scorePct: number;
  neetScore: number;
  timeTaken: number;
  onRetry: () => void;
  onNewTopic: () => void;
}

export function ScoreBoard({ correct, wrong, skipped, total, scorePct, neetScore, timeTaken, onRetry, onNewTopic }: Props) {
  const grade = scorePct >= 80 ? '🏆 Excellent!' : scorePct >= 60 ? '👍 Good Job!' : scorePct >= 40 ? '📚 Keep Studying!' : '💪 Practice More!';
  const mins = Math.floor(timeTaken / 60);
  const secs = timeTaken % 60;

  return (
    <div className="max-w-lg mx-auto bg-white rounded-2xl border border-gray-200 shadow-lg p-8 text-center">
      <div className="text-4xl mb-2">{grade.split(' ')[0]}</div>
      <h2 className="text-xl font-bold text-gray-800 mb-1">{grade.slice(2)}</h2>
      <p className="text-sm text-gray-500 mb-6">Test completed in {mins}m {secs}s</p>

      <div className="grid grid-cols-4 gap-3 mb-6">
        {[
          { label: 'Correct', value: correct, color: 'text-green-600 bg-green-50' },
          { label: 'Wrong', value: wrong, color: 'text-red-600 bg-red-50' },
          { label: 'Skipped', value: skipped, color: 'text-gray-600 bg-gray-50' },
          { label: 'Total', value: total, color: 'text-blue-600 bg-blue-50' },
        ].map(s => (
          <div key={s.label} className={`rounded-xl p-3 ${s.color}`}>
            <div className="text-xl font-bold">{s.value}</div>
            <div className="text-xs mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>

      <div className="bg-green-50 rounded-xl p-4 mb-6">
        <div className="text-3xl font-bold text-green-700">{scorePct.toFixed(1)}%</div>
        <div className="text-sm text-green-600 mt-1">NEET Score: <strong>{neetScore}</strong> marks</div>
        <p className="text-xs text-gray-400 mt-1">(+4 correct, −1 wrong)</p>
      </div>

      <div className="flex gap-3">
        <button onClick={onRetry} className="flex-1 border-2 border-green-700 text-green-700 font-semibold py-2.5 rounded-xl hover:bg-green-50 transition">
          Retry
        </button>
        <button onClick={onNewTopic} className="flex-1 bg-green-700 text-white font-semibold py-2.5 rounded-xl hover:bg-green-800 transition">
          New Topic
        </button>
      </div>
    </div>
  );
}
