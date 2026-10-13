"""
Adaptive Network Design and Optimization Framework
Pydantic Schemas for Request Validation and Consistent API Responses
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class VertexSchema(BaseModel):
    id: str
    label: str
    x: Optional[float] = None
    y: Optional[float] = None
    tier: Optional[str] = "Distribution"


class EdgeSchema(BaseModel):
    source: str
    target: str
    weight: float = Field(..., ge=0.0, description="Cost or weight of connection")
    bandwidth_gbps: Optional[float] = 10.0


class NetworkGraphSchema(BaseModel):
    vertices: List[VertexSchema]
    edges: List[EdgeSchema]


class DeviceRecordSchema(BaseModel):
    device_id: str
    device_name: str
    network_location: str
    device_category: str  # Router, Switch, Firewall, Gateway, Edge Server
    operational_status: str  # Active, Maintenance, Offline
    metadata: Optional[Dict[str, Any]] = None


class MaintenanceEventSchema(BaseModel):
    event_id: str
    description: str
    priority: int = Field(..., ge=1, le=10, description="1=Highest urgency/Emergency, 10=Lowest")
    network_location: str
    created_at: Optional[str] = None


class UpgradeProjectSchema(BaseModel):
    project_id: str
    project_name: str
    cost: float = Field(..., ge=0.0)
    expected_benefit: float = Field(..., ge=0.0)
    divisibility: str = "indivisible"  # divisible or indivisible


class RunMSTRequest(BaseModel):
    vertices: List[str]
    edges: List[List[Any]]  # [[u, v, weight], ...]
    algorithm: Optional[str] = "both"  # "prim", "kruskal", or "both"
    start_vertex: Optional[str] = None


class RunFloydWarshallRequest(BaseModel):
    vertices: List[str]
    edges: List[List[Any]]
    is_directed: Optional[bool] = False


class TreeOperationRequest(BaseModel):
    operation: str  # insert, search, update, delete, get_all, verify_invariants
    record: Optional[DeviceRecordSchema] = None
    device_id: Optional[str] = None
    order_t: Optional[int] = 3


class TreeWorkloadRequest(BaseModel):
    records: List[DeviceRecordSchema]
    search_ids: List[str]
    delete_ids: List[str]
    b_tree_order: Optional[int] = 3


class HeapOperationRequest(BaseModel):
    heap_type: str  # binomial or fibonacci
    operation: str  # insert, find_min, extract_min, decrease_key, get_all
    event: Optional[MaintenanceEventSchema] = None
    event_id: Optional[str] = None
    new_priority: Optional[int] = None


class HeapWorkloadRequest(BaseModel):
    events: List[MaintenanceEventSchema]
    priority_decreases: List[Dict[str, Any]]  # [{"event_id": "...", "new_priority": 1}]
    extract_count: Optional[int] = 3


class KnapsackRequest(BaseModel):
    projects: List[UpgradeProjectSchema]
    budget: float = Field(..., ge=0.0)
    force_divisible: Optional[bool] = None


class TSPRequest(BaseModel):
    locations: List[str]
    cost_matrix: Optional[Dict[str, Dict[str, float]]] = None
    start_location: Optional[str] = None
    algorithm: Optional[str] = "both"  # "backtracking", "branch_and_bound", "both"
    timeout_sec: Optional[float] = 4.0


class ExperimentRunRequest(BaseModel):
    experiment_family: str
    # "sparse_vs_dense_mst", "floyd_warshall_scaling", "tree_workloads", "heap_workloads", "knapsack_divisibility", "tsp_scaling"
    params: Dict[str, Any]
    trials: Optional[int] = 3


class ApiResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None
