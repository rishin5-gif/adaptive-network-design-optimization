"""
Adaptive Network Design and Optimization Framework
Module 5: Network Upgrade Budget Planner
Algorithms:
1. Fractional Knapsack (Greedy - O(n log n))
2. 0/1 Knapsack (Dynamic Programming - O(nW))
"""

import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class UpgradeProject(BaseModel):
    project_id: str
    project_name: str
    cost: float  # Weight/Resource required
    expected_benefit: float  # Value
    divisibility: str = "indivisible"  # "divisible" or "indivisible"


class SelectedProjectAllocation(BaseModel):
    project_id: str
    project_name: str
    original_cost: float
    original_benefit: float
    allocated_fraction: float
    allocated_cost: float
    allocated_benefit: float
    benefit_to_cost_ratio: float


class KnapsackResult(BaseModel):
    algorithm: str
    total_budget: float
    total_cost_spent: float
    total_benefit_gained: float
    remaining_budget: float
    num_projects_considered: int
    num_projects_selected: int
    allocations: List[SelectedProjectAllocation]
    execution_time_ms: float
    complexity_time: str
    complexity_space: str
    is_optimal: bool
    selection_reason: str
    counterexample_note: Optional[str] = None


def run_fractional_knapsack(
    projects: List[UpgradeProject],
    budget: float
) -> KnapsackResult:
    """
    Solves Fractional Knapsack using Greedy approach.
    Sorts projects by benefit/cost ratio in descending order.
    Complexity: O(n log n) time, O(n) space.
    """
    start_time = time.perf_counter_ns()

    if budget < 0:
        raise ValueError("Budget capacity cannot be negative.")

    # Filter and validate items
    valid_projects = []
    zero_cost_projects = []
    for p in projects:
        if p.cost < 0 or p.expected_benefit < 0:
            raise ValueError(f"Project {p.project_id} has negative cost or benefit.")
        if p.cost == 0:
            zero_cost_projects.append(p)
        else:
            valid_projects.append(p)

    allocations: List[SelectedProjectAllocation] = []
    total_cost: float = 0.0
    total_benefit: float = 0.0

    # 1. Take all zero-cost positive benefit projects
    for zp in zero_cost_projects:
        allocations.append(SelectedProjectAllocation(
            project_id=zp.project_id,
            project_name=zp.project_name,
            original_cost=0.0,
            original_benefit=zp.expected_benefit,
            allocated_fraction=1.0,
            allocated_cost=0.0,
            allocated_benefit=zp.expected_benefit,
            benefit_to_cost_ratio=float('inf')
        ))
        total_benefit += zp.expected_benefit

    # 2. Sort remaining by benefit-to-cost ratio descending
    sorted_projects = sorted(
        valid_projects,
        key=lambda p: (p.expected_benefit / p.cost),
        reverse=True
    )

    remaining_budget = budget - total_cost

    for p in sorted_projects:
        if remaining_budget <= 1e-9:
            break

        ratio = p.expected_benefit / p.cost

        if p.cost <= remaining_budget:
            # Take whole project
            fraction = 1.0
            cost_take = p.cost
            benefit_take = p.expected_benefit
        else:
            # Take fraction
            fraction = remaining_budget / p.cost
            cost_take = remaining_budget
            benefit_take = p.expected_benefit * fraction

        allocations.append(SelectedProjectAllocation(
            project_id=p.project_id,
            project_name=p.project_name,
            original_cost=p.cost,
            original_benefit=p.expected_benefit,
            allocated_fraction=round(fraction, 4),
            allocated_cost=round(cost_take, 4),
            allocated_benefit=round(benefit_take, 4),
            benefit_to_cost_ratio=round(ratio, 4)
        ))

        total_cost += cost_take
        total_benefit += benefit_take
        remaining_budget -= cost_take

    elapsed_ms = (time.perf_counter_ns() - start_time) / 1_000_000

    return KnapsackResult(
        algorithm="Fractional Knapsack (Greedy)",
        total_budget=round(budget, 4),
        total_cost_spent=round(total_cost, 4),
        total_benefit_gained=round(total_benefit, 4),
        remaining_budget=round(max(0.0, budget - total_cost), 4),
        num_projects_considered=len(projects),
        num_projects_selected=len(allocations),
        allocations=allocations,
        execution_time_ms=elapsed_ms,
        complexity_time="O(n log n)",
        complexity_space="O(n)",
        is_optimal=True,
        selection_reason=(
            "Fractional Knapsack exhibits the greedy-choice property. "
            "Because resources (e.g. bandwidth slices, cloud compute hours) can be divided, "
            "prioritizing highest benefit-per-cost ratio strictly maximizes overall objective."
        )
    )


