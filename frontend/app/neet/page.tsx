'use client';
import { useState, useCallback } from 'react';
import AppLayout from '@/components/common/AppLayout';
import { MCQCard } from '@/components/neet/MCQCard';
import { TimerBar } from '@/components/neet/TimerBar';
import { ScoreBoard } from '@/components/neet/ScoreBoard';
import { authHeaders } from '@/lib/api';
import { BookOpen, Loader2, Play } from 'lucide-react';

type Phase = 'setup' | 'loading' | 'quiz' | 'result';

const TOPICS = [
  'Cell Biology', 'Photosynthesis', 'Respiration', 'Genetics & Heredity',
  'Human Reproduction', 'Molecular Biology & DNA', 'Evolution',
  'Plant Morphology', 'Animal Kingdom', 'Ecosystem & Biodiversity',
  'Digestion & Nutrition', 'Circulation & Blood', 'Nervous System',
  'Endocrine System', 'Biotechnology',
];

export default function NEETPage() {
  const [phase, setPhase] = useState<Phase>('setup');
  const [topic, setTopic] = useState('Cell Biology');
  const [count, setCount] = useState(10);
  const [difficulty, setDifficulty] = useState('medium');
  const [questions, setQuestions] = useState<any[]>([]);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [sessionId, setSessionId] = useState('');
  const [result, setResult] = useState<any>(null);
  const [startTime, setStartTime] = useState(0);
  const [timerRunning, setTimerRunning] = useState(false);

  const TIMER_SECS = count * 90; // 90 sec per question

  const startQuiz = async () => {
    setPhase('loading');
    try {
      const res = await fetch('/api/neet/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeaders() },
        body: JSON.stringify({ topic, count, difficulty }),
      });
      const data = await res.json();
      setQuestions(data.questions);
      setSessionId(data.session_id);
      setAnswers({});
      setStartTime(Date.now());
      setTimerRunning(true);
      setPhase('quiz');
    } catch (e) {
      alert('Failed to generate questions. Check your API key.');
      setPhase('setup');
    }
  };

  const handleAnswer = (qIndex: number, answer: string) => {
    setAnswers(prev => ({ ...prev, [qIndex]: answer }));
  };

  const handleSubmit = useCallback(async () => {
    setTimerRunning(false);
    const timeTaken = Math.floor((Date.now() - startTime) / 1000);
    const answerList = questions.map((_, i) => answers[i] || '');

    try {
      const res = await fetch('/api/neet/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeaders() },
        body: JSON.stringify({ session_id: sessionId, questions, answers: answerList, time_taken: timeTaken }),
      });
      const data = await res.json();
      setResult({ ...data, timeTaken });
      setPhase('result');
    } catch {
      alert('Submit failed. Please try again.');
    }
  }, [answers, questions, sessionId, startTime]);

  const handleTimeUp = useCallback(() => {
    handleSubmit();
  }, [handleSubmit]);

  const answeredCount = Object.keys(answers).length;

  return (
    <AppLayout>
      <div className="flex-1 overflow-y-auto bg-gray-50">
        {phase === 'setup' && (
          <div className="max-w-xl mx-auto px-4 py-10">
            <div className="text-center mb-8">
              <div className="w-14 h-14 bg-green-700 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <BookOpen size={28} className="text-white" />
              </div>
              <h1 className="text-2xl font-bold text-green-800">NEET Practice Mode</h1>
              <p className="text-gray-500 text-sm mt-1">AI-generated NCERT Biology MCQs</p>
            </div>

            <div className="bg-white rounded-2xl border border-gray-200 p-6 space-y-5 shadow-sm">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Topic</label>
                <select value={topic} onChange={e => setTopic(e.target.value)}
                  className="w-full border border-gray-300 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-500">
                  {TOPICS.map(t => <option key={t}>{t}</option>)}
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Questions</label>
                  <select value={count} onChange={e => setCount(Number(e.target.value))}
                    className="w-full border border-gray-300 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-500">
                    {[5, 10, 15, 20, 30].map(n => <option key={n} value={n}>{n} Questions</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Difficulty</label>
                  <select value={difficulty} onChange={e => setDifficulty(e.target.value)}
                    className="w-full border border-gray-300 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-500">
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                  </select>
                </div>
              </div>

              <div className="bg-green-50 rounded-xl p-4 text-sm text-green-800">
                <strong>Marking Scheme:</strong> +4 correct | −1 wrong | 0 skipped
              </div>

              <button onClick={startQuiz}
                className="w-full bg-green-700 hover:bg-green-800 text-white font-semibold py-3 rounded-xl flex items-center justify-center gap-2 transition">
                <Play size={18} /> Start Practice Test
              </button>
            </div>
          </div>
        )}

        {phase === 'loading' && (
          <div className="flex flex-col items-center justify-center h-full py-24 gap-4">
            <Loader2 size={36} className="animate-spin text-green-600" />
            <p className="text-green-700 font-medium">Generating {count} questions on {topic}...</p>
            <p className="text-xs text-gray-400">Powered by Claude AI</p>
          </div>
        )}

        {phase === 'quiz' && questions.length > 0 && (
          <div className="max-w-2xl mx-auto px-4 py-6">
            <div className="bg-white rounded-2xl border border-gray-200 p-4 mb-6 shadow-sm space-y-3">
              <div className="flex items-center justify-between">
                <h2 className="font-bold text-green-800">{topic}</h2>
                <span className="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium">
                  {answeredCount}/{questions.length} answered
                </span>
              </div>
              <TimerBar totalSeconds={TIMER_SECS} onTimeUp={handleTimeUp} running={timerRunning} />
            </div>

            <div className="space-y-4 mb-6">
              {questions.map((q, i) => (
                <MCQCard key={i} index={i} question={q.question} options={q.options}
                  selectedAnswer={answers[i]} onAnswer={ans => handleAnswer(i, ans)} />
              ))}
            </div>

            <button onClick={handleSubmit}
              className="w-full bg-green-700 hover:bg-green-800 text-white font-bold py-3 rounded-xl transition">
              Submit Test ({answeredCount}/{questions.length} answered)
            </button>
          </div>
        )}

        {phase === 'result' && result && (
          <div className="max-w-xl mx-auto px-4 py-10">
            <ScoreBoard
              correct={result.correct} wrong={result.wrong} skipped={result.skipped}
              total={result.total} scorePct={result.score_pct} neetScore={result.neet_score}
              timeTaken={result.timeTaken}
              onRetry={() => { setPhase('setup'); }}
              onNewTopic={() => { setPhase('setup'); setTopic(TOPICS[Math.floor(Math.random() * TOPICS.length)]); }}
            />

            {result.details && (
              <div className="mt-6 space-y-3">
                <h3 className="font-bold text-gray-800">Answer Review</h3>
                {result.details.map((d: any, i: number) => (
                  <div key={i} className={`bg-white rounded-xl border p-4 text-sm ${
                    d.result === 'correct' ? 'border-green-200' : d.result === 'wrong' ? 'border-red-200' : 'border-gray-200'
                  }`}>
                    <div className="flex gap-2 mb-2">
                      <span>{d.result === 'correct' ? '✅' : d.result === 'wrong' ? '❌' : '⏭️'}</span>
                      <span className="font-medium text-gray-700">{d.question}</span>
                    </div>
                    <div className="text-xs text-gray-500 space-y-0.5 pl-6">
                      {d.result !== 'skipped' && <div>Your answer: <strong>{d.user_answer}</strong></div>}
                      <div>Correct: <strong className="text-green-700">{d.correct_answer}</strong></div>
                      {d.explanation && <div className="mt-1 text-gray-600 italic">{d.explanation}</div>}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </AppLayout>
  );
}
