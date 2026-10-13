"""
Adaptive Network Design and Optimization Framework
Network Router: Topology CRUD, Sample Data Management, Graph Generators
"""

import random
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException
from ..database import (
    get_all_vertices,
    get_all_edges,
    get_db_connection,
    seed_sample_data
)
from ..models.schemas import VertexSchema, EdgeSchema, ApiResponse
from ..data.sample_data import SAMPLE_DATA_DISCLAIMER

router = APIRouter(prefix="/api/network", tags=["Network Topology"])


@router.get("", response_model=ApiResponse)
def get_network():
    """Fetches the current network topology (vertices and edges)."""
    try:
        vertices = get_all_vertices()
        edges = get_all_edges()
        return ApiResponse(
            success=True,
            data={
                "vertices": vertices,
                "edges": edges,
                "num_vertices": len(vertices),
                "num_edges": len(edges),
                "disclaimer": SAMPLE_DATA_DISCLAIMER
            },
            message="Network topology retrieved successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset", response_model=ApiResponse)
def reset_network_data():
    """Resets network topology and sample records to default hypothetical state."""
    try:
        seed_sample_data()
        return ApiResponse(
            success=True,
            data={
                "vertices": get_all_vertices(),
                "edges": get_all_edges(),
                "disclaimer": SAMPLE_DATA_DISCLAIMER
            },
            message="Database successfully restored to hypothetical demonstration sample data."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vertices", response_model=ApiResponse)
def add_vertex(vertex: VertexSchema):
    """Adds a new network vertex."""
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO vertices (id, label, x, y, tier) VALUES (?, ?, ?, ?, ?)",
            (vertex.id, vertex.label, vertex.x or random.randint(100, 800), vertex.y or random.randint(100, 500), vertex.tier)
        )
        conn.commit()
        return ApiResponse(success=True, data=vertex.dict(), message=f"Vertex '{vertex.id}' added.")
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Failed to add vertex: {str(e)}")
    finally:
        conn.close()


@router.delete("/vertices/{vertex_id}", response_model=ApiResponse)
def delete_vertex(vertex_id: str):
    """Deletes a vertex and all its connected edges."""
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM edges WHERE source = ? OR target = ?", (vertex_id, vertex_id))
        res = conn.execute("DELETE FROM vertices WHERE id = ?", (vertex_id,))
        conn.commit()
        if res.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vertex not found.")
        return ApiResponse(success=True, message=f"Vertex '{vertex_id}' and incident edges deleted.")
    finally:
        conn.close()


@router.post("/edges", response_model=ApiResponse)
def add_edge(edge: EdgeSchema):
    """Adds a weighted connection between two vertices."""
    if edge.source == edge.target:
        raise HTTPException(status_code=400, detail="Self-loops are not allowed in this network model.")

    conn = get_db_connection()
    try:
        # Verify vertices exist
        v1 = conn.execute("SELECT id FROM vertices WHERE id = ?", (edge.source,)).fetchone()
        v2 = conn.execute("SELECT id FROM vertices WHERE id = ?", (edge.target,)).fetchone()
        if not v1 or not v2:
            raise HTTPException(status_code=400, detail="Both source and target vertices must exist.")

        conn.execute(
            "INSERT INTO edges (source, target, weight, bandwidth_gbps) VALUES (?, ?, ?, ?)",
            (edge.source, edge.target, edge.weight, edge.bandwidth_gbps or 10.0)
        )
        conn.commit()
        return ApiResponse(success=True, data=edge.dict(), message="Edge created successfully.")
    finally:
        conn.close()


@router.delete("/edges/{edge_id}", response_model=ApiResponse)
def delete_edge(edge_id: int):
    """Deletes an edge by ID."""
    conn = get_db_connection()
    try:
        res = conn.execute("DELETE FROM edges WHERE id = ?", (edge_id,))
        conn.commit()
        if res.rowcount == 0:
            raise HTTPException(status_code=404, detail="Edge not found.")
        return ApiResponse(success=True, message=f"Edge {edge_id} deleted.")
    finally:
        conn.close()


@router.post("/generate", response_model=ApiResponse)
def generate_synthetic_graph(num_vertices: int = 8, density_type: str = "sparse"):
    """
    Generates a synthetic connected test graph.
    density_type: 'sparse' (E approx 1.5V) or 'dense' (E approx 0.7 * V(V-1)/2).
    """
    if num_vertices < 2 or num_vertices > 100:
        raise HTTPException(status_code=400, detail="num_vertices must be between 2 and 100.")

    v_ids = [f"N-{i+1}" for i in range(num_vertices)]
    vertices = [{"id": vid, "label": f"Node {vid}", "x": random.randint(100, 800), "y": random.randint(100, 500), "tier": "Distribution"} for vid in v_ids]

    edges = []
    # 1. Guarantee connectivity with a random spanning tree
    shuffled = list(v_ids)
    random.shuffle(shuffled)
    connected = [shuffled[0]]
    for node in shuffled[1:]:
        target = random.choice(connected)
        w = round(random.uniform(5.0, 30.0), 1)
        edges.append({"source": node, "target": target, "weight": w, "bandwidth_gbps": 10.0})
        connected.append(node)

    # 2. Add additional edges based on density
    max_possible = (num_vertices * (num_vertices - 1)) // 2
    current_e = len(edges)
    target_e = current_e

    if density_type == "dense":
        target_e = int(max_possible * 0.7)
    elif density_type == "sparse":
        target_e = min(max_possible, int(num_vertices * 1.5))

    existing_pairs = set()
    for e in edges:
        existing_pairs.add((e["source"], e["target"]))
        existing_pairs.add((e["target"], e["source"]))

    all_pairs = []
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            u, v = v_ids[i], v_ids[j]
            if (u, v) not in existing_pairs:
                all_pairs.append((u, v))

    random.shuffle(all_pairs)
    add_count = target_e - current_e
    for u, v in all_pairs[:add_count]:
        w = round(random.uniform(5.0, 50.0), 1)
        edges.append({"source": u, "target": v, "weight": w, "bandwidth_gbps": 10.0})

    actual_density = (2 * len(edges)) / (num_vertices * (num_vertices - 1)) if num_vertices > 1 else 0

    return ApiResponse(
        success=True,
        data={
            "vertices": vertices,
            "edges": edges,
            "num_vertices": len(vertices),
            "num_edges": len(edges),
            "density": round(actual_density, 3),
            "density_type": density_type
        },
        message=f"Generated synthetic {density_type} graph with {num_vertices} vertices and {len(edges)} edges."
    )
