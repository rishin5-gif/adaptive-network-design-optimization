import React, { useState } from 'react';
import { api } from '../services/api';
import {
  FlaskConical,
  Play,
  Download,
  Activity,
  CheckCircle2,
  Clock,
  Layers,
  BarChart2,
  Table
} from 'lucide-react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';

export const ExperimentLab: React.FC = () => {
  const [selectedFamily, setSelectedFamily] = useState<string>('sparse_vs_dense_mst');
  const [trials, setTrials] = useState<number>(3);
  const [running, setRunning] = useState<boolean>(false);
  const [experimentOutput, setExperimentOutput] = useState<any | null>(null);
  const [activeTab, setActiveTab] = useState<'chart' | 'table'>('chart');

  const families = [
    {
      id: 'sparse_vs_dense_mst',
      name: '1. Sparse vs Dense Graphs for Prim & Kruskal',
      desc: 'Compares Prim and Kruskal across sparse (E ≈ 1.5V) and dense (E ≈ 0.7 V(V-1)/2) graphs across V=8, 16, 24, 32.'
    },
    {
      id: 'floyd_warshall_scaling',
      name: '2. Increasing Vertex Counts for Floyd-Warshall',
      desc: 'Measures all-pairs DP latency across V=5, 10, 15, 20, 25, 30 and compares against theoretical O(V³) cubic curve.'
    },
    {
      id: 'tree_workloads',
      name: '3. Identical Record Workloads for B-Tree & Red-Black Tree',
      desc: 'Evaluates key comparisons, node splits, and rotations across workloads of 50, 100, 200, 400 operations.'
    },
    {
      id: 'heap_workloads',
      name: '4. Identical Priority Workloads for Binomial & Fibonacci Heap',
      desc: 'Benchmarks tree links vs cascading cuts across event workloads of 20, 50, 100, 200 items.'
    },
    {
      id: 'knapsack_divisibility',
      name: '5. Divisible vs Indivisible Budget Selection',
      desc: 'Evaluates objective value difference between Fractional Greedy and 0/1 DP Knapsack across budget capacities.'
    },
    {
      id: 'tsp_scaling',
      name: '6. Increasing Small TSP Instances for Exact Search',
      desc: 'Evaluates search states explored vs pruned between Backtracking and Branch & Bound for N=4, 5, 6, 7, 8.'
    }
  ];

  const handleRunExperiment = async () => {
    try {
      setRunning(true);
      const params: Record<string, any> = {};
      if (selectedFamily === 'sparse_vs_dense_mst') params.sizes = [8, 16, 24, 32];
      if (selectedFamily === 'floyd_warshall_scaling') params.sizes = [5, 10, 15, 20, 25, 30];
      if (selectedFamily === 'tree_workloads') { params.scales = [50, 100, 200, 400]; params.b_tree_order = 3; }
      if (selectedFamily === 'heap_workloads') params.scales = [20, 50, 100, 200];
      if (selectedFamily === 'knapsack_divisibility') params.budgets = [20000, 50000, 80000, 120000];
      if (selectedFamily === 'tsp_scaling') params.sizes = [4, 5, 6, 7, 8];

      const res = await api.runExperiment(selectedFamily, params, trials);
      setExperimentOutput(res);
    } catch (err: any) {
      alert('Experiment execution failed: ' + err.message);
    } finally {
      setRunning(false);
    }
  };

  const handleExportCSV = () => {
    window.open(api.getExportUrl(), '_blank');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-blue-100 text-blue-700 rounded-lg">
              <FlaskConical className="w-5 h-5" />
            </span>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">
              Performance Experiment Lab (DAA Empirical Benchmarking)
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Conduct controlled, high-resolution trials using monotonic timers and operation counters across all 6 algorithm families.
          </p>
        </div>

        <button
          onClick={handleExportCSV}
          className="text-xs font-semibold bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 px-3.5 py-2 rounded-lg shadow-sm transition flex items-center space-x-1.5 self-start md:self-auto"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Export All Results to CSV</span>
        </button>
      </div>

      {/* Control Panel: Select Family and Trials */}
      <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-2 space-y-1.5">
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
              Select Benchmark Experiment Family:
            </label>
            <select
              value={selectedFamily}
              onChange={(e) => setSelectedFamily(e.target.value)}
              className="w-full border border-slate-300 rounded-lg px-3 py-2 text-xs font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {families.map(f => (
                <option key={f.id} value={f.id}>{f.name}</option>
              ))}
            </select>
            <p className="text-[11px] text-slate-500 italic mt-1">
              {families.find(f => f.id === selectedFamily)?.desc}
            </p>
          </div>

          <div className="space-y-1.5">
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
              Repetition Trials (Median Filter):
            </label>
            <div className="flex items-center space-x-3">
              <select
                value={trials}
                onChange={(e) => setTrials(Number(e.target.value))}
                className="w-full border border-slate-300 rounded-lg px-3 py-2 text-xs font-semibold text-slate-900"
              >
                <option value={1}>1 Trial (Fast Single Run)</option>
                <option value={3}>3 Trials (Median Filter)</option>
                <option value={5}>5 Trials (High Statistical Confidence)</option>
              </select>

              <button
                onClick={handleRunExperiment}
                disabled={running}
                className="text-xs font-bold bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg transition shadow flex items-center space-x-1.5 flex-shrink-0 disabled:opacity-50"
              >
                <Play className={`w-3.5 h-3.5 fill-current ${running ? 'animate-spin' : ''}`} />
                <span>{running ? 'Benchmarking...' : 'Execute Trial'}</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Experiment Results Container */}
      {experimentOutput && (
        <div className="bg-white border border-slate-200/80 rounded-xl shadow-sm overflow-hidden">
          <div className="px-5 py-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                Benchmark Results: {families.find(f => f.id === experimentOutput.experiment_family)?.name}
              </span>
              <span className="bg-blue-100 text-blue-800 text-[10px] font-bold px-2 py-0.5 rounded-full">
                {experimentOutput.results.trials || trials} Trials
              </span>
            </div>

            <div className="flex items-center space-x-1 bg-slate-200 p-0.5 rounded-lg text-xs font-semibold">
              <button
                onClick={() => setActiveTab('chart')}
                className={`px-3 py-1 rounded-md transition ${activeTab === 'chart' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600'}`}
              >
                Chart View
              </button>
              <button
                onClick={() => setActiveTab('table')}
                className={`px-3 py-1 rounded-md transition ${activeTab === 'table' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600'}`}
              >
                Table View
              </button>
            </div>
          </div>

          <div className="p-6">
            {activeTab === 'chart' ? (
              <div className="h-80 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  {selectedFamily === 'sparse_vs_dense_mst' && (
                    <LineChart data={experimentOutput.results.series} margin={{ top: 10, right: 30, left: 10, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                      <XAxis dataKey="num_vertices" label={{ value: 'Number of Vertices (V)', position: 'insideBottom', offset: -2, fontSize: 11 }} />
                      <YAxis label={{ value: 'Median Runtime (ms)', angle: -90, position: 'insideLeft', fontSize: 11 }} />
                      <Tooltip />
                      <Legend wrapperStyle={{ fontSize: '12px' }} />
                      <Line type="monotone" dataKey="prim_sparse_median_ms" stroke="#2563EB" strokeWidth={2} name="Prim (Sparse)" />
                      <Line type="monotone" dataKey="kruskal_sparse_median_ms" stroke="#0D9488" strokeWidth={2} name="Kruskal (Sparse)" />
                      <Line type="monotone" dataKey="prim_dense_median_ms" stroke="#9333EA" strokeDasharray="3 3" strokeWidth={2} name="Prim (Dense)" />
                      <Line type="monotone" dataKey="kruskal_dense_median_ms" stroke="#F59E0B" strokeDasharray="3 3" strokeWidth={2} name="Kruskal (Dense)" />
                    </LineChart>
                  )}

                  {selectedFamily === 'floyd_warshall_scaling' && (
                    <LineChart data={experimentOutput.results.series} margin={{ top: 10, right: 30, left: 10, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                      <XAxis dataKey="num_vertices" label={{ value: 'Number of Vertices (V)', position: 'insideBottom', offset: -2, fontSize: 11 }} />
                      <YAxis label={{ value: 'Median Time (ms)', angle: -90, position: 'insideLeft', fontSize: 11 }} />
                      <Tooltip />
                      <Legend wrapperStyle={{ fontSize: '12px' }} />
                      <Line type="monotone" dataKey="median_time_ms" stroke="#0D9488" strokeWidth={2.5} name="Measured Runtime (ms)" />
                      <Line type="monotone" dataKey="theoretical_v3" stroke="#94A3B8" strokeDasharray="5 5" name="Theoretical V³ Scale" yAxisId={0} />
                    </LineChart>
                  )}

                  {selectedFamily === 'tree_workloads' && (
                    <BarChart data={experimentOutput.results.series} margin={{ top: 10, right: 30, left: 10, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                      <XAxis dataKey="workload_size" label={{ value: 'Workload Size (Operations)', position: 'insideBottom', offset: -2, fontSize: 11 }} />
                      <YAxis label={{ value: 'Comparisons Count', angle: -90, position: 'insideLeft', fontSize: 11 }} />
                      <Tooltip />
                      <Legend wrapperStyle={{ fontSize: '12px' }} />
                      <Bar dataKey="btree_comparisons" fill="#4F46E5" name="B-Tree Comparisons" />
                      <Bar dataKey="rbt_comparisons" fill="#DC2626" name="Red-Black Tree Comparisons" />
                    </BarChart>
                  )}

                  {selectedFamily === 'heap_workloads' && (
                    <LineChart data={experimentOutput.results.series} margin={{ top: 10, right: 30, left: 10, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                      <XAxis dataKey="events_count" label={{ value: 'Events Count', position: 'insideBottom', offset: -2, fontSize: 11 }} />
                      <YAxis label={{ value: 'Median Time (ms)', angle: -90, position: 'insideLeft', fontSize: 11 }} />
                      <Tooltip />
                      <Legend wrapperStyle={{ fontSize: '12px' }} />
                      <Line type="monotone" dataKey="binomial_median_ms" stroke="#059669" strokeWidth={2} name="Binomial Heap Runtime (ms)" />
                      <Line type="monotone" dataKey="fibonacci_median_ms" stroke="#7C3AED" strokeWidth={2} name="Fibonacci Heap Runtime (ms)" />
                    </LineChart>
                  )}

                  {selectedFamily === 'knapsack_divisibility' && (
                    <BarChart data={experimentOutput.results.series} margin={{ top: 10, right: 30, left: 10, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                      <XAxis dataKey="budget" label={{ value: 'Budget Capacity ($)', position: 'insideBottom', offset: -2, fontSize: 11 }} />
                      <YAxis label={{ value: 'Total Benefit Score', angle: -90, position: 'insideLeft', fontSize: 11 }} />
                      <Tooltip />
                      <Legend wrapperStyle={{ fontSize: '12px' }} />
                      <Bar dataKey="fractional_benefit" fill="#0D9488" name="Fractional Benefit (Divisible)" />
                      <Bar dataKey="dp_benefit" fill="#D97706" name="0/1 DP Benefit (Indivisible)" />
                    </BarChart>
                  )}

                  {selectedFamily === 'tsp_scaling' && (
                    <LineChart data={experimentOutput.results.series} margin={{ top: 10, right: 30, left: 10, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                      <XAxis dataKey="num_locations" label={{ value: 'Locations (N)', position: 'insideBottom', offset: -2, fontSize: 11 }} />
                      <YAxis label={{ value: 'States Explored', angle: -90, position: 'insideLeft', fontSize: 11 }} />
                      <Tooltip />
                      <Legend wrapperStyle={{ fontSize: '12px' }} />
                      <Line type="monotone" dataKey="bt_states_explored" stroke="#EF4444" strokeWidth={2} name="Backtracking States Explored" />
                      <Line type="monotone" dataKey="bb_states_explored" stroke="#8B5CF6" strokeWidth={2} name="Branch & Bound States Explored" />
                      <Line type="monotone" dataKey="bb_states_pruned" stroke="#10B981" strokeDasharray="4 4" strokeWidth={2} name="B&B States Pruned" />
                    </LineChart>
                  )}
                </ResponsiveContainer>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-xs text-left border-collapse">
                  <thead className="bg-slate-100 text-slate-700 uppercase font-semibold">
                    <tr>
                      {Object.keys(experimentOutput.results.series[0] || {}).map((col) => (
                        <th key={col} className="p-2.5 border border-slate-200">{col.replace(/_/g, ' ')}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 font-mono">
                    {experimentOutput.results.series.map((row: any, idx: number) => (
                      <tr key={idx} className="hover:bg-slate-50">
                        {Object.values(row).map((val: any, cIdx: number) => (
                          <td key={cIdx} className="p-2.5 border border-slate-200">
                            {typeof val === 'number' ? val.toLocaleString() : String(val)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
