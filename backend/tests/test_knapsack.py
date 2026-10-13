"""
Tests for Module 5: Fractional Knapsack and 0/1 Knapsack algorithms
"""

import pytest
from app.algorithms.knapsack import (
    UpgradeProject,
    run_fractional_knapsack,
    run_01_knapsack
)


def test_knapsack_zero_budget():
    projects = [UpgradeProject(project_id="P1", project_name="Switch", cost=100.0, expected_benefit=50.0)]
    frac_res = run_fractional_knapsack(projects, 0.0)
    dp_res = run_01_knapsack(projects, 0.0)

    assert frac_res.total_benefit_gained == 0.0
    assert frac_res.num_projects_selected == 0
    assert dp_res.total_benefit_gained == 0.0
    assert dp_res.num_projects_selected == 0


def test_knapsack_fractional_allocation():
    # Item 1: cost 10, value 60 (ratio 6)
    # Item 2: cost 20, value 100 (ratio 5)
    # Budget: 25 -> Takes item 1 full (cost 10, val 60) and 15/20 of item 2 (cost 15, val 75) -> total val 135
    projects = [
        UpgradeProject(project_id="P1", project_name="A", cost=10.0, expected_benefit=60.0),
        UpgradeProject(project_id="P2", project_name="B", cost=20.0, expected_benefit=100.0)
    ]
    res = run_fractional_knapsack(projects, 25.0)

    assert res.total_cost_spent == 25.0
    assert res.total_benefit_gained == 135.0
    assert res.remaining_budget == 0.0
    assert len(res.allocations) == 2
    assert res.allocations[0].allocated_fraction == 1.0
    assert res.allocations[1].allocated_fraction == 0.75


def test_01_knapsack_counterexample_where_greedy_fails():
    """
    Counterexample proving greedy fails for 0/1 Knapsack:
    Capacity W = 50
    Item 1: cost 10, value 60 (ratio 6)
    Item 2: cost 20, value 100 (ratio 5)
    Item 3: cost 30, value 120 (ratio 4)
    Greedy takes Item 1 & 2 -> cost 30, value 160 (cannot fit item 3).
    Optimal 0/1 takes Item 2 & 3 -> cost 50, value 220!
    """
    projects = [
        UpgradeProject(project_id="P1", project_name="Item 1", cost=10.0, expected_benefit=60.0),
        UpgradeProject(project_id="P2", project_name="Item 2", cost=20.0, expected_benefit=100.0),
        UpgradeProject(project_id="P3", project_name="Item 3", cost=30.0, expected_benefit=120.0)
    ]
    dp_res = run_01_knapsack(projects, 50.0)

    # 0/1 DP must find optimal value 220
    assert dp_res.total_benefit_gained == 220.0
    assert dp_res.total_cost_spent == 50.0
    selected_ids = {a.project_id for a in dp_res.allocations}
    assert selected_ids == {"P2", "P3"}


def test_knapsack_negative_budget_or_weights_rejected():
    projects = [UpgradeProject(project_id="P1", project_name="Invalid", cost=-5.0, expected_benefit=10.0)]
    with pytest.raises(ValueError):
        run_fractional_knapsack(projects, 100.0)

    with pytest.raises(ValueError):
        run_01_knapsack(projects, 100.0)

    with pytest.raises(ValueError):
        run_fractional_knapsack([], -10.0)
