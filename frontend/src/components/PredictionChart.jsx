import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function PredictionChart({ probability = 0.5 }) {
  const churnPct = parseFloat((probability * 100).toFixed(1));
  const stayPct = parseFloat(((1 - probability) * 100).toFixed(1));

  const data = [
    { name: 'Retention Probability', value: stayPct, color: '#10b981' },
    { name: 'Churn Risk', value: churnPct, color: probability >= 0.7 ? '#ef4444' : '#f59e0b' },
  ];

  return (
    <div className="my-3">
      <h6 className="text-uppercase text-muted fw-bold mb-3" style={{ letterSpacing: '1px', fontSize: '0.8rem' }}>
        Probability Breakdown Comparison
      </h6>
      <div style={{ width: '100%', height: 180 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
            <XAxis dataKey="name" stroke="#94a3b8" tick={{ fontSize: 12 }} />
            <YAxis domain={[0, 100]} stroke="#94a3b8" tickFormatter={(v) => `${v}%`} />
            <Tooltip
              formatter={(val) => [`${val}%`, 'Probability']}
              contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
            />
            <Bar dataKey="value" radius={[6, 6, 0, 0]}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
