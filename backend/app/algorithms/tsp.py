"""
Adaptive Network Design and Optimization Framework
Module 6: Maintenance Route Planner (Travelling Salesperson Problem - TSP)
Algorithms:
1. Exact Backtracking (Depth-First Permutation Search with Cost Pruning)
2. Branch and Bound (Reduced Outgoing Edge Lower Bounding with State Pruning)
NP-Classification:
- Optimization TSP is NP-Hard.
- Decision TSP (Is there a tour of cost <= k?) is NP-Complete.
"""

import time
import math
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel


class TSPResult(BaseModel):
    algorithm: str
    is_feasible: bool
    num_locations: int
    start_location: str
    optimal_tour: List[str]
    total_tour_cost: Optional[float]
    states_explored: int
    states_pruned: int
    execution_time_ms: float
    timed_out: bool
    complexity_class: str = "NP-Hard (Optimization) / NP-Complete (Decision)"
    explanation: str
    scalability_warning: str


def solve_tsp_backtracking(
    locations: List[str],
    cost_matrix: Dict[str, Dict[str, float]],
    start_location: Optional[str] = None,
    timeout_sec: float = 4.0
) -> TSPResult:
    """
    Exact Backtracking TSP Solver.
    Worst-case complexity: O((n-1)!).
    """
    start_time = time.perf_counter_ns()
    n = len(locations)

    if n <= 1:
        elapsed = (time.perf_counter_ns() - start_time) / 1_000_000
        loc = locations[0] if n == 1 else ""
        return TSPResult(
            algorithm="Exact Backtracking",
            is_feasible=True,
            num_locations=n,
            start_location=loc,
            optimal_tour=[loc] if n == 1 else [],
            total_tour_cost=0.0,
            states_explored=1,
            states_pruned=0,
            execution_time_ms=elapsed,
            timed_out=False,
            explanation="Trivial tour for small instance.",
            scalability_warning="No scalability concern for n <= 1."
        )

    start_loc = start_location if (start_location and start_location in locations) else locations[0]
    unvisited = [loc for loc in locations if loc != start_loc]

    best_cost: float = math.inf
    best_tour: List[str] = []
    states_explored: int = 0
    states_pruned: int = 0
    timed_out: bool = False

    time_limit_ns = int(timeout_sec * 1_000_000_000)
    deadline_ns = start_time + time_limit_ns

    def _backtrack(curr_loc: str, current_cost: float, path: List[str], remaining: List[str]):
        nonlocal best_cost, best_tour, states_explored, states_pruned, timed_out

        states_explored += 1

        if time.perf_counter_ns() > deadline_ns:
            timed_out = True
            return

        # Prune if current cost is already worse than best known
        if current_cost >= best_cost:
            states_pruned += 1
            return

        if not remaining:
            # Check edge back to start_loc to complete cycle
            return_cost = cost_matrix.get(curr_loc, {}).get(start_loc, math.inf)
            if return_cost != math.inf:
                total_cycle_cost = current_cost + return_cost
                if total_cycle_cost < best_cost:
                    best_cost = total_cycle_cost
                    best_tour = path + [start_loc]
            return

        for i, next_loc in enumerate(remaining):
            edge_cost = cost_matrix.get(curr_loc, {}).get(next_loc, math.inf)
            if edge_cost != math.inf:
                next_remaining = remaining[:i] + remaining[i + 1:]
                _backtrack(next_loc, current_cost + edge_cost, path + [next_loc], next_remaining)
                if timed_out:
                    return

    _backtrack(start_loc, 0.0, [start_loc], unvisited)

    elapsed = (time.perf_counter_ns() - start_time) / 1_000_000
    is_feasible = (best_cost != math.inf)

    warning = (
        f"Scalability Warning: TSP state space grows as O((n-1)!). "
        f"For n={n}, theoretical permutation count is {math.factorial(n - 1)}. "
        "Instances with n > 13 become intractable for exact CPU search without approximation."
    )

    explanation = (
        f"Backtracking evaluated {states_explored} recursive states and pruned {states_pruned} partial branches. "
    )
    if timed_out:
        explanation += f"Execution reached timeout limit of {timeout_sec}s. Solution established up to interruption."
    elif is_feasible:
        explanation += f"Found optimal maintenance tour visiting all {n} locations and returning to {start_loc}."
    else:
        explanation += "Graph is not Hamiltonian connected. No feasible complete tour exists."

    return TSPResult(
        algorithm="Exact Backtracking",
        is_feasible=is_feasible,
        num_locations=n,
        start_location=start_loc,
        optimal_tour=best_tour if is_feasible else [],
        total_tour_cost=round(best_cost, 4) if is_feasible else None,
        states_explored=states_explored,
        states_pruned=states_pruned,
        execution_time_ms=elapsed,
        timed_out=timed_out,
        explanation=explanation,
        scalability_warning=warning
    )


