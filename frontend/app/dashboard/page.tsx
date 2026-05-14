'use client';
import { useEffect, useState } from 'react';
import AppLayout from '@/components/common/AppLayout';
import { apiFetch, getUser } from '@/lib/api';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { BarChart2, BookOpen, MessageSquare, TrendingUp } from 'lucide-react';

export default function DashboardPage() {
  const [data, setData] = useState<any>(null);
  const user = getUser();

  useEffect(() => {
    apiFetch('/api/analytics/dashboard').then(r => r.json()).then(setData).catch(console.error);
  }, []);

  if (!data) {
    return (
      <AppLayout>
        <div className="flex items-center justify-center h-full">
          <div className="text-green-600 animate-pulse">Loading dashboard...</div>
        </div>
      </AppLayout>
    );
  }

  const chartData = (data.recent_tests || [])
    .slice().reverse()
    .map((s: any, i: number) => ({ test: `T${i + 1}`, score: parseFloat(s.score_pct.toFixed(1)) }));

  return (
    <AppLayout>
      <div className="flex-1 overflow-y-auto bg-gray-50 px-6 py-6">
        <div className="max-w-4xl mx-auto space-y-6">
          <div>
            <h1 className="text-xl font-bold text-gray-800">Welcome back, {user?.name?.split(' ')[0]} 👋</h1>
            <p className="text-sm text-gray-500">Class {user?.class_level} | Keep up the momentum!</p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { icon: BookOpen, label: 'Tests Taken', value: data.neet?.total_tests || 0, color: 'text-green-600 bg-green-50' },
              { icon: TrendingUp, label: 'Avg Score', value: `${data.neet?.avg_score || 0}%`, color: 'text-blue-600 bg-blue-50' },
              { icon: BarChart2, label: 'Best Score', value: `${data.neet?.best_score || 0}%`, color: 'text-purple-600 bg-purple-50' },
              { icon: MessageSquare, label: 'Chat Sessions', value: data.chat_sessions || 0, color: 'text-orange-600 bg-orange-50' },
            ].map(({ icon: Icon, label, value, color }) => (
              <div key={label} className="bg-white rounded-2xl border border-gray-200 p-5 shadow-sm">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-3 ${color}`}>
                  <Icon size={20} />
                </div>
                <div className="text-2xl font-bold text-gray-800">{value}</div>
                <div className="text-xs text-gray-500 mt-0.5">{label}</div>
              </div>
            ))}
          </div>

          {/* Score trend chart */}
          {chartData.length > 0 && (
            <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-sm">
              <h2 className="font-semibold text-gray-700 mb-4">Score Trend</h2>
              <ResponsiveContainer width="100%" height={180}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="test" tick={{ fontSize: 12 }} />
                  <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
                  <Tooltip formatter={(v: any) => `${v}%`} />
                  <Line type="monotone" dataKey="score" stroke="#15803d" strokeWidth={2} dot={{ r: 4 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Recent tests table */}
          {data.recent_tests?.length > 0 && (
            <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-sm">
              <h2 className="font-semibold text-gray-700 mb-4">Recent Tests</h2>
              <div className="space-y-2">
                {data.recent_tests.map((s: any, i: number) => (
                  <div key={i} className="flex items-center gap-4 text-sm py-2 border-b border-gray-50 last:border-0">
                    <span className="text-gray-400 w-6 text-right">{i + 1}.</span>
                    <div className="flex-1">
                      <div className="font-medium text-gray-700">{s.correct}/{s.total_q} correct</div>
                      <div className="text-xs text-gray-400">{new Date(s.created_at).toLocaleDateString()}</div>
                    </div>
                    <span className={`font-bold px-3 py-1 rounded-full text-xs ${
                      s.score_pct >= 70 ? 'bg-green-100 text-green-700' :
                      s.score_pct >= 50 ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-700'
                    }`}>{s.score_pct.toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {data.recent_tests?.length === 0 && (
            <div className="bg-white rounded-2xl border border-gray-200 p-10 text-center shadow-sm">
              <div className="text-4xl mb-3">📚</div>
              <p className="text-gray-500 text-sm">No tests yet. Start your NEET practice to see progress here!</p>
            </div>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
