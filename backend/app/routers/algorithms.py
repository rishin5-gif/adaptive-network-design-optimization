"""
Adaptive Network Design and Optimization Framework
Algorithms Router: Module 1 (MST) & Module 2 (All-Pairs Shortest Paths)
"""

from typing import List, Tuple
from fastapi import APIRouter, HTTPException
from ..models.schemas import (
    RunMSTRequest,
    RunFloydWarshallRequest,
    ApiResponse
)
from ..algorithms.mst import run_prim, run_kruskal, compare_prim_kruskal
from ..algorithms.all_pairs import run_floyd_warshall, reconstruct_path
from ..algorithms.explanation_engine import generate_explanation

router = APIRouter(prefix="/api/algorithms", tags=["Graph Algorithms"])


@router.post("/prim", response_model=ApiResponse)
def execute_prim(req: RunMSTRequest):
    """Executes Prim's Algorithm for Minimum Spanning Tree."""
    try:
        clean_edges: List[Tuple[str, str, float]] = [(e[0], e[1], float(e[2])) for e in req.edges]
        result = run_prim(req.vertices, clean_edges, req.start_vertex)
        
        num_v = len(req.vertices)
        num_e = len(clean_edges)
        density = (2 * num_e) / (num_v * (num_v - 1)) if num_v > 1 else 0.0

        explanation = generate_explanation("module1_mst", {
            "density": density,
            "num_vertices": num_v,
            "num_edges": num_e,
            "summary": f"Prim's algorithm found spanning tree of cost {result.total_cost:.2f} using {len(result.selected_edges)} edges."
        })

        return ApiResponse(
            success=True,
            data={
                "result": result.dict(),
                "explanation": explanation.dict()
            },
            message="Prim's algorithm executed successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/kruskal", response_model=ApiResponse)
def execute_kruskal(req: RunMSTRequest):
    """Executes Kruskal's Algorithm for Minimum Spanning Tree."""
    try:
        clean_edges: List[Tuple[str, str, float]] = [(e[0], e[1], float(e[2])) for e in req.edges]
        result = run_kruskal(req.vertices, clean_edges)

        num_v = len(req.vertices)
        num_e = len(clean_edges)
        density = (2 * num_e) / (num_v * (num_v - 1)) if num_v > 1 else 0.0

        explanation = generate_explanation("module1_mst", {
            "density": density,
            "num_vertices": num_v,
            "num_edges": num_e,
            "summary": f"Kruskal's algorithm found spanning tree of cost {result.total_cost:.2f} using {len(result.selected_edges)} edges."
        })

        return ApiResponse(
            success=True,
            data={
                "result": result.dict(),
                "explanation": explanation.dict()
            },
            message="Kruskal's algorithm executed successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/mst/compare", response_model=ApiResponse)
def compare_mst_algorithms(req: RunMSTRequest):
    """Executes and compares Prim and Kruskal side by side with operation counts."""
    try:
        clean_edges: List[Tuple[str, str, float]] = [(e[0], e[1], float(e[2])) for e in req.edges]
        comparison = compare_prim_kruskal(req.vertices, clean_edges)

        explanation = generate_explanation("module1_mst", {
            "density": comparison["density"],
            "num_vertices": comparison["num_vertices"],
            "num_edges": comparison["num_edges"],
            "summary": (
                f"Prim Total Cost: {comparison['prim']['total_cost']} vs "
                f"Kruskal Total Cost: {comparison['kruskal']['total_cost']}. "
                f"Agreement: {comparison['cost_agreement']}."
            )
        })

        return ApiResponse(
            success=True,
            data={
                "comparison": comparison,
                "explanation": explanation.dict()
            },
            message="MST algorithms compared successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/floyd-warshall", response_model=ApiResponse)
def execute_floyd_warshall(req: RunFloydWarshallRequest):
    """Executes Floyd-Warshall All-Pairs Shortest Path algorithm."""
    try:
        clean_edges: List[Tuple[str, str, float]] = [(e[0], e[1], float(e[2])) for e in req.edges]
        has_negative = any(w < 0 for _, _, w in clean_edges)
        result = run_floyd_warshall(req.vertices, clean_edges, req.is_directed or False)

        explanation = generate_explanation("module2_all_pairs", {
            "num_vertices": len(req.vertices),
            "has_negative_weights": has_negative,
            "summary": f"Computed complete distance matrix for {len(req.vertices)} nodes in {result.execution_time_ms:.3f} ms."
        })

        return ApiResponse(
            success=True,
            data={
                "result": result.dict(),
                "explanation": explanation.dict()
            },
            message="Floyd-Warshall executed successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/floyd-warshall/path", response_model=ApiResponse)
def get_shortest_path(source: str, target: str, req: RunFloydWarshallRequest):
    """Reconstructs shortest path between source and target nodes."""
    try:
        clean_edges: List[Tuple[str, str, float]] = [(e[0], e[1], float(e[2])) for e in req.edges]
        fw_result = run_floyd_warshall(req.vertices, clean_edges, req.is_directed or False)
        path_res = reconstruct_path(source, target, req.vertices, fw_result.predecessor_matrix)

        # Look up distance
        v_map = {v: i for i, v in enumerate(req.vertices)}
        if source in v_map and target in v_map:
            cost = fw_result.distance_matrix[v_map[source]][v_map[target]]
            path_res.cost = cost

        return ApiResponse(
            success=True,
            data=path_res.dict(),
            message=f"Path reconstruction from {source} to {target} completed."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
