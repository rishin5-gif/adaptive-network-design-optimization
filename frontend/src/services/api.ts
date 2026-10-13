/**
 * API Service Client for Adaptive Network Framework Backend
 */

import {
  ApiResponse,
  DashboardSummary,
  Vertex,
  Edge,
  MSTResult,
  MSTComparison,
  FloydWarshallResult,
  PathResult,
  DeviceRecord,
  MaintenanceEvent,
  UpgradeProject,
  KnapsackResult,
  TSPResult,
  AlgorithmExplanation
} from '../types';

const API_BASE = '/api';

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  const json: ApiResponse<T> = await res.json();
  if (!res.ok || !json.success) {
    throw new Error(json.error || json.message || `Request failed with status ${res.status}`);
  }
  return json.data as T;
}

export const api = {
  // Health
  getHealth: () => request<any>('/health'),

  // Dashboard
  getDashboardSummary: () => request<DashboardSummary>('/dashboard/summary'),

  // Network Topology CRUD
  getNetwork: () => request<{ vertices: Vertex[]; edges: Edge[]; disclaimer: string }>('/network'),
  resetNetwork: () => request<{ vertices: Vertex[]; edges: Edge[]; disclaimer: string }>('/network/reset', { method: 'POST' }),
  addVertex: (vertex: Vertex) => request<Vertex>('/network/vertices', { method: 'POST', body: JSON.stringify(vertex) }),
  deleteVertex: (id: string) => request<any>(`/network/vertices/${id}`, { method: 'DELETE' }),
  addEdge: (edge: Edge) => request<Edge>('/network/edges', { method: 'POST', body: JSON.stringify(edge) }),
  deleteEdge: (id: number) => request<any>(`/network/edges/${id}`, { method: 'DELETE' }),
  generateGraph: (numVertices: number, densityType: string) =>
    request<{ vertices: Vertex[]; edges: Edge[]; density: number }>(`/network/generate?num_vertices=${numVertices}&density_type=${densityType}`, { method: 'POST' }),

  // Module 1: MST Algorithms
  runPrim: (vertices: string[], edges: [string, string, number][], startVertex?: string) =>
    request<{ result: MSTResult; explanation: AlgorithmExplanation }>('/algorithms/prim', {
      method: 'POST',
      body: JSON.stringify({ vertices, edges, start_vertex: startVertex }),
    }),
  runKruskal: (vertices: string[], edges: [string, string, number][]) =>
    request<{ result: MSTResult; explanation: AlgorithmExplanation }>('/algorithms/kruskal', {
      method: 'POST',
      body: JSON.stringify({ vertices, edges }),
    }),
  compareMST: (vertices: string[], edges: [string, string, number][]) =>
    request<{ comparison: MSTComparison; explanation: AlgorithmExplanation }>('/algorithms/mst/compare', {
      method: 'POST',
      body: JSON.stringify({ vertices, edges }),
    }),

  // Module 2: All-Pairs Shortest Path
  runFloydWarshall: (vertices: string[], edges: [string, string, number][], isDirected = false) =>
    request<{ result: FloydWarshallResult; explanation: AlgorithmExplanation }>('/algorithms/floyd-warshall', {
      method: 'POST',
      body: JSON.stringify({ vertices, edges, is_directed: isDirected }),
    }),
  getPath: (source: string, target: string, vertices: string[], edges: [string, string, number][], isDirected = false) =>
    request<PathResult>(`/algorithms/floyd-warshall/path?source=${encodeURIComponent(source)}&target=${encodeURIComponent(target)}`, {
      method: 'POST',
      body: JSON.stringify({ vertices, edges, is_directed: isDirected }),
    }),

  // Module 3: Trees (B-Tree & Red-Black Tree)
  executeBTreeOp: (operation: string, deviceId?: string, record?: DeviceRecord, orderT = 3) =>
    request<any>('/structures/btree/operations', {
      method: 'POST',
      body: JSON.stringify({ operation, device_id: deviceId, record, order_t: orderT }),
    }),
  executeRBTOp: (operation: string, deviceId?: string, record?: DeviceRecord) =>
    request<any>('/structures/red-black-tree/operations', {
      method: 'POST',
      body: JSON.stringify({ operation, device_id: deviceId, record }),
    }),
  compareTreeWorkload: (records: DeviceRecord[], searchIds: string[], deleteIds: string[], bTreeOrder = 3) =>
    request<any>('/structures/trees/compare-workload', {
      method: 'POST',
      body: JSON.stringify({ records, search_ids: searchIds, delete_ids: deleteIds, b_tree_order: bTreeOrder }),
    }),

  // Module 4: Heaps (Binomial & Fibonacci)
  executeBinomialHeapOp: (operation: string, eventId?: string, newPriority?: number, event?: MaintenanceEvent) =>
    request<any>('/structures/binomial-heap/operations', {
      method: 'POST',
      body: JSON.stringify({ heap_type: 'binomial', operation, event_id: eventId, new_priority: newPriority, event }),
    }),
  executeFibHeapOp: (operation: string, eventId?: string, newPriority?: number, event?: MaintenanceEvent) =>
    request<any>('/structures/fibonacci-heap/operations', {
      method: 'POST',
      body: JSON.stringify({ heap_type: 'fibonacci', operation, event_id: eventId, new_priority: newPriority, event }),
    }),
  compareHeapWorkload: (events: MaintenanceEvent[], decreases: { event_id: string; new_priority: number }[], extractCount = 2) =>
    request<any>('/structures/heaps/compare-workload', {
      method: 'POST',
      body: JSON.stringify({ events, priority_decreases: decreases, extract_count: extractCount }),
    }),

  // Module 5: Budget Planner (Knapsack)
  runFractionalKnapsack: (projects: UpgradeProject[], budget: number) =>
    request<{ result: KnapsackResult; explanation: AlgorithmExplanation }>('/optimization/fractional-knapsack', {
      method: 'POST',
      body: JSON.stringify({ projects, budget }),
    }),
  run01Knapsack: (projects: UpgradeProject[], budget: number) =>
    request<{ result: KnapsackResult; explanation: AlgorithmExplanation }>('/optimization/01-knapsack', {
      method: 'POST',
      body: JSON.stringify({ projects, budget }),
    }),
  compareKnapsack: (projects: UpgradeProject[], budget: number) =>
    request<{ fractional: KnapsackResult; discrete_01: KnapsackResult; benefit_gap: number; explanation: AlgorithmExplanation }>('/optimization/knapsack/compare', {
      method: 'POST',
      body: JSON.stringify({ projects, budget }),
    }),

  // Module 6: Route Planner (TSP)
  runTSPBacktracking: (locations: string[], costMatrix?: Record<string, Record<string, number>>, startLocation?: string, timeoutSec = 4.0) =>
    request<{ result: TSPResult; explanation: AlgorithmExplanation }>('/optimization/tsp/backtracking', {
      method: 'POST',
      body: JSON.stringify({ locations, cost_matrix: costMatrix, start_location: startLocation, timeout_sec: timeoutSec }),
    }),
  runTSPBranchAndBound: (locations: string[], costMatrix?: Record<string, Record<string, number>>, startLocation?: string, timeoutSec = 4.0) =>
    request<{ result: TSPResult; explanation: AlgorithmExplanation }>('/optimization/tsp/branch-and-bound', {
      method: 'POST',
      body: JSON.stringify({ locations, cost_matrix: costMatrix, start_location: startLocation, timeout_sec: timeoutSec }),
    }),
  compareTSP: (locations: string[], costMatrix?: Record<string, Record<string, number>>, startLocation?: string, timeoutSec = 4.0) =>
    request<any>('/optimization/tsp/compare', {
      method: 'POST',
      body: JSON.stringify({ locations, cost_matrix: costMatrix, start_location: startLocation, timeout_sec: timeoutSec }),
    }),

  // Module 7: Performance Experiments Lab
  runExperiment: (family: string, params: Record<string, any>, trials = 3) =>
    request<any>('/experiments/run', {
      method: 'POST',
      body: JSON.stringify({ experiment_family: family, params, trials }),
    }),
  getExperimentHistory: () => request<{ runs: any[]; count: number }>('/experiments/history'),
  getExportUrl: () => `${API_BASE}/experiments/export`,
};
