import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Vertex, Edge, FloydWarshallResult, PathResult, AlgorithmExplanation } from '../types';
import { ExplanationCard } from '../components/ExplanationCard';
import {
  Network,
  Play,
  RotateCcw,
  Navigation,
  AlertTriangle,
  Info,
  Sliders,
  TrendingUp,
  Activity
} from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';

export const CommunicationCost: React.FC = () => {
  const [vertices, setVertices] = useState<Vertex[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [result, setResult] = useState<FloydWarshallResult | null>(null);
  const [explanation, setExplanation] = useState<AlgorithmExplanation | null>(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);

  // Path Inspector State
  const [pathSource, setPathSource] = useState<string>('');
  const [pathTarget, setPathTarget] = useState<string>('');
  const [pathResult, setPathResult] = useState<PathResult | null>(null);
  const [reconstructingPath, setReconstructingPath] = useState(false);

  // Scaling Experiment State for Chart
  const [scalingData, setScalingData] = useState<any[]>([]);
  const [measuringScaling, setMeasuringScaling] = useState(false);

  useEffect(() => {
    loadNetwork();
  }, []);

  const loadNetwork = async () => {
    try {
      setLoading(true);
      const data = await api.getNetwork();
      setVertices(data.vertices);
      setEdges(data.edges);
      if (data.vertices.length > 0) {
        setPathSource(data.vertices[0].id);
        setPathTarget(data.vertices[1]?.id || data.vertices[0].id);
        await runFW(data.vertices, data.edges);
      }
    } catch (err: any) {
      alert('Failed to load network: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const runFW = async (vList = vertices, eList = edges) => {
    try {
      setRunning(true);
      const vIds = vList.map(v => v.id);
      const edgeTuples: [string, string, number][] = eList.map(e => [e.source, e.target, Number(e.weight)]);
      const res = await api.runFloydWarshall(vIds, edgeTuples);
      setResult(res.result);
      setExplanation(res.explanation);
    } catch (err: any) {
      alert('Floyd-Warshall execution failed: ' + err.message);
    } finally {
      setRunning(false);
    }
  };

  const handleInspectPath = async () => {
    if (!pathSource || !pathTarget) return;
    try {
      setReconstructingPath(true);
      const vIds = vertices.map(v => v.id);
      const edgeTuples: [string, string, number][] = edges.map(e => [e.source, e.target, Number(e.weight)]);
      const res = await api.getPath(pathSource, pathTarget, vIds, edgeTuples);
      setPathResult(res);
    } catch (err: any) {
      alert('Failed to reconstruct path: ' + err.message);
    } finally {
      setReconstructingPath(false);
    }
  };

  const handleRunScalingTest = async () => {
    try {
      setMeasuringScaling(true);
      const res = await api.runExperiment('floyd_warshall_scaling', {
        sizes: [5, 10, 15, 20, 25, 30]
      }, 2);
      const series = res.results.series.map((pt: any) => ({
        vertices: pt.num_vertices,
        measuredMs: pt.median_time_ms,
        theoreticalV3Norm: (pt.theoretical_v3 / 27000) * (pt.median_time_ms || 1), // Normalized reference curve
        relaxations: pt.actual_triplet_relaxations
      }));
      setScalingData(series);
    } catch (err: any) {
      alert('Scaling benchmark failed: ' + err.message);
    } finally {
      setMeasuringScaling(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-teal-100 text-teal-700 rounded-lg">
              <Network className="w-5 h-5" />
            </span>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">
              Module 2: All-Pairs Communication Cost Analysis
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Dynamic programming calculation of shortest-path latencies and multi-hop transit matrix via Floyd-Warshall.
          </p>
        </div>

        <button
          onClick={() => runFW()}
          disabled={running || vertices.length === 0}
          className="text-xs font-semibold bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 rounded-lg shadow-sm transition flex items-center space-x-1.5 self-start md:self-auto disabled:opacity-50"
        >
          <Play className={`w-3.5 h-3.5 fill-current ${running ? 'animate-spin' : ''}`} />
          <span>{running ? 'Computing DP...' : 'Run Floyd-Warshall'}</span>
        </button>
      </div>

      {/* Explanation Engine Display */}
      <ExplanationCard explanation={explanation} />

      {/* Distance Matrix Card */}
      {result && (
        <div className="bg-white border border-slate-200/80 rounded-xl shadow-sm overflow-hidden">
          <div className="px-5 py-3.5 bg-slate-50 border-b border-slate-200 flex flex-wrap items-center justify-between gap-2">
            <div>
              <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                All-Pairs Distance Matrix D ({result.num_vertices} × {result.num_vertices})
              </h3>
              <p className="text-[11px] text-slate-500 mt-0.5">
                Evaluated {result.total_triplet_relaxations.toLocaleString()} triplet combinations • {result.total_distance_updates} distance improvements
              </p>
            </div>
            <div className="flex items-center space-x-2 text-xs font-mono">
              <span className="bg-slate-200 text-slate-700 px-2.5 py-1 rounded">
                Time: {result.execution_time_ms.toFixed(3)} ms
              </span>
              <span className="bg-teal-100 text-teal-800 px-2.5 py-1 rounded font-semibold">
                Complexity: O(V³)
              </span>
            </div>
          </div>

          {result.has_negative_cycle && (
            <div className="bg-red-50 border-b border-red-200 p-3 text-xs text-red-800 flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4 text-red-600 flex-shrink-0" />
              <span>
                <strong>Negative Cycle Detected:</strong> Nodes {result.negative_cycle_nodes.join(', ')} participate in negative-weight loops. Shortest paths undefined.
              </span>
            </div>
          )}

          {/* Matrix Scrollable View */}
          <div className="overflow-x-auto p-4">
            <table className="w-full text-xs text-center border-collapse">
              <thead>
                <tr>
                  <th className="p-2 border border-slate-200 bg-slate-100 font-bold text-slate-600 uppercase">
                    From \ To
                  </th>
                  {result.vertices.map((v) => (
                    <th key={`col-${v}`} className="p-2 border border-slate-200 bg-slate-50 font-mono font-semibold text-slate-700">
                      {v}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {result.distance_matrix.map((row, rIdx) => {
                  const sourceNode = result.vertices[rIdx];
                  return (
                    <tr key={`row-${sourceNode}`} className="hover:bg-slate-50/60">
                      <td className="p-2 border border-slate-200 bg-slate-50 font-mono font-bold text-slate-700 text-left">
                        {sourceNode}
                      </td>
                      {row.map((cost, cIdx) => {
                        const targetNode = result.vertices[cIdx];
                        const isDiagonal = rIdx === cIdx;
                        const isUnreachable = cost === null;

                        return (
                          <td
                            key={`cell-${sourceNode}-${targetNode}`}
                            className={`p-2 border border-slate-200 font-mono ${
                              isDiagonal
                                ? 'bg-blue-50/80 font-bold text-blue-800'
                                : isUnreachable
                                ? 'bg-slate-100 text-slate-400 font-bold'
                                : 'text-slate-900'
                            }`}
                          >
                            {isUnreachable ? '∞' : cost?.toFixed(1)}
                          </td>
                        );
                      })}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          <div className="px-5 py-2.5 bg-slate-50 text-[11px] text-slate-500 border-t border-slate-200 flex items-center justify-between">
            <span>Diagonal elements D[i][i] = 0. Values represent minimum delay/cost across all intermediate hops k.</span>
            <span>Unreachable pairs indicated by ∞</span>
          </div>
        </div>
      )}

      {/* Path Reconstruction Tool & Scaling Benchmark Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Path Inspector */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center space-x-2">
            <Navigation className="w-4 h-4 text-teal-600" />
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Optimal Route Inspector (Predecessor Matrix Π)
            </h3>
          </div>
          <p className="text-xs text-slate-500">
            Reconstruct intermediate routing hops using the predecessor matrix updated during Floyd-Warshall relaxations.
          </p>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Source Site (From):</label>
              <select
                value={pathSource}
                onChange={(e) => setPathSource(e.target.value)}
                className="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-900"
              >
                {vertices.map(v => <option key={v.id} value={v.id}>{v.id} - {v.label}</option>)}
              </select>
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Destination Site (To):</label>
              <select
                value={pathTarget}
                onChange={(e) => setPathTarget(e.target.value)}
                className="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-900"
              >
                {vertices.map(v => <option key={v.id} value={v.id}>{v.id} - {v.label}</option>)}
              </select>
            </div>
          </div>

          <button
            onClick={handleInspectPath}
            disabled={reconstructingPath}
            className="w-full text-xs font-semibold bg-teal-50 hover:bg-teal-100 text-teal-800 border border-teal-200 py-2 rounded-lg transition"
          >
            {reconstructingPath ? 'Reconstructing...' : 'Inspect Shortest Route & Hops'}
          </button>

          {pathResult && (
            <div className="bg-slate-50 border border-slate-200 rounded-lg p-3.5 space-y-2 text-xs">
              <div className="flex justify-between font-semibold">
                <span className="text-slate-600">Total Path Latency/Cost:</span>
                <span className="font-mono text-teal-700 font-bold">
                  {pathResult.cost !== null ? `${pathResult.cost} units` : 'Unreachable'}
                </span>
              </div>
              <div>
                <span className="text-slate-600 block mb-1 font-semibold">Sequential Hop Sequence:</span>
                {pathResult.is_reachable ? (
                  <div className="flex flex-wrap items-center gap-1.5 font-mono">
                    {pathResult.path.map((node, idx) => (
                      <React.Fragment key={idx}>
                        <span className="bg-white border border-slate-300 px-2 py-0.5 rounded font-bold text-slate-800">
                          {node}
                        </span>
                        {idx < pathResult.path.length - 1 && (
                          <span className="text-teal-600 font-bold">→</span>
                        )}
                      </React.Fragment>
                    ))}
                  </div>
                ) : (
                  <span className="text-red-600 font-semibold">No valid path connects these two sites.</span>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Right: Theoretical vs Empirical O(V³) Scaling Chart */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-4 h-4 text-blue-600" />
              <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                Theoretical vs Measured O(V³) Growth
              </h3>
            </div>
            <button
              onClick={handleRunScalingTest}
              disabled={measuringScaling}
              className="text-xs bg-blue-50 text-blue-700 hover:bg-blue-100 font-semibold px-2.5 py-1 rounded border border-blue-200 transition"
            >
              {measuringScaling ? 'Benchmarking...' : 'Run Scaling Benchmark'}
            </button>
          </div>

          <p className="text-xs text-slate-500">
            Measures execution time against vertex count V, validating the cubic recurrence behaviour across 3 nested loops.
          </p>

          {scalingData.length > 0 ? (
            <div className="h-48 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={scalingData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="vertices" label={{ value: 'Vertices (V)', position: 'insideBottom', offset: -2, fontSize: 10 }} fontSize={11} />
                  <YAxis label={{ value: 'Time (ms)', angle: -90, position: 'insideLeft', fontSize: 10 }} fontSize={11} />
                  <Tooltip />
                  <Legend wrapperStyle={{ fontSize: '11px' }} />
                  <Line type="monotone" dataKey="measuredMs" stroke="#0D9488" strokeWidth={2} name="Measured Runtime (ms)" />
                  <Line type="monotone" dataKey="theoreticalV3Norm" stroke="#64748B" strokeDasharray="5 5" name="O(V³) Reference Curve" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="h-48 bg-slate-50 border border-slate-200/60 rounded-lg flex items-center justify-center text-xs text-slate-400">
              Click 'Run Scaling Benchmark' to generate runtime curves across V=5 to V=30.
            </div>
          )}

          <div className="bg-slate-50 p-3 rounded text-[11px] text-slate-600 leading-relaxed border border-slate-100">
            <strong>DAA Algorithmic Note:</strong> Floyd-Warshall checks all V³ triplets (i, k, j) where k is the candidate intermediate node. Doubling V increases relaxations by 8×, explaining why all-pairs DP is ideal for metropolitan backbones (V ≤ 500) but unsuitable for global internet graphs.
          </div>
        </div>
      </div>
    </div>
  );
};
