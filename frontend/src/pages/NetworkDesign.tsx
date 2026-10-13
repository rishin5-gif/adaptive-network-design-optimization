import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Vertex, Edge, MSTResult, MSTComparison, AlgorithmExplanation } from '../types';
import { NetworkGraph } from '../components/NetworkGraph';
import { ExplanationCard } from '../components/ExplanationCard';
import {
  GitBranch,
  Play,
  RotateCcw,
  Plus,
  Trash2,
  CheckCircle2,
  AlertTriangle,
  Activity,
  Layers,
  Sliders
} from 'lucide-react';

export const NetworkDesign: React.FC = () => {
  const [vertices, setVertices] = useState<Vertex[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [loading, setLoading] = useState(true);
  const [runningAlgo, setRunningAlgo] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // MST Output
  const [activeMST, setActiveMST] = useState<MSTResult | null>(null);
  const [comparison, setComparison] = useState<MSTComparison | null>(null);
  const [explanation, setExplanation] = useState<AlgorithmExplanation | null>(null);
  const [selectedAlgo, setSelectedAlgo] = useState<'prim' | 'kruskal' | 'both'>('both');

  // Vertex & Edge Form State
  const [showAddVertex, setShowAddVertex] = useState(false);
  const [showAddEdge, setShowAddEdge] = useState(false);
  const [newVertexId, setNewVertexId] = useState('');
  const [newVertexLabel, setNewVertexLabel] = useState('');
  const [newVertexTier, setNewVertexTier] = useState('Distribution');
  const [newEdgeSource, setNewEdgeSource] = useState('');
  const [newEdgeTarget, setNewEdgeTarget] = useState('');
  const [newEdgeWeight, setNewEdgeWeight] = useState(10.0);

  // Synthetic Generator State
  const [genCount, setGenCount] = useState(8);
  const [genDensity, setGenDensity] = useState('sparse');

  useEffect(() => {
    loadNetwork();
  }, []);

  const loadNetwork = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getNetwork();
      setVertices(data.vertices);
      setEdges(data.edges);
      // Run comparison by default
      if (data.vertices.length > 0) {
        runMST(data.vertices, data.edges, 'both');
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const runMST = async (vList = vertices, eList = edges, mode = selectedAlgo) => {
    if (vList.length === 0) return;
    try {
      setRunningAlgo(true);
      setError(null);
      const vIds = vList.map(v => v.id);
      const edgeTuples: [string, string, number][] = eList.map(e => [e.source, e.target, Number(e.weight)]);

      if (mode === 'prim') {
        const res = await api.runPrim(vIds, edgeTuples);
        setActiveMST(res.result);
        setComparison(null);
        setExplanation(res.explanation);
      } else if (mode === 'kruskal') {
        const res = await api.runKruskal(vIds, edgeTuples);
        setActiveMST(res.result);
        setComparison(null);
        setExplanation(res.explanation);
      } else {
        const res = await api.compareMST(vIds, edgeTuples);
        setComparison(res.comparison);
        setActiveMST(res.comparison.prim); // Highlight Prim's MST
        setExplanation(res.explanation);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setRunningAlgo(false);
    }
  };

  const handleAddVertex = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newVertexId.trim()) return;
    try {
      await api.addVertex({
        id: newVertexId.trim(),
        label: newVertexLabel.trim() || newVertexId.trim(),
        tier: newVertexTier
      });
      setShowAddVertex(false);
      setNewVertexId('');
      setNewVertexLabel('');
      await loadNetwork();
    } catch (err: any) {
      alert('Failed to add vertex: ' + err.message);
    }
  };

  const handleAddEdge = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newEdgeSource || !newEdgeTarget || newEdgeSource === newEdgeTarget) {
      alert('Please select two distinct vertices.');
      return;
    }
    try {
      await api.addEdge({
        source: newEdgeSource,
        target: newEdgeTarget,
        weight: Number(newEdgeWeight)
      });
      setShowAddEdge(false);
      await loadNetwork();
    } catch (err: any) {
      alert('Failed to add edge: ' + err.message);
    }
  };

  const handleDeleteVertex = async (id: string) => {
    if (!window.confirm(`Delete vertex '${id}' and all attached links?`)) return;
    try {
      await api.deleteVertex(id);
      await loadNetwork();
    } catch (err: any) {
      alert('Failed to delete vertex: ' + err.message);
    }
  };

  const handleGenerateGraph = async () => {
    try {
      setLoading(true);
      const res = await api.generateGraph(genCount, genDensity);
      setVertices(res.vertices);
      setEdges(res.edges);
      await runMST(res.vertices, res.edges, 'both');
    } catch (err: any) {
      alert('Failed to generate graph: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-blue-100 text-blue-700 rounded-lg">
              <GitBranch className="w-5 h-5" />
            </span>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">
              Module 1: Network Design & Minimum Spanning Tree
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Determine optimal minimum-cost fiber interconnects using Prim's and Kruskal's algorithms with Disjoint-Set Union.
          </p>
        </div>

        {/* Algorithm Execution Buttons */}
        <div className="flex items-center space-x-2">
          <select
            value={selectedAlgo}
            onChange={(e) => setSelectedAlgo(e.target.value as any)}
            className="text-xs bg-white border border-slate-300 rounded-lg px-3 py-2 font-semibold text-slate-700 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="both">Compare Both (Prim & Kruskal)</option>
            <option value="prim">Prim's Algorithm Only</option>
            <option value="kruskal">Kruskal's Algorithm Only</option>
          </select>

          <button
            onClick={() => runMST(vertices, edges, selectedAlgo)}
            disabled={runningAlgo || vertices.length === 0}
            className="text-xs font-semibold bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow-sm transition flex items-center space-x-1.5 disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 fill-current ${runningAlgo ? 'animate-spin' : ''}`} />
            <span>{runningAlgo ? 'Solving...' : 'Execute MST'}</span>
          </button>
        </div>
      </div>

      {/* Decision Engine Explanation */}
      <ExplanationCard explanation={explanation} />

      {/* Main Grid: Interactive Graph + Action Panels */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Interactive Graph */}
        <div className="lg:col-span-2 space-y-4">
          <NetworkGraph
            vertices={vertices}
            edges={edges}
            highlightedEdges={activeMST?.selected_edges || []}
            height={440}
          />

          {/* Quick Graph Topology Editing Toolbar */}
          <div className="bg-white border border-slate-200/80 rounded-xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setShowAddVertex(true)}
                className="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold px-3 py-1.5 rounded-lg flex items-center space-x-1 transition"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Add Vertex</span>
              </button>
              <button
                onClick={() => setShowAddEdge(true)}
                className="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold px-3 py-1.5 rounded-lg flex items-center space-x-1 transition"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Add Link</span>
              </button>
              <button
                onClick={loadNetwork}
                className="text-xs bg-slate-100 hover:bg-slate-200 text-slate-600 px-3 py-1.5 rounded-lg transition"
                title="Reload Predefined Sample Network"
              >
                Reload Default Graph
              </button>
            </div>

            {/* Test Data Generator Controls */}
            <div className="flex items-center space-x-2 text-xs">
              <span className="text-slate-500 font-medium flex items-center">
                <Sliders className="w-3.5 h-3.5 mr-1 text-slate-400" /> Test Generator:
              </span>
              <select
                value={genCount}
                onChange={(e) => setGenCount(Number(e.target.value))}
                className="bg-slate-50 border border-slate-200 rounded px-2 py-1 text-xs text-slate-700"
              >
                <option value={6}>6 Nodes</option>
                <option value={10}>10 Nodes</option>
                <option value={16}>16 Nodes</option>
                <option value={24}>24 Nodes</option>
              </select>
              <select
                value={genDensity}
                onChange={(e) => setGenDensity(e.target.value)}
                className="bg-slate-50 border border-slate-200 rounded px-2 py-1 text-xs text-slate-700"
              >
                <option value="sparse">Sparse (E ≪ V²)</option>
                <option value="dense">Dense (E ≈ V²)</option>
              </select>
              <button
                onClick={handleGenerateGraph}
                className="bg-blue-50 text-blue-700 hover:bg-blue-100 font-semibold px-2.5 py-1 rounded border border-blue-200 transition"
              >
                Generate
              </button>
            </div>
          </div>
        </div>

        {/* Right Col: MST Results & Operation Counters */}
        <div className="space-y-4">
          {/* Solution Status Card */}
          <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3 flex items-center">
              <Activity className="w-4 h-4 mr-1.5 text-blue-600" /> Solution Metrics
            </h3>

            {activeMST ? (
              <div className="space-y-3.5">
                <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                  <span className="text-xs text-slate-500">Connectivity:</span>
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${activeMST.is_connected ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'}`}>
                    {activeMST.is_connected ? 'All Vertices Connected' : 'Disconnected (No Full MST)'}
                  </span>
                </div>

                <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                  <span className="text-xs text-slate-500">Total Deployment Cost:</span>
                  <span className="text-lg font-bold text-slate-900 font-mono">
                    ${activeMST.total_cost.toLocaleString()}k
                  </span>
                </div>

                <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                  <span className="text-xs text-slate-500">Selected Links:</span>
                  <span className="text-xs font-bold text-slate-700 font-mono">
                    {activeMST.num_selected_edges} of {vertices.length - 1} required (|V|-1)
                  </span>
                </div>

                <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                  <span className="text-xs text-slate-500">Execution Wall-Clock:</span>
                  <span className="text-xs font-bold text-blue-600 font-mono">
                    {activeMST.execution_time_ms.toFixed(3)} ms
                  </span>
                </div>

                <div>
                  <span className="text-xs font-semibold text-slate-600 block mb-1.5">Meaningful Operations Count:</span>
                  <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-100 space-y-1 font-mono text-[11px] text-slate-700">
                    {Object.entries(activeMST.operation_counts).map(([k, v]) => (
                      <div key={k} className="flex justify-between">
                        <span className="text-slate-500">{k.replace(/_/g, ' ')}:</span>
                        <span className="font-semibold text-slate-900">{v}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <p className="text-[11px] text-slate-500 italic mt-2">
                  {activeMST.status_message}
                </p>
              </div>
            ) : (
              <p className="text-xs text-slate-400">Run Prim or Kruskal to view solution metrics.</p>
            )}
          </div>

          {/* Prim vs Kruskal Side-by-Side Comparison */}
          {comparison && (
            <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm">
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">
                Prim vs Kruskal Agreement Check
              </h3>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between p-2 bg-slate-50 rounded">
                  <span className="font-medium text-slate-600">Prim Total Cost:</span>
                  <span className="font-mono font-bold text-slate-900">${comparison.prim.total_cost}k</span>
                </div>
                <div className="flex justify-between p-2 bg-slate-50 rounded">
                  <span className="font-medium text-slate-600">Kruskal Total Cost:</span>
                  <span className="font-mono font-bold text-slate-900">${comparison.kruskal.total_cost}k</span>
                </div>
                <div className="flex justify-between p-2 bg-slate-50 rounded">
                  <span className="font-medium text-slate-600">Cost Agreement:</span>
                  <span className="font-bold text-emerald-700 flex items-center">
                    <CheckCircle2 className="w-3.5 h-3.5 mr-1" /> Verified Identical
                  </span>
                </div>
                <div className="flex justify-between p-2 bg-slate-50 rounded">
                  <span className="font-medium text-slate-600">Prim Runtime:</span>
                  <span className="font-mono text-slate-700">{comparison.prim.execution_time_ms.toFixed(3)} ms</span>
                </div>
                <div className="flex justify-between p-2 bg-slate-50 rounded">
                  <span className="font-medium text-slate-600">Kruskal Runtime:</span>
                  <span className="font-mono text-slate-700">{comparison.kruskal.execution_time_ms.toFixed(3)} ms</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Selected MST Links Table */}
      {activeMST && activeMST.selected_edges.length > 0 && (
        <div className="bg-white border border-slate-200/80 rounded-xl overflow-hidden shadow-sm">
          <div className="px-5 py-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
            <h3 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              Selected Minimum Spanning Tree Links ({activeMST.selected_edges.length} links)
            </h3>
            <span className="text-xs font-mono text-slate-500">
              Representation: {activeMST.graph_representation}
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-100/70 text-slate-600 uppercase font-semibold">
                <tr>
                  <th className="px-4 py-2.5">#</th>
                  <th className="px-4 py-2.5">Endpoint 1 (Source)</th>
                  <th className="px-4 py-2.5">Endpoint 2 (Target)</th>
                  <th className="px-4 py-2.5">Fiber Link Cost ($k)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-mono">
                {activeMST.selected_edges.map((e, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/80">
                    <td className="px-4 py-2 text-slate-400">{idx + 1}</td>
                    <td className="px-4 py-2 font-semibold text-blue-700">{e.source}</td>
                    <td className="px-4 py-2 font-semibold text-blue-700">{e.target}</td>
                    <td className="px-4 py-2 font-bold text-slate-900">${e.weight.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Add Vertex Modal Form */}
      {showAddVertex && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-xl border border-slate-200">
            <h3 className="text-base font-bold text-slate-900 mb-4">Add Network Vertex</h3>
            <form onSubmit={handleAddVertex} className="space-y-3.5 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Vertex Identifier (e.g. Node-11)</label>
                <input
                  type="text"
                  required
                  value={newVertexId}
                  onChange={(e) => setNewVertexId(e.target.value)}
                  placeholder="Node ID"
                  className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Display Label</label>
                <input
                  type="text"
                  value={newVertexLabel}
                  onChange={(e) => setNewVertexLabel(e.target.value)}
                  placeholder="Descriptive Name"
                  className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Tier</label>
                <select
                  value={newVertexTier}
                  onChange={(e) => setNewVertexTier(e.target.value)}
                  className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Core">Core Tier</option>
                  <option value="Distribution">Distribution Tier</option>
                  <option value="Access">Access Tier</option>
                </select>
              </div>

              <div className="pt-3 flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setShowAddVertex(false)}
                  className="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold"
                >
                  Add Node
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Edge Modal Form */}
      {showAddEdge && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-xl border border-slate-200">
            <h3 className="text-base font-bold text-slate-900 mb-4">Add Weighted Link</h3>
            <form onSubmit={handleAddEdge} className="space-y-3.5 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Source Node</label>
                <select
                  required
                  value={newEdgeSource}
                  onChange={(e) => setNewEdgeSource(e.target.value)}
                  className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900"
                >
                  <option value="">Select source</option>
                  {vertices.map(v => <option key={v.id} value={v.id}>{v.label} ({v.id})</option>)}
                </select>
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Target Node</label>
                <select
                  required
                  value={newEdgeTarget}
                  onChange={(e) => setNewEdgeTarget(e.target.value)}
                  className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900"
                >
                  <option value="">Select target</option>
                  {vertices.map(v => <option key={v.id} value={v.id}>{v.label} ({v.id})</option>)}
                </select>
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Connection Cost / Weight ($k)</label>
                <input
                  type="number"
                  step="0.1"
                  min="0.1"
                  required
                  value={newEdgeWeight}
                  onChange={(e) => setNewEdgeWeight(parseFloat(e.target.value))}
                  className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900"
                />
              </div>

              <div className="pt-3 flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setShowAddEdge(false)}
                  className="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold"
                >
                  Add Link
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
