"""
Tests for Module 1: Prim and Kruskal Minimum Spanning Tree algorithms
"""

import pytest
from app.algorithms.mst import run_prim, run_kruskal, compare_prim_kruskal


def test_mst_single_vertex():
    vertices = ["A"]
    edges = []
    prim_res = run_prim(vertices, edges)
    kruskal_res = run_kruskal(vertices, edges)

    assert prim_res.is_connected is True
    assert prim_res.spanning_tree_exists is True
    assert prim_res.total_cost == 0.0
    assert prim_res.num_selected_edges == 0

    assert kruskal_res.is_connected is True
    assert kruskal_res.total_cost == 0.0
    assert kruskal_res.num_selected_edges == 0


def test_mst_connected_graph():
    # Canonical CLRS-style graph
    vertices = ["A", "B", "C", "D"]
    edges = [
        ("A", "B", 1.0),
        ("B", "C", 2.0),
        ("C", "D", 3.0),
        ("A", "D", 4.0),
        ("B", "D", 5.0)
    ]
    prim_res = run_prim(vertices, edges)
    kruskal_res = run_kruskal(vertices, edges)

    assert prim_res.spanning_tree_exists is True
    assert kruskal_res.spanning_tree_exists is True
    # Expected MST: A-B (1), B-C (2), C-D (3) -> Total Cost = 6.0
    assert prim_res.total_cost == 6.0
    assert kruskal_res.total_cost == 6.0
    assert prim_res.num_selected_edges == 3
    assert kruskal_res.num_selected_edges == 3


def test_mst_equal_edge_weights():
    vertices = ["A", "B", "C"]
    edges = [
        ("A", "B", 10.0),
        ("B", "C", 10.0),
        ("A", "C", 10.0)
    ]
    prim_res = run_prim(vertices, edges)
    kruskal_res = run_kruskal(vertices, edges)

    assert prim_res.total_cost == 20.0
    assert kruskal_res.total_cost == 20.0
    assert prim_res.num_selected_edges == 2
    assert kruskal_res.num_selected_edges == 2


def test_mst_disconnected_graph():
    vertices = ["A", "B", "C", "D"]
    edges = [
        ("A", "B", 1.0),
        ("C", "D", 2.0)
    ]
    prim_res = run_prim(vertices, edges)
    kruskal_res = run_kruskal(vertices, edges)

    # Disconnected graph must report no spanning tree exists
    assert prim_res.is_connected is False
    assert prim_res.spanning_tree_exists is False
    assert kruskal_res.is_connected is False
    assert kruskal_res.spanning_tree_exists is False


def test_mst_self_loops_and_duplicates():
    vertices = ["A", "B"]
    edges = [
        ("A", "A", 0.5),  # Self-loop
        ("A", "B", 5.0),
        ("A", "B", 3.0)   # Parallel edge
    ]
    prim_res = run_prim(vertices, edges)
    kruskal_res = run_kruskal(vertices, edges)

    assert prim_res.spanning_tree_exists is True
    assert kruskal_res.spanning_tree_exists is True
    # Should choose parallel edge with minimum weight 3.0
    assert prim_res.total_cost == 3.0
    assert kruskal_res.total_cost == 3.0
    assert prim_res.num_selected_edges == 1
    assert kruskal_res.num_selected_edges == 1


def test_compare_prim_kruskal():
    vertices = ["A", "B", "C", "D", "E"]
    edges = [
        ("A", "B", 4.0),
        ("A", "C", 2.0),
        ("B", "C", 1.0),
        ("B", "D", 5.0),
        ("C", "D", 8.0),
        ("C", "E", 10.0),
        ("D", "E", 2.0)
    ]
    comp = compare_prim_kruskal(vertices, edges)
    assert comp["cost_agreement"] is True
    assert comp["prim"]["total_cost"] == comp["kruskal"]["total_cost"]
    assert comp["prim"]["num_selected_edges"] == 4
