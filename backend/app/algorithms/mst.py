"""
Adaptive Network Design and Optimization Framework
Module 1: Network Design and Minimum Spanning Tree (MST)
Algorithms: Prim's Algorithm & Kruskal's Algorithm with Disjoint-Set Union (DSU)
"""

import heapq
import time
from typing import Dict, List, Tuple, Set, Optional, Any
from pydantic import BaseModel, Field


class DisjointSetUnion:
    """
    Disjoint-Set Union (Union-Find) data structure.
    Implements path compression and union by rank.
    """
    def __init__(self, elements: List[str]):
        self.parent: Dict[str, str] = {x: x for x in elements}
        self.rank: Dict[str, int] = {x: 0 for x in elements}
        self.num_components: int = len(elements)
        self.find_ops: int = 0
        self.union_ops: int = 0

    def find(self, x: str) -> str:
        """Find representative with path compression."""
        self.find_ops += 1
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: str, y: str) -> bool:
        """Union two sets by rank. Returns True if merged, False if already in same set."""
        self.union_ops += 1
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        self.num_components -= 1
        return True


class MSTEdge(BaseModel):
    source: str
    target: str
    weight: float


class MSTResult(BaseModel):
    algorithm: str
    is_connected: bool
    spanning_tree_exists: bool
    total_cost: float
    selected_edges: List[MSTEdge]
    num_selected_edges: int
    num_vertices: int
    execution_time_ms: float
    operation_counts: Dict[str, int]
    graph_representation: str
    status_message: str


def run_prim(
    vertices: List[str],
    edges: List[Tuple[str, str, float]],
    start_vertex: Optional[str] = None
) -> MSTResult:
    """
    Prim's Algorithm for Minimum Spanning Tree.
    Graph Representation: Adjacency List (Dict[str, List[Tuple[str, float]]]).
    Complexity: O((V + E) log V) using binary min-heap.
    """
    start_time = time.perf_counter_ns()
    op_counts = {
        "heap_pushes": 0,
        "heap_pops": 0,
        "edge_explorations": 0,
        "comparisons": 0
    }

    # Handle boundary conditions
    num_v = len(vertices)
    if num_v == 0:
        elapsed = (time.perf_counter_ns() - start_time) / 1_000_000
        return MSTResult(
            algorithm="Prim",
            is_connected=True,
            spanning_tree_exists=True,
            total_cost=0.0,
            selected_edges=[],
            num_selected_edges=0,
            num_vertices=0,
            execution_time_ms=elapsed,
            operation_counts=op_counts,
            graph_representation="Adjacency List",
            status_message="Empty graph. Trivial spanning tree."
        )

    if num_v == 1:
        elapsed = (time.perf_counter_ns() - start_time) / 1_000_000
        return MSTResult(
            algorithm="Prim",
            is_connected=True,
            spanning_tree_exists=True,
            total_cost=0.0,
            selected_edges=[],
            num_selected_edges=0,
            num_vertices=1,
            execution_time_ms=elapsed,
            operation_counts=op_counts,
            graph_representation="Adjacency List",
            status_message="Single vertex graph. Spanning tree has 0 edges."
        )

    # Build Adjacency List
    adj: Dict[str, List[Tuple[str, float]]] = {v: [] for v in vertices}
    for u, v, w in edges:
        if u in adj and v in adj:
            if u == v:
                continue  # Ignore self-loops
            adj[u].append((v, float(w)))
            adj[v].append((u, float(w)))

    # Choose starting vertex
    root = start_vertex if (start_vertex and start_vertex in adj) else vertices[0]

    visited: Set[str] = set()
    visited.add(root)
    # Min-heap entries: (weight, source, target)
    min_heap: List[Tuple[float, str, str]] = []
    
    for neighbor, weight in adj[root]:
        heapq.heappush(min_heap, (weight, root, neighbor))
        op_counts["heap_pushes"] += 1

    selected_edges: List[MSTEdge] = []
    total_cost: float = 0.0

    while min_heap and len(visited) < num_v:
        weight, u, v = heapq.heappop(min_heap)
        op_counts["heap_pops"] += 1
        op_counts["comparisons"] += 1

        if v in visited:
            continue

        visited.add(v)
        selected_edges.append(MSTEdge(source=u, target=v, weight=weight))
        total_cost += weight

        for next_neighbor, next_weight in adj[v]:
            op_counts["edge_explorations"] += 1
            if next_neighbor not in visited:
                heapq.heappush(min_heap, (next_weight, v, next_neighbor))
                op_counts["heap_pushes"] += 1

    elapsed = (time.perf_counter_ns() - start_time) / 1_000_000
    is_connected = (len(visited) == num_v)

    if not is_connected:
        return MSTResult(
            algorithm="Prim",
            is_connected=False,
            spanning_tree_exists=False,
            total_cost=round(total_cost, 4),
            selected_edges=selected_edges,
            num_selected_edges=len(selected_edges),
            num_vertices=num_v,
            execution_time_ms=elapsed,
            operation_counts=op_counts,
            graph_representation="Adjacency List (Dict of lists)",
            status_message=(
                f"Graph is disconnected. Visited {len(visited)} of {num_v} vertices. "
                "No spanning tree exists for the entire graph (minimum spanning forest formed)."
            )
        )

    return MSTResult(
        algorithm="Prim",
        is_connected=True,
        spanning_tree_exists=True,
        total_cost=round(total_cost, 4),
        selected_edges=selected_edges,
        num_selected_edges=len(selected_edges),
        num_vertices=num_v,
        execution_time_ms=elapsed,
        operation_counts=op_counts,
        graph_representation="Adjacency List (Dict of lists)",
        status_message=f"Optimal MST found with {len(selected_edges)} edges connecting all {num_v} vertices."
    )