def run_01_knapsack(
    projects: List[UpgradeProject],
    budget: float,
    scale_factor: int = 1
) -> KnapsackResult:
    """
    Solves 0/1 Knapsack using Dynamic Programming.
    Guarantees global optimum for indivisible assets.
    Complexity: O(n * W) time, O(n * W) space.
    """
    start_time = time.perf_counter_ns()

    if budget < 0:
        raise ValueError("Budget capacity cannot be negative.")

    # Validate inputs
    for p in projects:
        if p.cost < 0 or p.expected_benefit < 0:
            raise ValueError(f"Project {p.project_id} has negative cost or benefit.")

    # Scale costs to integer units for canonical DP grid
    # If costs have decimals, scale_factor can be 10 or 100
    W_int = int(round(budget * scale_factor))
    n = len(projects)

    # Free items handling
    free_items = [p for p in projects if p.cost == 0]
    paid_items = [p for p in projects if p.cost > 0]
    n_paid = len(paid_items)

    int_costs = [int(round(p.cost * scale_factor)) for p in paid_items]
    values = [p.expected_benefit for p in paid_items]

    # DP Table: (n_paid + 1) x (W_int + 1)
    dp: List[List[float]] = [[0.0] * (W_int + 1) for _ in range(n_paid + 1)]

    for i in range(1, n_paid + 1):
        c_i = int_costs[i - 1]
        v_i = values[i - 1]
        for w in range(W_int + 1):
            # Option 1: Don't take item i
            dp[i][w] = dp[i - 1][w]
            # Option 2: Take item i if capacity permits
            if c_i <= w:
                candidate = dp[i - 1][w - c_i] + v_i
                if candidate > dp[i][w]:
                    dp[i][w] = candidate

    # Backtrack to find selected items
    selected_indices = []
    w_curr = W_int
    for i in range(n_paid, 0, -1):
        if dp[i][w_curr] != dp[i - 1][w_curr]:
            selected_indices.append(i - 1)
            w_curr -= int_costs[i - 1]

    selected_indices.reverse()

    allocations: List[SelectedProjectAllocation] = []
    total_cost = 0.0
    total_benefit = 0.0

    # Include free items first
    for fp in free_items:
        allocations.append(SelectedProjectAllocation(
            project_id=fp.project_id,
            project_name=fp.project_name,
            original_cost=0.0,
            original_benefit=fp.expected_benefit,
            allocated_fraction=1.0,
            allocated_cost=0.0,
            allocated_benefit=fp.expected_benefit,
            benefit_to_cost_ratio=float('inf')
        ))
        total_benefit += fp.expected_benefit

    # Include DP selected items
    for idx in selected_indices:
        p = paid_items[idx]
        ratio = p.expected_benefit / p.cost if p.cost > 0 else float('inf')
        allocations.append(SelectedProjectAllocation(
            project_id=p.project_id,
            project_name=p.project_name,
            original_cost=p.cost,
            original_benefit=p.expected_benefit,
            allocated_fraction=1.0,
            allocated_cost=p.cost,
            allocated_benefit=p.expected_benefit,
            benefit_to_cost_ratio=round(ratio, 4)
        ))
        total_cost += p.cost
        total_benefit += p.expected_benefit

    elapsed_ms = (time.perf_counter_ns() - start_time) / 1_000_000

    counterexample = (
        "Note on Greedy vs 0/1 DP: A greedy strategy fails for indivisible items. "
        "For instance, with Budget=50 and items: A(w=10, v=60, ratio=6), B(w=20, v=100, ratio=5), C(w=30, v=120, ratio=4). "
        "Greedy takes A and B (cost=30, value=160), but the optimal 0/1 DP selection is B and C (cost=50, value=220)!"
    )

    return KnapsackResult(
        algorithm="0/1 Knapsack (Dynamic Programming)",
        total_budget=round(budget, 4),
        total_cost_spent=round(total_cost, 4),
        total_benefit_gained=round(total_benefit, 4),
        remaining_budget=round(max(0.0, budget - total_cost), 4),
        num_projects_considered=len(projects),
        num_projects_selected=len(allocations),
        allocations=allocations,
        execution_time_ms=elapsed_ms,
        complexity_time=f"O(n * W) = O({n} * {W_int}) operations",
        complexity_space="O(n * W)",
        is_optimal=True,
        selection_reason=(
            "0/1 Knapsack enforces discrete all-or-nothing purchase of network hardware (routers, switches). "
            "Dynamic programming guarantees the exact global optimum via optimal substructure and overlapping subproblems."
        ),
        counterexample_note=counterexample
    )
