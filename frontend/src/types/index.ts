/**
 * TypeScript Data Models for Adaptive Network Framework
 */

export interface Vertex {
  id: string;
  label: string;
  x?: number;
  y?: number;
  tier?: string;
}

export interface Edge {
  id?: number;
  source: string;
  target: string;
  weight: number;
  bandwidth_gbps?: number;
}

export interface MSTEdge {
  source: string;
  target: string;
  weight: number;
}

export interface MSTResult {
  algorithm: string;
  is_connected: boolean;
  spanning_tree_exists: boolean;
  total_cost: number;
  selected_edges: MSTEdge[];
  num_selected_edges: number;
  num_vertices: number;
  execution_time_ms: number;
  operation_counts: Record<string, number>;
  graph_representation: string;
  status_message: string;
}

export interface MSTComparison {
  num_vertices: number;
  num_edges: number;
  density: number;
  is_dense: boolean;
  cost_agreement: boolean;
  prim: MSTResult;
  kruskal: MSTResult;
  recommendation: string | string[];
}

export interface FloydWarshallResult {
  algorithm: string;
  num_vertices: number;
  vertices: string[];
  distance_matrix: (number | null)[][];
  predecessor_matrix: (number | null)[][];
  has_negative_cycle: boolean;
  negative_cycle_nodes: string[];
  execution_time_ms: number;
  total_triplet_relaxations: number;
  total_distance_updates: number;
  complexity_time: string;
  complexity_space: string;
  explanation: string;
}

export interface PathResult {
  source: string;
  target: string;
  cost: number | null;
  is_reachable: boolean;
  path: string[];
}

export interface DeviceRecord {
  device_id: string;
  device_name: string;
  network_location: string;
  device_category: string;
  operational_status: string;
  metadata?: Record<string, any>;
}

export interface MaintenanceEvent {
  event_id: string;
  description: string;
  priority: number;
  network_location: string;
  created_at?: string;
}

export interface UpgradeProject {
  project_id: string;
  project_name: string;
  cost: number;
  expected_benefit: number;
  divisibility: string;
}

export interface SelectedProjectAllocation {
  project_id: string;
  project_name: string;
  original_cost: number;
  original_benefit: number;
  allocated_fraction: number;
  allocated_cost: number;
  allocated_benefit: number;
  benefit_to_cost_ratio: number;
}

export interface KnapsackResult {
  algorithm: string;
  total_budget: number;
  total_cost_spent: number;
  total_benefit_gained: number;
  remaining_budget: number;
  num_projects_considered: number;
  num_projects_selected: number;
  allocations: SelectedProjectAllocation[];
  execution_time_ms: number;
  complexity_time: string;
  complexity_space: string;
  is_optimal: boolean;
  selection_reason: string;
  counterexample_note?: string;
}

export interface TSPResult {
  algorithm: string;
  is_feasible: boolean;
  num_locations: number;
  start_location: string;
  optimal_tour: string[];
  total_tour_cost: number | null;
  states_explored: number;
  states_pruned: number;
  execution_time_ms: number;
  timed_out: boolean;
  complexity_class: string;
  explanation: string;
  scalability_warning: string;
}

export interface AlgorithmExplanation {
  module_name: string;
  real_world_question: string;
  mathematical_formulation: string;
  input_properties: Record<string, any>;
  selected_algorithm: string;
  alternative_considered: string;
  selection_reason: string;
  expected_time_complexity: string;
  expected_space_complexity: string;
  correctness_assumptions: string;
  actual_result_summary: string;
  limitations_and_warnings: string;
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface DashboardSummary {
  num_locations: number;
  num_links: number;
  mst_cost: number | null;
  mst_connected: boolean;
  num_devices: number;
  num_maintenance_events: number;
  avg_event_priority: number;
  num_upgrade_projects: number;
  total_upgrade_cost_pool: number;
  total_upgrade_benefit_pool: number;
  last_completed_experiment?: {
    family: string;
    timestamp: string;
  };
  disclaimer: string;
}
