"""
Adaptive Network Design and Optimization Framework
Dashboard Router: Aggregated System Metrics & Activity Summary
"""

from typing import Dict, Any
from fastapi import APIRouter
from ..database import (
    get_all_vertices,
    get_all_edges,
    get_all_devices,
    get_all_maintenance_events,
    get_all_upgrade_projects,
    get_recent_experiments
)
from ..algorithms.mst import run_kruskal
from ..models.schemas import ApiResponse
from ..data.sample_data import SAMPLE_DATA_DISCLAIMER

router = APIRouter(prefix="/api/dashboard", tags=["Overview Dashboard"])


@router.get("/summary", response_model=ApiResponse)
def get_dashboard_summary():
    """Returns real-time aggregated metrics computed from stored records and algorithms."""
    vertices = get_all_vertices()
    edges = get_all_edges()
    devices = get_all_devices()
    events = get_all_maintenance_events()
    projects = get_all_upgrade_projects()
    recent_experiments = get_recent_experiments(limit=5)

    # Compute current MST cost dynamically
    v_ids = [v["id"] for v in vertices]
    edge_tuples = [(e["source"], e["target"], float(e["weight"])) for e in edges]
    mst_res = run_kruskal(v_ids, edge_tuples)

    # Calculate total upgrade budget needed & average event priority
    total_project_cost = sum(p["cost"] for p in projects)
    total_project_benefit = sum(p["expected_benefit"] for p in projects)
    avg_priority = (sum(e["priority"] for e in events) / len(events)) if events else 0.0

    last_experiment = recent_experiments[0] if recent_experiments else None

    return ApiResponse(
        success=True,
        data={
            "num_locations": len(vertices),
            "num_links": len(edges),
            "mst_cost": mst_res.total_cost if mst_res.spanning_tree_exists else None,
            "mst_connected": mst_res.is_connected,
            "num_devices": len(devices),
            "num_maintenance_events": len(events),
            "avg_event_priority": round(avg_priority, 2),
            "num_upgrade_projects": len(projects),
            "total_upgrade_cost_pool": total_project_cost,
            "total_upgrade_benefit_pool": total_project_benefit,
            "last_completed_experiment": {
                "family": last_experiment["experiment_family"] if last_experiment else "None",
                "timestamp": last_experiment["execution_timestamp"] if last_experiment else "None"
            } if last_experiment else None,
            "disclaimer": SAMPLE_DATA_DISCLAIMER
        },
        message="Dashboard metrics aggregated successfully."
    )
