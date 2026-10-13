import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Vertex, Edge, TSPResult, AlgorithmExplanation } from '../types';
import { NetworkGraph } from '../components/NetworkGraph';
import { ExplanationCard } from '../components/ExplanationCard';
import {
  Compass,
  Play,
  RotateCcw,
  AlertTriangle,
  CheckCircle2,
  Activity,
  Layers,
  MapPin,
  Clock,
  ShieldAlert
} from 'lucide-react';

export const RoutePlanner: React.FC = () => {
  const [vertices, setVertices] = useState<Vertex[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [selectedLocations, setSelectedLocations] = useState<string[]>([]);
  const [startLocation, setStartLocation] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [solving, setSolving] = useState(false);

  // Results
  const [backtrackingResult, setBacktrackingResult] = useState<TSPResult | null>(null);
  const [branchAndBoundResult, setBranchAndBoundResult] = useState<TSPResult | null>(null);
  const [comparison, setComparison] = useState<any | null>(null);
  const [explanation, setExplanation] = useState<AlgorithmExplanation | null>(null);
  const [selectedSolver, setSelectedSolver] = useState<'both' | 'backtracking' | 'branch_and_bound'>('both');

  useEffect(() => {
    loadNetwork();
  }, []);

  const loadNetwork = async () => {
    try {
      setLoading(true);
      const data = await api.getNetwork();
      setVertices(data.vertices);
      setEdges(data.edges);
      // Pick first 5 locations by default
      const defaultSubset = data.vertices.slice(0, 5).map(v => v.id);
      setSelectedLocations(defaultSubset);
      if (defaultSubset.length > 0) {
        setStartLocation(defaultSubset[0]);
        await solveTSP(defaultSubset, defaultSubset[0], data.vertices, data.edges);
      }
    } catch (err: any) {
      alert('Failed to load network: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const buildCostMatrix = (locs: string[], allV: Vertex[], allE: Edge[]): Record<string, Record<string, number>> => {
    const coords: Record<string, { x: number; y: number }> = {};
    allV.forEach((v, idx) => {
      coords[v.id] = { x: v.x || (100 + idx * 50), y: v.y || (100 + idx * 40) };
    });

    const matrix: Record<string, Record<string, number>> = {};
    locs.forEach(u => {
      matrix[u] = {};
      locs.forEach(v => {
        if (u === v) {
          matrix[u][v] = 0.0;
        } else {
          // Check if direct edge exists
          const direct = allE.find(e => (e.source === u && e.target === v) || (e.source === v && e.target === u));
          if (direct) {
            matrix[u][v] = Number(direct.weight);
          } else {
            // Euclidean metric distance fallback
            const p1 = coords[u] || { x: 0, y: 0 };
            const p2 = coords[v] || { x: 100, y: 100 };
            const dist = Math.round(Math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2) / 10 * 10) / 10;
            matrix[u][v] = dist;
          }
        }
      });
    });
    return matrix;
  };

  const solveTSP = async (locs = selectedLocations, start = startLocation, allV = vertices, allE = edges) => {
    if (locs.length < 2) return;
    if (locs.length > 12) {
      alert('Instance size n > 12 exceeds practical safety limit for exact CPU search.');
      return;
    }

    try {
      setSolving(true);
      const matrix = buildCostMatrix(locs, allV, allE);

      if (selectedSolver === 'backtracking') {
        const res = await api.runTSPBacktracking(locs, matrix, start);
        setBacktrackingResult(res.result);
        setBranchAndBoundResult(null);
        setComparison(null);
        setExplanation(res.explanation);
      } else if (selectedSolver === 'branch_and_bound') {
        const res = await api.runTSPBranchAndBound(locs, matrix, start);
        setBranchAndBoundResult(res.result);
        setBacktrackingResult(null);
        setComparison(null);
        setExplanation(res.explanation);
      } else {
        const comp = await api.compareTSP(locs, matrix, start);
        setBacktrackingResult(comp.backtracking);
        setBranchAndBoundResult(comp.branch_and_bound);
        setComparison(comp);
        setExplanation(comp.explanation);
      }
    } catch (err: any) {
      alert('TSP solver error: ' + err.message);
    } finally {
      setSolving(false);
    }
  };

  const toggleLocation = (id: string) => {
    let next: string[];
    if (selectedLocations.includes(id)) {
      if (selectedLocations.length <= 3) {
        alert('A minimum of 3 locations is required for a valid TSP cycle.');
        return;
      }
      next = selectedLocations.filter(x => x !== id);
    } else {
      if (selectedLocations.length >= 10) {
        alert('Maximum of 10 locations recommended to avoid factorial state space explosion.');
        return;
      }
      next = [...selectedLocations, id];
    }
    setSelectedLocations(next);
    if (!next.includes(startLocation)) {
      setStartLocation(next[0]);
    }
    solveTSP(next, next.includes(startLocation) ? startLocation : next[0]);
  };

  const activeTour = branchAndBoundResult?.optimal_tour || backtrackingResult?.optimal_tour || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-purple-100 text-purple-700 rounded-lg">
              <Compass className="w-5 h-5" />
            </span>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">
              Module 6: Maintenance Route Planner (Exact TSP)
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Solve the Travelling Salesperson Problem using Exact Backtracking and Branch & Bound lower bounding.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <select
            value={selectedSolver}
            onChange={(e) => setSelectedSolver(e.target.value as any)}
            className="text-xs bg-white border border-slate-300 rounded-lg px-3 py-2 font-semibold text-slate-700 shadow-sm"
          >
            <option value="both">Compare Both (B&B vs Backtrack)</option>
            <option value="branch_and_bound">Branch and Bound Only</option>
            <option value="backtracking">Exact Backtracking Only</option>
          </select>

          <button
            onClick={() => solveTSP()}
            disabled={solving}
            className="text-xs font-semibold bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg shadow-sm transition flex items-center space-x-1.5 disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 fill-current ${solving ? 'animate-spin' : ''}`} />
            <span>{solving ? 'Searching Tour...' : 'Solve Tour'}</span>
          </button>
        </div>
      </div>

      {/* Decision Engine Explanation */}
      <ExplanationCard explanation={explanation} />

      {/* Scalability Warning Card */}
      <div className="bg-purple-950 text-white rounded-2xl p-5 shadow-sm border border-purple-900 flex items-start space-x-3.5">
        <ShieldAlert className="w-5 h-5 text-purple-400 flex-shrink-0 mt-0.5" />
        <div className="space-y-1 text-xs">
          <div className="flex items-center space-x-2">
            <span className="font-bold text-purple-200 uppercase tracking-wider">
              Computational Complexity Classification:
            </span>
            <span className="bg-purple-800 text-purple-200 text-[10px] font-mono px-2 py-0.5 rounded">
              NP-Hard Optimization • NP-Complete Decision
            </span>
          </div>
          <p className="text-slate-300 leading-relaxed">
            The decision problem ("Does there exist a tour of cost ≤ k?") is NP-Complete, and finding the exact minimum is NP-Hard.
            The permutation space grows as <strong>(n - 1)! / 2</strong>. For 5 sites: 12 permutations; for 10 sites: 181,440; for 15 sites: 43.5 billion!
            Branch & bound prunes non-optimal search subtrees early using admissible lower bounds, but worst-case time remains exponential.
          </p>
        </div>
      </div>

      {/* Main Layout Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Interactive Graph with Active Tour Highlight */}
        <div className="lg:col-span-2 space-y-4">
          <NetworkGraph
            vertices={vertices}
            edges={edges}
            highlightPath={activeTour}
            height={440}
          />

          {/* Location Selection Chips */}
          <div className="bg-white border border-slate-200/80 rounded-xl p-4 shadow-sm space-y-2">
            <span className="text-xs font-bold text-slate-700 uppercase tracking-wider block">
              Required Maintenance Inspection Sites ({selectedLocations.length} selected):
            </span>
            <div className="flex flex-wrap gap-2">
              {vertices.map((v) => {
                const isSelected = selectedLocations.includes(v.id);
                const isStart = startLocation === v.id;
                return (
                  <button
                    key={v.id}
                    onClick={() => toggleLocation(v.id)}
                    className={`text-xs px-3 py-1.5 rounded-lg border font-medium transition flex items-center space-x-1.5 ${
                      isSelected
                        ? isStart
                          ? 'bg-purple-600 text-white border-purple-700 shadow-sm'
                          : 'bg-purple-50 text-purple-800 border-purple-200'
                        : 'bg-slate-50 text-slate-500 border-slate-200 hover:bg-slate-100'
                    }`}
                  >
                    <MapPin className="w-3 h-3" />
                    <span>{v.label}</span>
                    {isStart && <span className="text-[10px] bg-purple-800 text-purple-200 px-1 rounded">START</span>}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Right Col: Solver Results & Pruning Metrics */}
        <div className="space-y-4">
          {/* Starting Depot Selector */}
          <div className="bg-white border border-slate-200/80 rounded-xl p-4 shadow-sm text-xs space-y-2">
            <label className="block font-bold text-slate-700 uppercase tracking-wider">
              Starting Depot Site (Origin & Return):
            </label>
            <select
              value={startLocation}
              onChange={(e) => {
                setStartLocation(e.target.value);
                solveTSP(selectedLocations, e.target.value);
              }}
              className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 font-semibold"
            >
              {selectedLocations.map(loc => (
                <option key={loc} value={loc}>Start at {loc}</option>
              ))}
            </select>
          </div>

          {/* Optimal Tour Metric Card */}
          <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm space-y-3.5">
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Optimal Tour Solution
            </h3>

            {branchAndBoundResult || backtrackingResult ? (
              <div className="space-y-3 text-xs">
                <div className="flex justify-between items-center pb-2.5 border-b border-slate-100">
                  <span className="text-slate-500">Minimum Tour Distance/Cost:</span>
                  <span className="text-xl font-extrabold font-mono text-purple-700">
                    {(branchAndBoundResult?.total_tour_cost || backtrackingResult?.total_tour_cost)?.toFixed(2)} units
                  </span>
                </div>

                <div className="space-y-1.5 pb-2.5 border-b border-slate-100">
                  <span className="text-slate-500 font-semibold block">Sequential Visiting Order:</span>
                  <div className="flex flex-wrap items-center gap-1.5 font-mono text-[11px]">
                    {activeTour.map((node, idx) => (
                      <React.Fragment key={idx}>
                        <span className="bg-purple-50 text-purple-900 border border-purple-200 px-2 py-0.5 rounded font-bold">
                          {node}
                        </span>
                        {idx < activeTour.length - 1 && (
                          <span className="text-purple-600 font-bold">→</span>
                        )}
                      </React.Fragment>
                    ))}
                  </div>
                </div>

                {/* Search Tree Explored vs Pruned Metrics */}
                <div className="space-y-2 font-mono text-[11px]">
                  <div className="flex justify-between p-2 bg-slate-50 rounded">
                    <span className="text-slate-600 font-sans">B&B States Explored:</span>
                    <span className="font-bold text-slate-900">{branchAndBoundResult?.states_explored ?? 'N/A'}</span>
                  </div>
                  <div className="flex justify-between p-2 bg-emerald-50 rounded border border-emerald-100">
                    <span className="text-emerald-800 font-sans font-semibold">B&B Subtrees Pruned:</span>
                    <span className="font-bold text-emerald-800">{branchAndBoundResult?.states_pruned ?? 'N/A'}</span>
                  </div>
                  <div className="flex justify-between p-2 bg-slate-50 rounded">
                    <span className="text-slate-600 font-sans">Backtracking States Explored:</span>
                    <span className="font-bold text-slate-900">{backtrackingResult?.states_explored ?? 'N/A'}</span>
                  </div>
                  <div className="flex justify-between p-2 bg-slate-50 rounded">
                    <span className="text-slate-600 font-sans">B&B Wall-Clock Runtime:</span>
                    <span className="font-bold text-purple-700">{branchAndBoundResult?.execution_time_ms.toFixed(3)} ms</span>
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-xs text-slate-400">Click Solve Tour to calculate exact Hamiltonian cycle.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
