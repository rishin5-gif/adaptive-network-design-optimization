"""
Tests for Module 6: Exact Backtracking and Branch & Bound TSP solvers
"""

import pytest
import math
from app.algorithms.tsp import (
    solve_tsp_backtracking,
    solve_tsp_branch_and_bound
)


def test_tsp_4_cities_known_optimal():
    # Symmetric 4-city cost matrix
    locations = ["A", "B", "C", "D"]
    matrix = {
        "A": {"A": 0.0, "B": 10.0, "C": 15.0, "D": 20.0},
        "B": {"A": 10.0, "B": 0.0, "C": 35.0, "D": 25.0},
        "C": {"A": 15.0, "B": 35.0, "C": 0.0, "D": 30.0},
        "D": {"A": 20.0, "B": 25.0, "C": 30.0, "D": 0.0}
    }
    # Tours:
    # A -> B -> D -> C -> A = 10 + 25 + 30 + 15 = 80.0
    # A -> B -> C -> D -> A = 10 + 35 + 30 + 20 = 95.0
    # A -> C -> B -> D -> A = 15 + 35 + 25 + 20 = 95.0
    # Minimum tour cost is 80.0

    bt_res = solve_tsp_backtracking(locations, matrix, "A")
    bb_res = solve_tsp_branch_and_bound(locations, matrix, "A")

    assert bt_res.is_feasible is True
    assert bb_res.is_feasible is True
    assert bt_res.total_tour_cost == 80.0
    assert bb_res.total_tour_cost == 80.0
    assert bt_res.total_tour_cost == bb_res.total_tour_cost

    # Both tours must start and end at "A" and visit all 4 locations
    assert bt_res.optimal_tour[0] == "A"
    assert bt_res.optimal_tour[-1] == "A"
    assert len(set(bt_res.optimal_tour[:-1])) == 4

    assert bb_res.optimal_tour[0] == "A"
    assert bb_res.optimal_tour[-1] == "A"
    assert len(set(bb_res.optimal_tour[:-1])) == 4


def test_tsp_branch_and_bound_pruning():
    locations = ["A", "B", "C", "D", "E"]
    # Fully connected metric matrix
    coords = {"A": (0, 0), "B": (10, 0), "C": (10, 10), "D": (0, 10), "E": (5, 5)}
    matrix = {u: {} for u in locations}
    for u in locations:
        for v in locations:
            matrix[u][v] = round(((coords[u][0] - coords[v][0])**2 + (coords[u][1] - coords[v][1])**2)**0.5, 2)

    bt_res = solve_tsp_backtracking(locations, matrix, "A")
    bb_res = solve_tsp_branch_and_bound(locations, matrix, "A")

    assert bt_res.is_feasible is True
    assert bb_res.is_feasible is True
    assert abs(bt_res.total_tour_cost - bb_res.total_tour_cost) < 1e-3
    # Branch and bound must have pruned states
    assert bb_res.states_pruned >= 0


def test_tsp_infeasible_disconnected():
    locations = ["A", "B", "C"]
    # No path between B and C
    matrix = {
        "A": {"A": 0.0, "B": 5.0, "C": math.inf},
        "B": {"A": 5.0, "B": 0.0, "C": math.inf},
        "C": {"A": math.inf, "B": math.inf, "C": 0.0}
    }
    bt_res = solve_tsp_backtracking(locations, matrix, "A")
    bb_res = solve_tsp_branch_and_bound(locations, matrix, "A")

    assert bt_res.is_feasible is False
    assert bb_res.is_feasible is False
    assert bt_res.total_tour_cost is None
    assert bb_res.total_tour_cost is None
