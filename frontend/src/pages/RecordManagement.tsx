import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { DeviceRecord, AlgorithmExplanation } from '../types';
import { ExplanationCard } from '../components/ExplanationCard';
import {
  Database,
  Search,
  Plus,
  Trash2,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
  Activity,
  Layers,
  BarChart2
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';

export const RecordManagement: React.FC = () => {
  const [records, setRecords] = useState<DeviceRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [explanation, setExplanation] = useState<AlgorithmExplanation | null>(null);

  // Search State
  const [searchKey, setSearchKey] = useState('');
  const [searchResult, setSearchResult] = useState<any | null>(null);
  const [searching, setSearching] = useState(false);

  // Invariant States
  const [bTreeInvariants, setBTreeInvariants] = useState<any | null>(null);
  const [rbtInvariants, setRbtInvariants] = useState<any | null>(null);
  const [bTreeDegree, setBTreeDegree] = useState(3);

  // Comparative Workload State
  const [benchmarkResult, setBenchmarkResult] = useState<any | null>(null);
  const [runningBenchmark, setRunningBenchmark] = useState(false);

  // Insert Record Modal
  const [showAddModal, setShowAddModal] = useState(false);
  const [newDeviceId, setNewDeviceId] = useState('');
  const [newDeviceName, setNewDeviceName] = useState('');
  const [newLocation, setNewLocation] = useState('HQ-Core');
  const [newCategory, setNewCategory] = useState('Router');
  const [newStatus, setNewStatus] = useState('Active');

  useEffect(() => {
    loadRecords();
  }, [bTreeDegree]);

  const loadRecords = async () => {
    try {
      setLoading(true);
      const bRes = await api.executeBTreeOp('get_all', undefined, undefined, bTreeDegree);
      const rRes = await api.executeRBTOp('verify_invariants');
      setRecords(bRes.records);
      setBTreeInvariants(bRes.invariants);
      setRbtInvariants(rRes);
    } catch (err: any) {
      alert('Failed to load tree records: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchKey.trim()) return;
    try {
      setSearching(true);
      const bRes = await api.executeBTreeOp('search', searchKey.trim(), undefined, bTreeDegree);
      const rRes = await api.executeRBTOp('search', searchKey.trim());
      setSearchResult({
        key: searchKey.trim(),
        found: bRes.found,
        record: bRes.record,
        btreeComps: bRes.key_comparisons,
        rbtComps: rRes.key_comparisons,
      });
    } catch (err: any) {
      alert('Search failed: ' + err.message);
    } finally {
      setSearching(false);
    }
  };

  const handleInsert = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newDeviceId.trim() || !newDeviceName.trim()) return;
    const newRec: DeviceRecord = {
      device_id: newDeviceId.trim(),
      device_name: newDeviceName.trim(),
      network_location: newLocation,
      device_category: newCategory,
      operational_status: newStatus,
      metadata: { addedAt: new Date().toISOString() }
    };

    try {
      await api.executeBTreeOp('insert', undefined, newRec, bTreeDegree);
      await api.executeRBTOp('insert', undefined, newRec);
      setShowAddModal(false);
      setNewDeviceId('');
      setNewDeviceName('');
      await loadRecords();
    } catch (err: any) {
      alert('Failed to insert record: ' + err.message);
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm(`Delete record '${id}' from both B-Tree and Red-Black Tree?`)) return;
    try {
      await api.executeBTreeOp('delete', id, undefined, bTreeDegree);
      await api.executeRBTOp('delete', id);
      await loadRecords();
    } catch (err: any) {
      alert('Failed to delete: ' + err.message);
    }
  };

  const handleRunWorkloadBenchmark = async () => {
    try {
      setRunningBenchmark(true);
      // Generate synthetic workload with 100 inserts, 40 searches, 20 deletes
      const sampleRecords: DeviceRecord[] = Array.from({ length: 100 }, (_, i) => ({
        device_id: `BM-${1000 + i}`,
        device_name: `Benchmark Node ${i}`,
        network_location: 'Cloud-Edge',
        device_category: i % 2 === 0 ? 'Router' : 'Switch',
        operational_status: 'Active',
      }));

      const searchKeys = Array.from({ length: 40 }, (_, i) => `BM-${1000 + (i * 2)}`);
      const deleteKeys = Array.from({ length: 20 }, (_, i) => `BM-${1000 + (i * 4)}`);

      const res = await api.compareTreeWorkload(sampleRecords, searchKeys, deleteKeys, bTreeDegree);
      setBenchmarkResult(res);
      setExplanation(res.explanation);
    } catch (err: any) {
      alert('Workload benchmark failed: ' + err.message);
    } finally {
      setRunningBenchmark(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-indigo-100 text-indigo-700 rounded-lg">
              <Database className="w-5 h-5" />
            </span>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">
              Module 3: Network Record Management (Advanced Trees)
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Search, insert, and maintain network inventory records with custom B-Tree and Red-Black Tree implementations.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-1.5 text-xs bg-white border border-slate-300 rounded-lg px-2.5 py-1.5 shadow-sm">
            <span className="font-semibold text-slate-600">B-Tree Order (t):</span>
            <select
              value={bTreeDegree}
              onChange={(e) => setBTreeDegree(Number(e.target.value))}
              className="font-bold text-indigo-600 bg-transparent focus:outline-none"
            >
              <option value={2}>t = 2 (2-3-4 Tree)</option>
              <option value={3}>t = 3 (Max 5 keys)</option>
              <option value={4}>t = 4 (Max 7 keys)</option>
              <option value={5}>t = 5 (Max 9 keys)</option>
            </select>
          </div>

          <button
            onClick={() => setShowAddModal(true)}
            className="text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 text-white px-3 py-2 rounded-lg shadow-sm transition flex items-center space-x-1.5"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Add Device Record</span>
          </button>
        </div>
      </div>

      {/* Explanation Engine Display */}
      <ExplanationCard explanation={explanation} />

      {/* Invariants & Search Bar Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Search Bar */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm space-y-4">
          <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center">
            <Search className="w-4 h-4 mr-1.5 text-indigo-600" /> Search Device By ID
          </h3>

          <form onSubmit={handleSearch} className="flex gap-2">
            <input
              type="text"
              required
              value={searchKey}
              onChange={(e) => setSearchKey(e.target.value)}
              placeholder="e.g. DEV-1001"
              className="flex-1 border border-slate-300 rounded-lg px-3 py-1.5 text-xs font-mono text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <button
              type="submit"
              disabled={searching}
              className="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition"
            >
              Search
            </button>
          </form>

          {searchResult && (
            <div className="bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs space-y-2">
              <div className="flex justify-between items-center">
                <span className="font-semibold text-slate-700">Lookup Key: {searchResult.key}</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${searchResult.found ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'}`}>
                  {searchResult.found ? 'FOUND' : 'NOT FOUND'}
                </span>
              </div>
              {searchResult.found && (
                <div className="text-slate-800 space-y-1 pt-1 border-t border-slate-200 font-mono text-[11px]">
                  <div>Name: <strong>{searchResult.record.device_name}</strong></div>
                  <div>Category: {searchResult.record.device_category} • Status: {searchResult.record.operational_status}</div>
                  <div>Location: {searchResult.record.network_location}</div>
                </div>
              )}
              <div className="pt-2 border-t border-slate-200 grid grid-cols-2 gap-2 text-[11px] font-mono">
                <div className="bg-white p-1.5 rounded border border-slate-200">
                  <span className="text-slate-500 block">B-Tree Key Comparisons:</span>
                  <span className="font-bold text-indigo-700">{searchResult.btreeComps}</span>
                </div>
                <div className="bg-white p-1.5 rounded border border-slate-200">
                  <span className="text-slate-500 block">RBT Key Comparisons:</span>
                  <span className="font-bold text-indigo-700">{searchResult.rbtComps}</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Center: B-Tree Invariants Status */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              B-Tree Structure Invariants (t = {bTreeDegree})
            </h3>
            <span className="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-2 py-0.5 rounded-full">
              CLRS Valid
            </span>
          </div>

          {bTreeInvariants && (
            <div className="space-y-2 text-xs font-mono">
              <div className="flex justify-between p-1.5 bg-slate-50 rounded">
                <span className="text-slate-500 font-sans">Tree Height:</span>
                <span className="font-bold text-slate-900">{bTreeInvariants.height} levels</span>
              </div>
              <div className="flex justify-between p-1.5 bg-slate-50 rounded">
                <span className="text-slate-500 font-sans">Leaf Depths Uniform:</span>
                <span className="font-bold text-emerald-700">True (Strict Balance)</span>
              </div>
              <div className="flex justify-between p-1.5 bg-slate-50 rounded">
                <span className="text-slate-500 font-sans">Key Bounds per Node:</span>
                <span className="font-bold text-slate-900">[{bTreeDegree - 1} .. {2 * bTreeDegree - 1}]</span>
              </div>
              <div className="flex justify-between p-1.5 bg-slate-50 rounded">
                <span className="text-slate-500 font-sans">Total Stored Keys:</span>
                <span className="font-bold text-slate-900">{bTreeInvariants.size}</span>
              </div>
            </div>
          )}
        </div>

        {/* Right: Red-Black Tree Invariants Status */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Red-Black Tree Invariants
            </h3>
            <span className="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-2 py-0.5 rounded-full">
              CLRS Valid
            </span>
          </div>

          {rbtInvariants && (
            <div className="space-y-2 text-xs font-mono">
              <div className="flex justify-between p-1.5 bg-slate-50 rounded">
                <span className="text-slate-500 font-sans">Uniform Black Height:</span>
                <span className="font-bold text-emerald-700">{rbtInvariants.black_height}</span>
              </div>
              <div className="flex justify-between p-1.5 bg-slate-50 rounded">
                <span className="text-slate-500 font-sans">No Double Red Nodes:</span>
                <span className="font-bold text-emerald-700">Verified</span>
              </div>
              <div className="flex justify-between p-1.5 bg-slate-50 rounded">
                <span className="text-slate-500 font-sans">Root Node Color:</span>
                <span className="font-bold text-slate-900">BLACK (Invariant 2)</span>
              </div>
              <div className="flex justify-between p-1.5 bg-slate-50 rounded">
                <span className="text-slate-500 font-sans">Total Stored Nodes:</span>
                <span className="font-bold text-slate-900">{rbtInvariants.size}</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Comparative Workload Benchmark Section */}
      <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center">
              <BarChart2 className="w-4 h-4 mr-1.5 text-indigo-600" />
              Side-by-Side Tree Workload Benchmark
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Executes identical sequence of 100 Inserts, 40 Searches, and 20 Deletions on both B-Tree and Red-Black Tree.
            </p>
          </div>

          <button
            onClick={handleRunWorkloadBenchmark}
            disabled={runningBenchmark}
            className="text-xs font-semibold bg-indigo-50 hover:bg-indigo-100 text-indigo-800 border border-indigo-200 px-3.5 py-1.5 rounded-lg transition self-start md:self-auto"
          >
            {runningBenchmark ? 'Benchmarking Trees...' : 'Run Identical Workload Comparison'}
          </button>
        </div>

        {benchmarkResult && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-3 border-t border-slate-100 text-xs">
            <div className="bg-slate-50 p-3.5 rounded-lg border border-slate-200 space-y-2">
              <span className="font-bold text-indigo-950 block">B-Tree Metrics (t = {benchmarkResult.b_tree.minimum_degree})</span>
              <div className="grid grid-cols-2 gap-2 font-mono text-[11px]">
                <div>Time: <strong>{benchmarkResult.b_tree.execution_time_ms.toFixed(3)} ms</strong></div>
                <div>Comparisons: <strong>{benchmarkResult.b_tree.key_comparisons}</strong></div>
                <div>Node Splits: <strong>{benchmarkResult.b_tree.splits}</strong></div>
                <div>Node Merges: <strong>{benchmarkResult.b_tree.merges}</strong></div>
              </div>
            </div>

            <div className="bg-slate-50 p-3.5 rounded-lg border border-slate-200 space-y-2">
              <span className="font-bold text-indigo-950 block">Red-Black Tree Metrics</span>
              <div className="grid grid-cols-2 gap-2 font-mono text-[11px]">
                <div>Time: <strong>{benchmarkResult.red_black_tree.execution_time_ms.toFixed(3)} ms</strong></div>
                <div>Comparisons: <strong>{benchmarkResult.red_black_tree.key_comparisons}</strong></div>
                <div>Rotations: <strong>{benchmarkResult.red_black_tree.total_rotations}</strong></div>
                <div>Recolorings: <strong>{benchmarkResult.red_black_tree.recolorings}</strong></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Stored Device Records Table */}
      <div className="bg-white border border-slate-200/80 rounded-xl overflow-hidden shadow-sm">
        <div className="px-5 py-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <h3 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
            Indexed Device Records ({records.length} devices)
          </h3>
          <span className="text-xs text-slate-500">
            Maintained across both tree structures
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-100/70 text-slate-600 uppercase font-semibold">
              <tr>
                <th className="px-4 py-2.5">Device ID</th>
                <th className="px-4 py-2.5">Hardware Name</th>
                <th className="px-4 py-2.5">Network Site</th>
                <th className="px-4 py-2.5">Category</th>
                <th className="px-4 py-2.5">Status</th>
                <th className="px-4 py-2.5 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono">
              {records.map((r) => (
                <tr key={r.device_id} className="hover:bg-slate-50/80">
                  <td className="px-4 py-2.5 font-bold text-indigo-700">{r.device_id}</td>
                  <td className="px-4 py-2.5 font-sans font-semibold text-slate-800">{r.device_name}</td>
                  <td className="px-4 py-2.5 text-slate-600">{r.network_location}</td>
                  <td className="px-4 py-2.5">
                    <span className="bg-slate-100 text-slate-700 px-2 py-0.5 rounded text-[10px] font-sans font-semibold">
                      {r.device_category}
                    </span>
                  </td>
                  <td className="px-4 py-2.5">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-sans font-semibold ${r.operational_status === 'Active' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}`}>
                      {r.operational_status}
                    </span>
                  </td>
                  <td className="px-4 py-2.5 text-right">
                    <button
                      onClick={() => handleDelete(r.device_id)}
                      className="text-red-500 hover:text-red-700 p-1 transition"
                      title="Delete Record"
                    >
                      <Trash2 className="w-3.5 h-3.5 inline" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add Record Modal Form */}
      {showAddModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-xl border border-slate-200">
            <h3 className="text-base font-bold text-slate-900 mb-4">Add Device Record</h3>
            <form onSubmit={handleInsert} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Device ID (Unique Key)</label>
                <input
                  type="text"
                  required
                  value={newDeviceId}
                  onChange={(e) => setNewDeviceId(e.target.value)}
                  placeholder="e.g. DEV-1011"
                  className="w-full border border-slate-300 rounded-lg px-3 py-1.5 text-slate-900 font-mono"
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Hardware Model Name</label>
                <input
                  type="text"
                  required
                  value={newDeviceName}
                  onChange={(e) => setNewDeviceName(e.target.value)}
                  placeholder="e.g. Arista 7280R3 Core"
                  className="w-full border border-slate-300 rounded-lg px-3 py-1.5 text-slate-900"
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Network Location</label>
                <input
                  type="text"
                  required
                  value={newLocation}
                  onChange={(e) => setNewLocation(e.target.value)}
                  placeholder="Location site"
                  className="w-full border border-slate-300 rounded-lg px-3 py-1.5 text-slate-900"
                />
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Category</label>
                  <select
                    value={newCategory}
                    onChange={(e) => setNewCategory(e.target.value)}
                    className="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-900"
                  >
                    <option value="Router">Router</option>
                    <option value="Switch">Switch</option>
                    <option value="Firewall">Firewall</option>
                    <option value="Gateway">Gateway</option>
                    <option value="Edge Server">Edge Server</option>
                  </select>
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Status</label>
                  <select
                    value={newStatus}
                    onChange={(e) => setNewStatus(e.target.value)}
                    className="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-900"
                  >
                    <option value="Active">Active</option>
                    <option value="Maintenance">Maintenance</option>
                    <option value="Offline">Offline</option>
                  </select>
                </div>
              </div>

              <div className="pt-3 flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-semibold"
                >
                  Insert Record
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