def run_kruskal(
    vertices: List[str],
    edges: List[Tuple[str, str, float]]
) -> MSTResult:
    """
    Kruskal's Algorithm for Minimum Spanning Tree.
    Graph Representation: Edge List (List[Tuple[float, str, str]]).
    Complexity: O(E log E) or O(E log V) with Disjoint-Set Union (DSU).
    """
    start_time = time.perf_counter_ns()
    op_counts = {
        "edge_sort_comparisons": 0,
        "find_operations": 0,
        "union_operations": 0,
        "examined_edges": 0
    }

    num_v = len(vertices)
    if num_v == 0:
        elapsed = (time.perf_counter_ns() - start_time) / 1_000_000
        return MSTResult(
            algorithm="Kruskal",
            is_connected=True,
            spanning_tree_exists=True,
            total_cost=0.0,
            selected_edges=[],
            num_selected_edges=0,
            num_vertices=0,
            execution_time_ms=elapsed,
            operation_counts=op_counts,
            graph_representation="Edge List",
            status_message="Empty graph. Trivial spanning tree."
        )

    if num_v == 1:
        elapsed = (time.perf_counter_ns() - start_time) / 1_000_000
        return MSTResult(
            algorithm="Kruskal",
            is_connected=True,
            spanning_tree_exists=True,
            total_cost=0.0,
            selected_edges=[],
            num_selected_edges=0,
            num_vertices=1,
            execution_time_ms=elapsed,
            operation_counts=op_counts,
            graph_representation="Edge List",
            status_message="Single vertex graph. Spanning tree has 0 edges."
        )

    # Clean edges: remove self-loops, filter invalid endpoints
    valid_vertices = set(vertices)
    clean_edges: List[Tuple[float, str, str]] = []
    for u, v, w in edges:
        if u in valid_vertices and v in valid_vertices and u != v:
            clean_edges.append((float(w), u, v))

    # Sort edges by weight
    clean_edges.sort(key=lambda x: x[0])
    op_counts["edge_sort_comparisons"] = int(len(clean_edges) * max(1, len(clean_edges).bit_length()))

    dsu = DisjointSetUnion(vertices)
    selected_edges: List[MSTEdge] = []
    total_cost: float = 0.0

    for weight, u, v in clean_edges:
        op_counts["examined_edges"] += 1
        if dsu.find(u) != dsu.find(v):
            dsu.union(u, v)
            selected_edges.append(MSTEdge(source=u, target=v, weight=weight))
            total_cost += weight
            if len(selected_edges) == num_v - 1:
                break

    op_counts["find_operations"] = dsu.find_ops
    op_counts["union_operations"] = dsu.union_ops

    elapsed = (time.perf_counter_ns() - start_time) / 1_000_000
    is_connected = (dsu.num_components == 1 and len(selected_edges) == num_v - 1)

    if not is_connected:
        return MSTResult(
            algorithm="Kruskal",
            is_connected=False,
            spanning_tree_exists=False,
            total_cost=round(total_cost, 4),
            selected_edges=selected_edges,
            num_selected_edges=len(selected_edges),
            num_vertices=num_v,
            execution_time_ms=elapsed,
            operation_counts=op_counts,
            graph_representation="Edge List with Disjoint-Set Union (Rank & Path Compression)",
            status_message=(
                f"Graph is disconnected. Result contains {dsu.num_components} components. "
                f"Selected {len(selected_edges)} edges. Complete spanning tree does not exist."
            )
        )

    return MSTResult(
        algorithm="Kruskal",
        is_connected=True,
        spanning_tree_exists=True,
        total_cost=round(total_cost, 4),
        selected_edges=selected_edges,
        num_selected_edges=len(selected_edges),
        num_vertices=num_v,
        execution_time_ms=elapsed,
        operation_counts=op_counts,
        graph_representation="Edge List with Disjoint-Set Union (Rank & Path Compression)",
        status_message=f"Optimal MST found with {len(selected_edges)} edges connecting all {num_v} vertices."
    )


def compare_prim_kruskal(
    vertices: List[str],
    edges: List[Tuple[str, str, float]]
) -> Dict[str, Any]:
    """Runs and compares Prim and Kruskal side by side."""
    prim_res = run_prim(vertices, edges)
    kruskal_res = run_kruskal(vertices, edges)

    cost_agreement = (
        prim_res.spanning_tree_exists == kruskal_res.spanning_tree_exists
        and abs(prim_res.total_cost - kruskal_res.total_cost) < 1e-6
    )

    num_v = len(vertices)
    num_e = len(edges)
    density = (2 * num_e) / (num_v * (num_v - 1)) if num_v > 1 else 0.0

    return {
        "num_vertices": num_v,
        "num_edges": num_e,
        "density": round(density, 4),
        "is_dense": density > 0.5,
        "cost_agreement": cost_agreement,
        "prim": prim_res.dict(),
        "kruskal": kruskal_res.dict(),
        "recommendation": (
            "Prim's algorithm is theoretically preferred for dense networks (E ≈ V²) using an adjacency list/matrix.",
            "Kruskal's algorithm is theoretically preferred for sparse networks (E ≪ V²) with edge-list sorting and DSU."
        ) if not cost_agreement else (
            "Both algorithms successfully verified identical optimal MST cost."
        )
    }