def solve_tsp_branch_and_bound(
    locations: List[str],
    cost_matrix: Dict[str, Dict[str, float]],
    start_location: Optional[str] = None,
    timeout_sec: float = 4.0
) -> TSPResult:
    """
    Branch and Bound TSP Solver with Minimum Outgoing Edge Lower Bounding.
    Prunes subtree whenever (current_cost + lower_bound) >= best_cost.
    """
    start_time = time.perf_counter_ns()
    n = len(locations)

    if n <= 1:
        elapsed = (time.perf_counter_ns() - start_time) / 1_000_000
        loc = locations[0] if n == 1 else ""
        return TSPResult(
            algorithm="Branch and Bound",
            is_feasible=True,
            num_locations=n,
            start_location=loc,
            optimal_tour=[loc] if n == 1 else [],
            total_tour_cost=0.0,
            states_explored=1,
            states_pruned=0,
            execution_time_ms=elapsed,
            timed_out=False,
            explanation="Trivial tour for small instance.",
            scalability_warning="No scalability concern for n <= 1."
        )

    start_loc = start_location if (start_location and start_location in locations) else locations[0]
    unvisited = [loc for loc in locations if loc != start_loc]

    # Precompute minimum outgoing edge from each vertex to valid targets
    min_outgoing: Dict[str, float] = {}
    for u in locations:
        min_w = math.inf
        for v in locations:
            if u != v:
                w = cost_matrix.get(u, {}).get(v, math.inf)
                if w < min_w:
                    min_w = w
        min_outgoing[u] = min_w

    best_cost: float = math.inf
    best_tour: List[str] = []
    states_explored: int = 0
    states_pruned: int = 0
    timed_out: bool = False

    time_limit_ns = int(timeout_sec * 1_000_000_000)
    deadline_ns = start_time + time_limit_ns

    def _calc_lower_bound(curr_loc: str, remaining: List[str]) -> float:
        """Computes lower bound for remaining unvisited nodes + return to start."""
        bound = 0.0
        # Edge leaving curr_loc
        bound += min_outgoing.get(curr_loc, 0.0)
        # Edges leaving each remaining node
        for u in remaining:
            bound += min_outgoing.get(u, 0.0)
        return bound

    def _branch_and_bound(curr_loc: str, current_cost: float, path: List[str], remaining: List[str]):
        nonlocal best_cost, best_tour, states_explored, states_pruned, timed_out

        states_explored += 1

        if time.perf_counter_ns() > deadline_ns:
            timed_out = True
            return

        if not remaining:
            return_cost = cost_matrix.get(curr_loc, {}).get(start_loc, math.inf)
            if return_cost != math.inf:
                total_cycle_cost = current_cost + return_cost
                if total_cycle_cost < best_cost:
                    best_cost = total_cycle_cost
                    best_tour = path + [start_loc]
            return

        # Compute Lower Bound
        bound = _calc_lower_bound(curr_loc, remaining)
        if current_cost + bound >= best_cost:
            states_pruned += 1
            return  # Prune search branch!

        # Branching: sort candidate successors by edge cost to find tighter bounds earlier
        candidates = []
        for i, next_loc in enumerate(remaining):
            edge_cost = cost_matrix.get(curr_loc, {}).get(next_loc, math.inf)
            if edge_cost != math.inf:
                candidates.append((edge_cost, next_loc, i))

        candidates.sort(key=lambda x: x[0])

        for edge_cost, next_loc, idx in candidates:
            next_remaining = remaining[:idx] + remaining[idx + 1:]
            _branch_and_bound(next_loc, current_cost + edge_cost, path + [next_loc], next_remaining)
            if timed_out:
                return

    _branch_and_bound(start_loc, 0.0, [start_loc], unvisited)

    elapsed = (time.perf_counter_ns() - start_time) / 1_000_000
    is_feasible = (best_cost != math.inf)

    warning = (
        f"Scalability Warning: While Branch and Bound aggressively prunes search subtrees using admissible lower bounds, "
        f"worst-case complexity remains exponential O((n-1)!). "
        "Bound pruning effectiveness depends on cost matrix structure and triangle inequality."
    )

    explanation = (
        f"Branch and Bound explored {states_explored} nodes and pruned {states_pruned} subtrees using minimum outgoing edge lower bounding. "
    )
    if timed_out:
        explanation += f"Reached timeout of {timeout_sec}s. Best tour captured before interruption."
    elif is_feasible:
        explanation += f"Proved exact minimum tour cost of {best_cost:.2f}."
    else:
        explanation += "No feasible tour exists for the provided graph structure."

    return TSPResult(
        algorithm="Branch and Bound",
        is_feasible=is_feasible,
        num_locations=n,
        start_location=start_loc,
        optimal_tour=best_tour if is_feasible else [],
        total_tour_cost=round(best_cost, 4) if is_feasible else None,
        states_explored=states_explored,
        states_pruned=states_pruned,
        execution_time_ms=elapsed,
        timed_out=timed_out,
        explanation=explanation,
        scalability_warning=warning
    )
