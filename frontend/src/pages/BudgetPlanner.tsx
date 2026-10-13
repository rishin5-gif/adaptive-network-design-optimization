import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { UpgradeProject, KnapsackResult, AlgorithmExplanation } from '../types';
import { ExplanationCard } from '../components/ExplanationCard';
import {
  DollarSign,
  Play,
  RotateCcw,
  Plus,
  Trash2,
  CheckCircle2,
  AlertTriangle,
  Info,
  Sliders,
  Layers
} from 'lucide-react';

export const BudgetPlanner: React.FC = () => {
  const [projects, setProjects] = useState<UpgradeProject[]>([]);
  const [budget, setBudget] = useState<number>(85000);
  const [loading, setLoading] = useState(true);
  const [solving, setSolving] = useState(false);

  // Results
  const [fractionalResult, setFractionalResult] = useState<KnapsackResult | null>(null);
  const [dpResult, setDpResult] = useState<KnapsackResult | null>(null);
  const [activeTab, setActiveTab] = useState<'both' | 'fractional' | '01'>('both');
  const [explanation, setExplanation] = useState<AlgorithmExplanation | null>(null);

  // New Project Form
  const [showAddModal, setShowAddModal] = useState(false);
  const [newProjectId, setNewProjectId] = useState('');
  const [newProjectName, setNewProjectName] = useState('');
  const [newCost, setNewCost] = useState<number>(25000);
  const [newBenefit, setNewBenefit] = useState<number>(60);
  const [newDivisibility, setNewDivisibility] = useState('indivisible');

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);
      // Load default sample projects via dashboard or hardcoded initial
      const sample = [
        { project_id: 'PRJ-01', project_name: 'Metro Core 400Gbps Optics Transceivers', cost: 45000, expected_benefit: 92, divisibility: 'indivisible' },
        { project_id: 'PRJ-02', project_name: 'Cloud Direct-Connect 100Gbps Cross-Connect', cost: 30000, expected_benefit: 75, divisibility: 'indivisible' },
        { project_id: 'PRJ-03', project_name: 'Zero-Trust Perimeter Firewall Cluster', cost: 25000, expected_benefit: 60, divisibility: 'indivisible' },
        { project_id: 'PRJ-04', project_name: 'Dedicated DWDM Leased Spectrum Slices', cost: 50000, expected_benefit: 110, divisibility: 'divisible' },
        { project_id: 'PRJ-05', project_name: 'Edge AI Inference Acceleration Blade', cost: 20000, expected_benefit: 42, divisibility: 'indivisible' },
        { project_id: 'PRJ-06', project_name: 'Burstable Tier-1 Bandwidth Pool', cost: 15000, expected_benefit: 38, divisibility: 'divisible' },
      ];
      setProjects(sample);
      await runOptimization(sample, 85000);
    } catch (err: any) {
      alert('Failed to load upgrade projects: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const runOptimization = async (pList = projects, bLimit = budget) => {
    try {
      setSolving(true);
      const fracRes = await api.runFractionalKnapsack(pList, bLimit);
      const dpRes = await api.run01Knapsack(pList, bLimit);
      setFractionalResult(fracRes.result);
      setDpResult(dpRes.result);
      setExplanation(dpRes.explanation);
    } catch (err: any) {
      alert('Knapsack optimization failed: ' + err.message);
    } finally {
      setSolving(false);
    }
  };

  const handleAddProject = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProjectId.trim() || !newProjectName.trim()) return;
    const p: UpgradeProject = {
      project_id: newProjectId.trim(),
      project_name: newProjectName.trim(),
      cost: Number(newCost),
      expected_benefit: Number(newBenefit),
      divisibility: newDivisibility
    };
    const updated = [...projects, p];
    setProjects(updated);
    setShowAddModal(false);
    setNewProjectId('');
    setNewProjectName('');
    runOptimization(updated, budget);
  };

  const handleDeleteProject = (id: string) => {
    const updated = projects.filter(p => p.project_id !== id);
    setProjects(updated);
    runOptimization(updated, budget);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-amber-100 text-amber-700 rounded-lg">
              <DollarSign className="w-5 h-5" />
            </span>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">
              Module 5: Network Upgrade Budget Planner (Knapsack)
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Optimize capital expenditure allocations using Fractional Knapsack (Greedy) and 0/1 Knapsack (Dynamic Programming).
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowAddModal(true)}
            className="text-xs font-semibold bg-amber-600 hover:bg-amber-700 text-white px-3.5 py-2 rounded-lg shadow-sm transition flex items-center space-x-1.5"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Add Candidate Project</span>
          </button>
        </div>
      </div>

      {/* Explanation Engine Display */}
      <ExplanationCard explanation={explanation} />

      {/* Budget Capacity Control Card */}
      <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <span className="text-xs font-bold text-slate-700 uppercase tracking-wider block">
              CapEx Budget Capacity Parameter
            </span>
            <p className="text-xs text-slate-500 mt-0.5">
              Adjust budget limit to evaluate optimal upgrade selections under financial resource constraints.
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <span className="text-xl font-extrabold font-mono text-slate-900">
              ${budget.toLocaleString()}
            </span>
            <button
              onClick={() => runOptimization(projects, budget)}
              disabled={solving}
              className="text-xs font-bold bg-amber-600 hover:bg-amber-700 text-white px-4 py-2 rounded-lg transition flex items-center space-x-1.5"
            >
              <Play className={`w-3 h-3 fill-current ${solving ? 'animate-spin' : ''}`} />
              <span>{solving ? 'Optimizing...' : 'Re-Run Solvers'}</span>
            </button>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <input
            type="range"
            min="10000"
            max="180000"
            step="5000"
            value={budget}
            onChange={(e) => {
              const val = Number(e.target.value);
              setBudget(val);
              runOptimization(projects, val);
            }}
            className="w-full accent-amber-600 cursor-pointer"
          />
        </div>
      </div>

      {/* Comparison Overview Cards */}
      {fractionalResult && dpResult && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Fractional Knapsack Card */}
          <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-teal-800 bg-teal-50 border border-teal-200 px-2.5 py-1 rounded-full uppercase tracking-wider">
                Fractional Knapsack (Divisible)
              </span>
              <span className="text-xs font-mono font-semibold text-slate-500">O(n log n) Greedy</span>
            </div>

            <div className="grid grid-cols-3 gap-2 pt-2 border-t border-slate-100 font-mono text-xs">
              <div className="bg-slate-50 p-2.5 rounded">
                <span className="text-slate-500 font-sans block text-[11px]">Total Benefit:</span>
                <span className="text-base font-bold text-teal-700">{fractionalResult.total_benefit_gained.toFixed(1)}</span>
              </div>
              <div className="bg-slate-50 p-2.5 rounded">
                <span className="text-slate-500 font-sans block text-[11px]">Budget Spent:</span>
                <span className="text-base font-bold text-slate-800">${fractionalResult.total_cost_spent.toLocaleString()}</span>
              </div>
              <div className="bg-slate-50 p-2.5 rounded">
                <span className="text-slate-500 font-sans block text-[11px]">Remaining:</span>
                <span className="text-base font-bold text-slate-600">${fractionalResult.remaining_budget.toLocaleString()}</span>
              </div>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed pt-1">
              {fractionalResult.selection_reason}
            </p>
          </div>

          {/* 0/1 Knapsack DP Card */}
          <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-amber-800 bg-amber-50 border border-amber-200 px-2.5 py-1 rounded-full uppercase tracking-wider">
                0/1 Knapsack (Indivisible Equipment)
              </span>
              <span className="text-xs font-mono font-semibold text-slate-500">O(nW) Dynamic Prog.</span>
            </div>

            <div className="grid grid-cols-3 gap-2 pt-2 border-t border-slate-100 font-mono text-xs">
              <div className="bg-slate-50 p-2.5 rounded">
                <span className="text-slate-500 font-sans block text-[11px]">Total Benefit:</span>
                <span className="text-base font-bold text-amber-700">{dpResult.total_benefit_gained.toFixed(1)}</span>
              </div>
              <div className="bg-slate-50 p-2.5 rounded">
                <span className="text-slate-500 font-sans block text-[11px]">Budget Spent:</span>
                <span className="text-base font-bold text-slate-800">${dpResult.total_cost_spent.toLocaleString()}</span>
              </div>
              <div className="bg-slate-50 p-2.5 rounded">
                <span className="text-slate-500 font-sans block text-[11px]">Remaining:</span>
                <span className="text-base font-bold text-slate-600">${dpResult.remaining_budget.toLocaleString()}</span>
              </div>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed pt-1">
              {dpResult.selection_reason}
            </p>
          </div>
        </div>
      )}

      {/* Greedy Failure Counterexample Callout */}
      {dpResult?.counterexample_note && (
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 text-xs text-blue-900 flex items-start space-x-3">
          <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <div>
            <strong className="text-blue-950 font-bold block mb-1">DAA Theoretical Foundation: Why Greedy Fails for 0/1 Knapsack</strong>
            <p className="leading-relaxed text-blue-800">{dpResult.counterexample_note}</p>
          </div>
        </div>
      )}

      {/* Selected Items & Allocations Table */}
      {dpResult && (
        <div className="bg-white border border-slate-200/80 rounded-xl overflow-hidden shadow-sm">
          <div className="px-5 py-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
            <h3 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              Allocated Projects in 0/1 Dynamic Programming Solution ({dpResult.allocations.length} projects selected)
            </h3>
            <span className="text-xs text-slate-500">
              Optimal Global Substructure Recovery
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-100/70 text-slate-600 uppercase font-semibold">
                <tr>
                  <th className="px-4 py-2.5">Project ID</th>
                  <th className="px-4 py-2.5">Upgrade Name</th>
                  <th className="px-4 py-2.5">Project Cost</th>
                  <th className="px-4 py-2.5">Benefit Score</th>
                  <th className="px-4 py-2.5">Benefit/Cost Ratio</th>
                  <th className="px-4 py-2.5">Allocated Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-mono">
                {dpResult.allocations.map((a) => (
                  <tr key={a.project_id} className="hover:bg-slate-50/80">
                    <td className="px-4 py-2.5 font-bold text-amber-700">{a.project_id}</td>
                    <td className="px-4 py-2.5 font-sans font-semibold text-slate-900">{a.project_name}</td>
                    <td className="px-4 py-2.5 text-slate-800">${a.allocated_cost.toLocaleString()}</td>
                    <td className="px-4 py-2.5 font-bold text-emerald-700">+{a.allocated_benefit.toFixed(1)}</td>
                    <td className="px-4 py-2.5 text-slate-600">{a.benefit_to_cost_ratio.toFixed(4)}</td>
                    <td className="px-4 py-2.5">
                      <span className="bg-emerald-100 text-emerald-800 text-[10px] font-sans font-bold px-2 py-0.5 rounded-full">
                        Fully Funded (100%)
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Candidate Projects Pool Table */}
      <div className="bg-white border border-slate-200/80 rounded-xl overflow-hidden shadow-sm">
        <div className="px-5 py-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <h3 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
            All Candidate Upgrade Projects Pool ({projects.length} candidate projects)
          </h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-100/70 text-slate-600 uppercase font-semibold">
              <tr>
                <th className="px-4 py-2.5">ID</th>
                <th className="px-4 py-2.5">Upgrade Description</th>
                <th className="px-4 py-2.5">Cost ($)</th>
                <th className="px-4 py-2.5">Benefit</th>
                <th className="px-4 py-2.5">Divisibility</th>
                <th className="px-4 py-2.5 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono">
              {projects.map((p) => (
                <tr key={p.project_id} className="hover:bg-slate-50/80">
                  <td className="px-4 py-2.5 font-bold text-slate-800">{p.project_id}</td>
                  <td className="px-4 py-2.5 font-sans font-semibold text-slate-900">{p.project_name}</td>
                  <td className="px-4 py-2.5 text-slate-800">${p.cost.toLocaleString()}</td>
                  <td className="px-4 py-2.5 font-bold text-slate-900">{p.expected_benefit}</td>
                  <td className="px-4 py-2.5">
                    <span className={`text-[10px] font-sans font-semibold px-2 py-0.5 rounded ${p.divisibility === 'divisible' ? 'bg-teal-100 text-teal-800' : 'bg-slate-100 text-slate-700'}`}>
                      {p.divisibility}
                    </span>
                  </td>
                  <td className="px-4 py-2.5 text-right">
                    <button
                      onClick={() => handleDeleteProject(p.project_id)}
                      className="text-red-500 hover:text-red-700 p-1 transition"
                      title="Delete Project"
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

      {/* Add Project Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-xl border border-slate-200">
            <h3 className="text-base font-bold text-slate-900 mb-4">Add Upgrade Project</h3>
            <form onSubmit={handleAddProject} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Project ID</label>
                <input
                  type="text"
                  required
                  value={newProjectId}
                  onChange={(e) => setNewProjectId(e.target.value)}
                  placeholder="e.g. PRJ-07"
                  className="w-full border border-slate-300 rounded-lg px-3 py-1.5 text-slate-900 font-mono"
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Project Title</label>
                <input
                  type="text"
                  required
                  value={newProjectName}
                  onChange={(e) => setNewProjectName(e.target.value)}
                  placeholder="e.g. Optical Transceiver Blade"
                  className="w-full border border-slate-300 rounded-lg px-3 py-1.5 text-slate-900"
                />
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Cost ($)</label>
                  <input
                    type="number"
                    min="100"
                    step="500"
                    required
                    value={newCost}
                    onChange={(e) => setNewCost(parseFloat(e.target.value))}
                    className="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-900 font-mono"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Benefit (Value)</label>
                  <input
                    type="number"
                    min="1"
                    step="1"
                    required
                    value={newBenefit}
                    onChange={(e) => setNewBenefit(parseFloat(e.target.value))}
                    className="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-900 font-mono"
                  />
                </div>
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Divisibility Resource Model</label>
                <select
                  value={newDivisibility}
                  onChange={(e) => setNewDivisibility(e.target.value)}
                  className="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-900"
                >
                  <option value="indivisible">Indivisible (Discrete Hardware / 0-1)</option>
                  <option value="divisible">Divisible (Bandwidth / Optical Spectrum)</option>
                </select>
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
                  className="px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg font-semibold"
                >
                  Add Project
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
