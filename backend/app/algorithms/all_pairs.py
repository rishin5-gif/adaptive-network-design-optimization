"""
Adaptive Network Design and Optimization Framework
Module 2: All-Pairs Communication Cost Analysis
Algorithm: Floyd-Warshall Algorithm (Dynamic Programming)
"""

import time
import math
from typing import Dict, List, Tuple, Optional, Any
from pydantic import BaseModel


class PathResult(BaseModel):
    source: str
    target: str
    cost: Optional[float]
    is_reachable: bool
    path: List[str]


class FloydWarshallResult(BaseModel):
    algorithm: str = "Floyd-Warshall"
    num_vertices: int
    vertices: List[str]
    distance_matrix: List[List[Optional[float]]]
    predecessor_matrix: List[List[Optional[int]]]
    has_negative_cycle: bool
    negative_cycle_nodes: List[str]
    execution_time_ms: float
    total_triplet_relaxations: int
    total_distance_updates: int
    complexity_time: str = "O(V^3)"
    complexity_space: str = "O(V^2)"
    explanation: str


def run_floyd_warshall(
    vertices: List[str],
    edges: List[Tuple[str, str, float]],
    is_directed: bool = False
) -> FloydWarshallResult:
    """
    Executes Floyd-Warshall All-Pairs Shortest Path algorithm.
    Time Complexity: O(V^3)
    Space Complexity: O(V^2)
    Safe handling of infinity, path reconstruction matrix, and negative cycle detection.
    """
    start_time = time.perf_counter_ns()
    n = len(vertices)
    v_map = {v: i for i, v in enumerate(vertices)}

    # Initialize Distance matrix D and Predecessor matrix Pi
    # Using math.inf for unreachable entries
    D: List[List[float]] = [[math.inf] * n for _ in range(n)]
    Pi: List[List[Optional[int]]] = [[None] * n for _ in range(n)]

    # 1. Base cases: Diagonal distances are 0
    for i in range(n):
        D[i][i] = 0.0

    # 2. Base cases: Direct edges
    for u, v, w in edges:
        if u in v_map and v in v_map:
            ui, vi = v_map[u], v_map[v]
            weight = float(w)
            if weight < D[ui][vi]:
                D[ui][vi] = weight
                Pi[ui][vi] = ui
            if not is_directed:
                if weight < D[vi][ui]:
                    D[vi][ui] = weight
                    Pi[vi][ui] = vi

    relaxation_count = 0
    update_count = 0

    # 3. Canonical Three-loop recurrence:
    # D[i][j] = min(D[i][j], D[i][k] + D[k][j]) for intermediate vertices k from 0 to n-1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                relaxation_count += 1
                if D[i][k] != math.inf and D[k][j] != math.inf:
                    through_k = D[i][k] + D[k][j]
                    if through_k < D[i][j]:
                        D[i][j] = through_k
                        Pi[i][j] = Pi[k][j]
                        update_count += 1

    # 4. Negative Cycle Detection:
    # A negative cycle exists if any diagonal element becomes strictly negative (D[i][i] < 0)
    has_negative_cycle = False
    neg_nodes: List[str] = []
    for i in range(n):
        if D[i][i] < 0:
            has_negative_cycle = True
            neg_nodes.append(vertices[i])

    elapsed_ms = (time.perf_counter_ns() - start_time) / 1_000_000

    # Format distance matrix for JSON response (replace math.inf with None)
    clean_dist: List[List[Optional[float]]] = []
    for i in range(n):
        row: List[Optional[float]] = []
        for j in range(n):
            if D[i][j] == math.inf:
                row.append(None)
            else:
                row.append(round(D[i][j], 4))
        clean_dist.append(row)

    explanation = (
        f"Floyd-Warshall evaluated all {relaxation_count} (i, k, j) triplet paths across {n} nodes. "
        f"Found {update_count} shortest path relaxations. "
    )
    if has_negative_cycle:
        explanation += f"WARNING: Negative cycle detected involving vertices: {', '.join(neg_nodes)}."
    else:
        explanation += "All-pairs shortest distances computed successfully without negative cycles."

    return FloydWarshallResult(
        num_vertices=n,
        vertices=vertices,
        distance_matrix=clean_dist,
        predecessor_matrix=Pi,
        has_negative_cycle=has_negative_cycle,
        negative_cycle_nodes=neg_nodes,
        execution_time_ms=elapsed_ms,
        total_triplet_relaxations=relaxation_count,
        total_distance_updates=update_count,
        explanation=explanation
    )


def reconstruct_path(
    source: str,
    target: str,
    vertices: List[str],
    predecessor_matrix: List[List[Optional[int]]]
) -> PathResult:
    """Reconstructs the shortest path between source and target using predecessor matrix."""
    v_map = {v: i for i, v in enumerate(vertices)}
    if source not in v_map or target not in v_map:
        return PathResult(source=source, target=target, cost=None, is_reachable=False, path=[])

    s_idx = v_map[source]
    t_idx = v_map[target]

    if s_idx == t_idx:
        return PathResult(source=source, target=target, cost=0.0, is_reachable=True, path=[source])

    if predecessor_matrix[s_idx][t_idx] is None:
        return PathResult(source=source, target=target, cost=None, is_reachable=False, path=[])

    path_indices = [t_idx]
    curr = t_idx
    # Reconstruct backwards
    visited = set()
    while curr != s_idx:
        visited.add(curr)
        prev = predecessor_matrix[s_idx][curr]
        if prev is None or prev in visited:
            return PathResult(source=source, target=target, cost=None, is_reachable=False, path=[])
        path_indices.append(prev)
        curr = prev

    path_indices.reverse()
    path = [vertices[idx] for idx in path_indices]
    return PathResult(source=source, target=target, cost=None, is_reachable=True, path=path)
