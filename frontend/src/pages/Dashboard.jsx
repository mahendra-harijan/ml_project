import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Activity, Users, CheckCircle, XCircle } from 'lucide-react';

const StatCard = ({ title, value, icon: Icon, colorClass }) => (
  <div className="bg-white overflow-hidden shadow rounded-lg border border-gray-100 transition-all hover:shadow-md">
    <div className="p-5">
      <div className="flex items-center">
        <div className="flex-shrink-0">
          <Icon className={`h-6 w-6 ${colorClass}`} aria-hidden="true" />
        </div>
        <div className="ml-5 w-0 flex-1">
          <dl>
            <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
            <dd>
              <div className="text-lg font-medium text-gray-900">{value}</div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
);

const Dashboard = () => {
  const [modelMetrics, setModelMetrics] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const metricsRes = await axios.get('http://localhost:8000/api/model/metrics');
        setModelMetrics(metricsRes.data);
        
        const predsRes = await axios.get('http://localhost:8000/api/predictions');
        setPredictions(predsRes.data);
      } catch (error) {
        console.error("Error fetching dashboard data", error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);

  if (loading) {
    return <div className="flex justify-center items-center h-64"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div></div>;
  }

  const totalPredictions = predictions.length;
  const selectedCount = predictions.filter(p => p.prediction === 'Selected').length;
  const notSelectedCount = totalPredictions - selectedCount;
  
  const avgSkillMatch = totalPredictions > 0 
    ? (predictions.reduce((acc, p) => acc + (p.skill_match_score || 0), 0) / totalPredictions).toFixed(1) 
    : 0;

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Total Screened" value={totalPredictions} icon={Users} colorClass="text-blue-500" />
        <StatCard title="Selected Candidates" value={selectedCount} icon={CheckCircle} colorClass="text-green-500" />
        <StatCard title="Rejected Candidates" value={notSelectedCount} icon={XCircle} colorClass="text-red-500" />
        <StatCard title="Avg Skill Match" value={`${avgSkillMatch}%`} icon={Activity} colorClass="text-purple-500" />
      </div>

      <div className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-2">
        {/* Model Metrics Chart */}
        <div className="bg-white shadow rounded-lg p-6 border border-gray-100">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Model Performance Metrics</h2>
          <div className="h-72">
            {modelMetrics.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={modelMetrics} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="Model" />
                  <YAxis domain={[0, 1]} />
                  <Tooltip cursor={{fill: '#f3f4f6'}} />
                  <Legend />
                  <Bar dataKey="Accuracy" fill="#4f46e5" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="F1" fill="#10b981" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-gray-400 text-sm">
                No model metrics available. Please train models first.
              </div>
            )}
          </div>
        </div>

        {/* Recent History */}
        <div className="bg-white shadow rounded-lg p-6 border border-gray-100">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Recent Predictions</h2>
          <div className="overflow-y-auto h-72 pr-2">
            {predictions.length > 0 ? (
              <ul className="divide-y divide-gray-200">
                {predictions.slice().reverse().map((pred, idx) => (
                  <li key={idx} className="py-4">
                    <div className="flex items-center space-x-4">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {pred.candidate?.name || 'Unknown Candidate'}
                        </p>
                        <p className="text-sm text-gray-500 truncate">
                          {pred.candidate?.education} • {pred.candidate?.experience_years} years exp
                        </p>
                      </div>
                      <div className="inline-flex flex-col items-end">
                        <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          pred.prediction === 'Selected' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {pred.prediction}
                        </span>
                        <span className="text-xs text-gray-400 mt-1">{(pred.probability * 100).toFixed(1)}% prob</span>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="h-full flex items-center justify-center text-gray-400 text-sm">
                No recent predictions.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
