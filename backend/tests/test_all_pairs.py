"""
Tests for Module 2: Floyd-Warshall All-Pairs Shortest Path algorithm
"""

import pytest
from app.algorithms.all_pairs import run_floyd_warshall, reconstruct_path


def test_floyd_warshall_triangle():
    vertices = ["A", "B", "C"]
    edges = [
        ("A", "B", 5.0),
        ("B", "C", 3.0),
        ("A", "C", 10.0)  # Direct edge is 10, but multi-hop A->B->C is 8
    ]
    res = run_floyd_warshall(vertices, edges, is_directed=False)

    assert res.has_negative_cycle is False
    # Diagonal must be 0
    assert res.distance_matrix[0][0] == 0.0
    assert res.distance_matrix[1][1] == 0.0
    assert res.distance_matrix[2][2] == 0.0

    # A to C should be 8.0 via B
    assert res.distance_matrix[0][2] == 8.0
    assert res.distance_matrix[2][0] == 8.0

    # Path reconstruction
    path_res = reconstruct_path("A", "C", vertices, res.predecessor_matrix)
    assert path_res.is_reachable is True
    assert path_res.path == ["A", "B", "C"]


def test_floyd_warshall_unreachable():
    vertices = ["A", "B", "C"]
    edges = [("A", "B", 4.0)]  # C is isolated
    res = run_floyd_warshall(vertices, edges, is_directed=True)

    assert res.distance_matrix[0][1] == 4.0
    assert res.distance_matrix[0][2] is None  # Unreachable marked as None
    assert res.distance_matrix[2][0] is None

    path_res = reconstruct_path("A", "C", vertices, res.predecessor_matrix)
    assert path_res.is_reachable is False
    assert path_res.path == []


def test_floyd_warshall_negative_weights_safe():
    vertices = ["A", "B", "C"]
    edges = [
        ("A", "B", 4.0),
        ("B", "C", -2.0),
        ("A", "C", 5.0)
    ]
    res = run_floyd_warshall(vertices, edges, is_directed=True)

    assert res.has_negative_cycle is False
    # A to C: 4 + (-2) = 2.0
    assert res.distance_matrix[0][2] == 2.0


def test_floyd_warshall_negative_cycle_detection():
    vertices = ["A", "B"]
    edges = [
        ("A", "B", 2.0),
        ("B", "A", -3.0)  # Cycle A -> B -> A has weight -1
    ]
    res = run_floyd_warshall(vertices, edges, is_directed=True)

    assert res.has_negative_cycle is True
    assert "A" in res.negative_cycle_nodes or "B" in res.negative_cycle_nodes
