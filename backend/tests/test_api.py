"""
Tests for FastAPI Backend API Endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"


def test_api_dashboard_summary():
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "num_locations" in data["data"]
    assert "mst_cost" in data["data"]


def test_api_network():
    response = client.get("/api/network")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["vertices"]) >= 8
    assert len(data["data"]["edges"]) >= 10


def test_api_mst_prim_and_kruskal():
    req_payload = {
        "vertices": ["A", "B", "C"],
        "edges": [["A", "B", 10.0], ["B", "C", 20.0], ["A", "C", 30.0]]
    }
    # Prim
    p_res = client.post("/api/algorithms/prim", json=req_payload)
    assert p_res.status_code == 200
    assert p_res.json()["data"]["result"]["total_cost"] == 30.0

    # Kruskal
    k_res = client.post("/api/algorithms/kruskal", json=req_payload)
    assert k_res.status_code == 200
    assert k_res.json()["data"]["result"]["total_cost"] == 30.0


def test_api_floyd_warshall():
    req_payload = {
        "vertices": ["A", "B", "C"],
        "edges": [["A", "B", 2.0], ["B", "C", 3.0]],
        "is_directed": False
    }
    response = client.post("/api/algorithms/floyd-warshall", json=req_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["result"]["distance_matrix"][0][2] == 5.0


def test_api_knapsack():
    req_payload = {
        "projects": [
            {"project_id": "P1", "project_name": "Switch", "cost": 10.0, "expected_benefit": 50.0},
            {"project_id": "P2", "project_name": "Router", "cost": 20.0, "expected_benefit": 60.0}
        ],
        "budget": 20.0
    }
    res_frac = client.post("/api/optimization/fractional-knapsack", json=req_payload)
    assert res_frac.status_code == 200
    assert res_frac.json()["data"]["result"]["total_benefit_gained"] == 80.0

    res_dp = client.post("/api/optimization/01-knapsack", json=req_payload)
    assert res_dp.status_code == 200
    assert res_dp.json()["data"]["result"]["total_benefit_gained"] == 60.0


def test_api_experiment_run():
    req_payload = {
        "experiment_family": "sparse_vs_dense_mst",
        "params": {"sizes": [4, 6]},
        "trials": 1
    }
    response = client.post("/api/experiments/run", json=req_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["results"]["series"]) == 2
