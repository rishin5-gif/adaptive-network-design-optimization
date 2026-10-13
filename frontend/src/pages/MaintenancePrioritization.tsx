import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { MaintenanceEvent, AlgorithmExplanation } from '../types';
import { ExplanationCard } from '../components/ExplanationCard';
import {
  ListOrdered,
  Plus,
  Play,
  ArrowDown,
  AlertCircle,
  Activity,
  Layers,
  CheckCircle2,
  Clock,
  Sparkles
} from 'lucide-react';

export const MaintenancePrioritization: React.FC = () => {
  const [events, setEvents] = useState<MaintenanceEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [explanation, setExplanation] = useState<AlgorithmExplanation | null>(null);

  // Next event to process
  const [nextEvent, setNextEvent] = useState<MaintenanceEvent | null>(null);
  const [extractedEvent, setExtractedEvent] = useState<MaintenanceEvent | null>(null);

  // Decrease Key Form
  const [selectedEventId, setSelectedEventId] = useState('');
  const [newPriorityVal, setNewPriorityVal] = useState(1);

  // Comparative Workload State
  const [benchmarkResult, setBenchmarkResult] = useState<any | null>(null);
  const [benchmarking, setBenchmarking] = useState(false);

  // New Event Modal
  const [showAddModal, setShowAddModal] = useState(false);
  const [newEventId, setNewEventId] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [newPriority, setNewPriority] = useState(3);
  const [newLocation, setNewLocation] = useState('HQ-Core');

  useEffect(() => {
    loadEvents();
  }, []);

  const loadEvents = async () => {
    try {
      setLoading(true);
      const bRes = await api.executeBinomialHeapOp('get_all');
      setEvents(bRes.events);
      if (bRes.events.length > 0) {
        const minRes = await api.executeFibHeapOp('find_min');
        setNextEvent(minRes.event);
        setSelectedEventId(bRes.events[0].event_id);
      }
    } catch (err: any) {
      alert('Failed to load heap events: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExtractMin = async () => {
    try {
      // Extract from both heaps to keep them synchronized
      const bExt = await api.executeBinomialHeapOp('extract_min');
      await api.executeFibHeapOp('extract_min');
      setExtractedEvent(bExt.extracted_event);
      await loadEvents();
    } catch (err: any) {
      alert('Extract min failed: ' + err.message);
    }
  };

  const handleDecreaseKey = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedEventId) return;
    try {
      await api.executeBinomialHeapOp('decrease_key', selectedEventId, Number(newPriorityVal));
      await api.executeFibHeapOp('decrease_key', selectedEventId, Number(newPriorityVal));
      alert(`Urgency escalated for '${selectedEventId}' to Priority ${newPriorityVal}.`);
      await loadEvents();
    } catch (err: any) {
      alert('Decrease key failed: ' + err.message);
    }
  };

  const handleInsertEvent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newEventId.trim() || !newDescription.trim()) return;
    const evt: MaintenanceEvent = {
      event_id: newEventId.trim(),
      description: newDescription.trim(),
      priority: Number(newPriority),
      network_location: newLocation,
      created_at: new Date().toISOString()
    };
    try {
      await api.executeBinomialHeapOp('insert', undefined, undefined, evt);
      await api.executeFibHeapOp('insert', undefined, undefined, evt);
      setShowAddModal(false);
      setNewEventId('');
      setNewDescription('');
      await loadEvents();
    } catch (err: any) {
      alert('Failed to insert event: ' + err.message);
    }
  };

  const handleRunHeapBenchmark = async () => {
    try {
      setBenchmarking(true);
      // Run identical priority sequence on both heaps
      const sampleEvents: MaintenanceEvent[] = Array.from({ length: 60 }, (_, i) => ({
        event_id: `BENCH-${i}`,
        description: `Synthetic Alert ${i}`,
        priority: 10 + (i % 50),
        network_location: 'East-DC',
      }));

      const decreases = [
        { event_id: 'BENCH-15', new_priority: 2 },
        { event_id: 'BENCH-35', new_priority: 1 },
        { event_id: 'BENCH-48', new_priority: 3 },
      ];

      const res = await api.compareHeapWorkload(sampleEvents, decreases, 10);
      setBenchmarkResult(res);
      setExplanation(res.explanation);
    } catch (err: any) {
      alert('Heap benchmark failed: ' + err.message);
    } finally {
      setBenchmarking(false);
    }
  };

  const getPriorityBadge = (p: number) => {
    if (p === 1) return { label: 'P1 - EMERGENCY', style: 'bg-red-100 text-red-800 border-red-300' };
    if (p === 2) return { label: 'P2 - CRITICAL', style: 'bg-orange-100 text-orange-800 border-orange-300' };
    if (p === 3) return { label: 'P3 - HIGH', style: 'bg-amber-100 text-amber-800 border-amber-300' };
    if (p === 4) return { label: 'P4 - MEDIUM', style: 'bg-blue-100 text-blue-800 border-blue-300' };
    return { label: `P${p} - ROUTINE`, style: 'bg-slate-100 text-slate-800 border-slate-300' };
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-emerald-100 text-emerald-700 rounded-lg">
              <ListOrdered className="w-5 h-5" />
            </span>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">
              Module 4: Maintenance Event Prioritization (Priority Heaps)
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Prioritize network outage tickets with Binomial and Fibonacci Heaps. Lower priority value = higher urgency.
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="text-xs font-semibold bg-emerald-600 hover:bg-emerald-700 text-white px-3.5 py-2 rounded-lg shadow-sm transition flex items-center space-x-1.5 self-start md:self-auto"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>Dispatch New Event Ticket</span>
        </button>
      </div>

      {/* Explanation Engine Display */}
      <ExplanationCard explanation={explanation} />

      {/* Next Urgent Event Hero Banner */}
      {nextEvent && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 text-white shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="space-y-2 max-w-2xl">
            <div className="flex items-center space-x-2">
              <span className="text-[10px] uppercase font-bold tracking-wider text-emerald-400 flex items-center">
                <Sparkles className="w-3.5 h-3.5 mr-1" /> Next Urgent Maintenance Task (Heap Find-Min)
              </span>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${getPriorityBadge(nextEvent.priority).style}`}>
                {getPriorityBadge(nextEvent.priority).label}
              </span>
            </div>
            <h3 className="text-base font-bold text-white">{nextEvent.description}</h3>
            <div className="text-xs text-slate-400 flex items-center space-x-4 font-mono">
              <span>Event ID: <strong>{nextEvent.event_id}</strong></span>
              <span>Site: {nextEvent.network_location}</span>
              <span>Priority Value: {nextEvent.priority}</span>
            </div>
          </div>

          <button
            onClick={handleExtractMin}
            className="text-xs font-bold bg-emerald-500 hover:bg-emerald-600 text-slate-950 px-4 py-2.5 rounded-xl shadow transition flex items-center space-x-1.5 flex-shrink-0"
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>Extract & Process Event</span>
          </button>
        </div>
      )}

      {/* Recently Extracted Notice */}
      {extractedEvent && (
        <div className="bg-emerald-50 border border-emerald-200 text-emerald-900 p-3.5 rounded-xl text-xs flex items-center justify-between">
          <span>
            <strong>Processed Event:</strong> {extractedEvent.event_id} ({extractedEvent.description}) extracted with Priority {extractedEvent.priority}.
          </span>
          <span className="text-[11px] text-emerald-700 font-mono">Heap Min Updated</span>
        </div>
      )}

      {/* Decrease Key & Comparative Benchmark Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Escalate Urgency (Decrease-Key) */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm space-y-4">
          <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center">
            <ArrowDown className="w-4 h-4 mr-1.5 text-emerald-600" />
            Escalate Priority (Decrease-Key Operation)
          </h3>
          <p className="text-xs text-slate-500">
            Escalates event urgency by decreasing its priority number. Fibonacci Heap accomplishes this in O(1) amortized via cascading cuts.
          </p>

          <form onSubmit={handleDecreaseKey} className="space-y-3 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Target Ticket:</label>
              <select
                value={selectedEventId}
                onChange={(e) => setSelectedEventId(e.target.value)}
                className="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-900"
              >
                {events.map(e => (
                  <option key={e.event_id} value={e.event_id}>
                    {e.event_id} - Priority {e.priority} ({e.description.substring(0, 45)}...)
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">New Escalate Priority Value (1=Max Emergency):</label>
              <input
                type="number"
                min="1"
                max="10"
                required
                value={newPriorityVal}
                onChange={(e) => setNewPriorityVal(parseInt(e.target.value))}
                className="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-900 font-mono"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-slate-900 hover:bg-slate-800 text-white font-semibold py-2 rounded-lg transition"
            >
              Decrease-Key & Rebalance Heaps
            </button>
          </form>
        </div>

        {/* Right: Heaps Comparative Benchmark */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Binomial vs Fibonacci Heap Benchmark
            </h3>
            <button
              onClick={handleRunHeapBenchmark}
              disabled={benchmarking}
              className="text-xs font-semibold bg-emerald-50 text-emerald-800 hover:bg-emerald-100 border border-emerald-200 px-3 py-1.5 rounded-lg transition"
            >
              {benchmarking ? 'Running Workload...' : 'Run Heap Comparison'}
            </button>
          </div>
          <p className="text-xs text-slate-500">
            Executes identical 60-event insertion, cascading decrease-key operations, and extract-min sequences.
          </p>

          {benchmarkResult ? (
            <div className="grid grid-cols-2 gap-3 text-xs pt-2 border-t border-slate-100 font-mono">
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 space-y-1">
                <span className="font-bold text-slate-900 font-sans block">Binomial Heap</span>
                <div>Time: <strong>{benchmarkResult.binomial_heap.execution_time_ms.toFixed(3)} ms</strong></div>
                <div>Tree Links: <strong>{benchmarkResult.binomial_heap.links_count}</strong></div>
                <div>Root Merges: <strong>{benchmarkResult.binomial_heap.merges_count}</strong></div>
              </div>

              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 space-y-1">
                <span className="font-bold text-slate-900 font-sans block">Fibonacci Heap</span>
                <div>Time: <strong>{benchmarkResult.fibonacci_heap.execution_time_ms.toFixed(3)} ms</strong></div>
                <div>Node Cuts: <strong>{benchmarkResult.fibonacci_heap.cuts_count}</strong></div>
                <div>Cascading Cuts: <strong>{benchmarkResult.fibonacci_heap.cascading_cuts_count}</strong></div>
              </div>
            </div>
          ) : (
            <div className="bg-slate-50 p-4 rounded-lg text-xs text-slate-400 text-center border border-slate-200/60">
              Run benchmark to view actual links and cascading cuts operation counts.
            </div>
          )}

          <div className="bg-slate-50 p-2.5 rounded text-[11px] text-slate-600 border border-slate-100">
            <strong>Theoretical Note:</strong> Fibonacci Heap maintains O(1) amortized decrease-key by delaying tree consolidation until Extract-Min, whereas Binomial Heap links trees during insertion in O(log n).
          </div>
        </div>
      </div>

      {/* Pending Events Queue Table */}
      <div className="bg-white border border-slate-200/80 rounded-xl overflow-hidden shadow-sm">
        <div className="px-5 py-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <h3 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
            Pending Maintenance Event Queue ({events.length} tickets)
          </h3>
          <span className="text-xs text-slate-500">
            Ordered by Urgency Priority (Ascending)
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-100/70 text-slate-600 uppercase font-semibold">
              <tr>
                <th className="px-4 py-2.5">Priority Urgency</th>
                <th className="px-4 py-2.5">Ticket ID</th>
                <th className="px-4 py-2.5">Site Location</th>
                <th className="px-4 py-2.5">Issue Description</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {events.map((e) => {
                const badge = getPriorityBadge(e.priority);
                return (
                  <tr key={e.event_id} className="hover:bg-slate-50/80">
                    <td className="px-4 py-2.5">
                      <span className={`px-2.5 py-0.5 rounded text-[10px] font-bold border ${badge.style}`}>
                        {badge.label}
                      </span>
                    </td>
                    <td className="px-4 py-2.5 font-mono font-bold text-slate-800">{e.event_id}</td>
                    <td className="px-4 py-2.5 font-semibold text-slate-700">{e.network_location}</td>
                    <td className="px-4 py-2.5 text-slate-600">{e.description}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add Event Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-xl border border-slate-200">
            <h3 className="text-base font-bold text-slate-900 mb-4">Dispatch Maintenance Ticket</h3>
            <form onSubmit={handleInsertEvent} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Event Ticket ID</label>
                <input
                  type="text"
                  required
                  value={newEventId}
                  onChange={(e) => setNewEventId(e.target.value)}
                  placeholder="e.g. EVT-307"
                  className="w-full border border-slate-300 rounded-lg px-3 py-1.5 text-slate-900 font-mono"
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Issue Description</label>
                <textarea
                  required
                  rows={2}
                  value={newDescription}
                  onChange={(e) => setNewDescription(e.target.value)}
                  placeholder="Describe failure or maintenance requirement"
                  className="w-full border border-slate-300 rounded-lg px-3 py-1.5 text-slate-900"
                />
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Priority (1=Emergency)</label>
                  <select
                    value={newPriority}
                    onChange={(e) => setNewPriority(Number(e.target.value))}
                    className="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-900 font-mono"
                  >
                    <option value={1}>1 - Emergency</option>
                    <option value={2}>2 - Critical</option>
                    <option value={3}>3 - High</option>
                    <option value={4}>4 - Medium</option>
                    <option value={5}>5 - Routine</option>
                  </select>
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Site Location</label>
                  <input
                    type="text"
                    required
                    value={newLocation}
                    onChange={(e) => setNewLocation(e.target.value)}
                    className="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-900"
                  />
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
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-semibold"
                >
                  Enqueue Ticket
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
