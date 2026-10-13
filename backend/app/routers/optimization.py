"""
Adaptive Network Design and Optimization Framework
Optimization Router: Module 5 (Budget Planner Knapsack) & Module 6 (Maintenance Route Planner TSP)
"""

import math
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException
from ..models.schemas import (
    KnapsackRequest,
    TSPRequest,
    ApiResponse
)
from ..algorithms.knapsack import (
    UpgradeProject,
    run_fractional_knapsack,
    run_01_knapsack
)
from ..algorithms.tsp import (
    solve_tsp_backtracking,
    solve_tsp_branch_and_bound
)
from ..algorithms.explanation_engine import generate_explanation

router = APIRouter(prefix="/api/optimization", tags=["Combinatorial Optimization"])


@router.post("/fractional-knapsack", response_model=ApiResponse)
def execute_fractional_knapsack(req: KnapsackRequest):
    """Executes Fractional Knapsack for divisible upgrade resources."""
    try:
        projects = [UpgradeProject(**p.dict()) for p in req.projects]
        result = run_fractional_knapsack(projects, req.budget)

        explanation = generate_explanation("module5_knapsack", {
            "budget": req.budget,
            "num_projects": len(projects),
            "is_divisible": True,
            "summary": f"Selected {result.num_projects_selected} projects/allocations yielding total benefit {result.total_benefit_gained:.2f}."
        })

        return ApiResponse(
            success=True,
            data={
                "result": result.dict(),
                "explanation": explanation.dict()
            },
            message="Fractional Knapsack executed successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/01-knapsack", response_model=ApiResponse)
def execute_01_knapsack(req: KnapsackRequest):
    """Executes 0/1 Knapsack Dynamic Programming for indivisible upgrades."""
    try:
        projects = [UpgradeProject(**p.dict()) for p in req.projects]
        result = run_01_knapsack(projects, req.budget)

        explanation = generate_explanation("module5_knapsack", {
            "budget": req.budget,
            "num_projects": len(projects),
            "is_divisible": False,
            "summary": f"Optimal 0/1 selection yielded total benefit {result.total_benefit_gained:.2f} spending ${result.total_cost_spent:,.2f}."
        })

        return ApiResponse(
            success=True,
            data={
                "result": result.dict(),
                "explanation": explanation.dict()
            },
            message="0/1 Knapsack DP executed successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/knapsack/compare", response_model=ApiResponse)
def compare_knapsack_models(req: KnapsackRequest):
    """Compares Fractional Greedy vs 0/1 Dynamic Programming on the same project set."""
    try:
        projects = [UpgradeProject(**p.dict()) for p in req.projects]
        fractional_res = run_fractional_knapsack(projects, req.budget)
        dp_res = run_01_knapsack(projects, req.budget)

        explanation = generate_explanation("module5_knapsack", {
            "budget": req.budget,
            "num_projects": len(projects),
            "is_divisible": False,
            "summary": (
                f"Fractional Benefit: {fractional_res.total_benefit_gained:.2f} (with resource slicing) vs "
                f"0/1 DP Benefit: {dp_res.total_benefit_gained:.2f} (discrete hardware units)."
            )
        })

        return ApiResponse(
            success=True,
            data={
                "fractional": fractional_res.dict(),
                "discrete_01": dp_res.dict(),
                "benefit_gap": round(fractional_res.total_benefit_gained - dp_res.total_benefit_gained, 4),
                "explanation": explanation.dict()
            },
            message="Knapsack divisibility comparison completed."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tsp/backtracking", response_model=ApiResponse)
def execute_tsp_backtracking(req: TSPRequest):
    """Executes Exact Backtracking TSP solver."""
    try:
        cost_matrix = req.cost_matrix or {}
        result = solve_tsp_backtracking(req.locations, cost_matrix, req.start_location, req.timeout_sec or 4.0)

        explanation = generate_explanation("module6_tsp", {
            "num_locations": len(req.locations),
            "summary": (
                f"Backtracking found tour of cost {result.total_tour_cost} in {result.execution_time_ms:.2f} ms "
                f"visiting {result.states_explored} states."
                if result.is_feasible else "Infeasible: No Hamiltonian tour found."
            )
        })

        return ApiResponse(
            success=True,
            data={
                "result": result.dict(),
                "explanation": explanation.dict()
            },
            message="TSP Backtracking executed successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tsp/branch-and-bound", response_model=ApiResponse)
def execute_tsp_branch_and_bound(req: TSPRequest):
    """Executes Branch and Bound TSP solver with lower bound state pruning."""
    try:
        cost_matrix = req.cost_matrix or {}
        result = solve_tsp_branch_and_bound(req.locations, cost_matrix, req.start_location, req.timeout_sec or 4.0)

        explanation = generate_explanation("module6_tsp", {
            "num_locations": len(req.locations),
            "summary": (
                f"Branch & Bound proved tour of cost {result.total_tour_cost} in {result.execution_time_ms:.2f} ms, "
                f"pruning {result.states_pruned} states."
                if result.is_feasible else "Infeasible: No Hamiltonian tour found."
            )
        })

        return ApiResponse(
            success=True,
            data={
                "result": result.dict(),
                "explanation": explanation.dict()
            },
            message="TSP Branch and Bound executed successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tsp/compare", response_model=ApiResponse)
def compare_tsp_solvers(req: TSPRequest):
    """Compares Backtracking and Branch and Bound on the same TSP instance."""
    try:
        cost_matrix = req.cost_matrix or {}
        n = len(req.locations)
        if n > 13:
            raise HTTPException(status_code=400, detail=f"Instance size n={n} exceeds exact search safety threshold (max n=13).")

        bt_res = solve_tsp_backtracking(req.locations, cost_matrix, req.start_location, req.timeout_sec or 4.0)
        bb_res = solve_tsp_branch_and_bound(req.locations, cost_matrix, req.start_location, req.timeout_sec or 4.0)

        cost_match = (
            bt_res.is_feasible == bb_res.is_feasible
            and (bt_res.total_tour_cost is None or abs((bt_res.total_tour_cost or 0) - (bb_res.total_tour_cost or 0)) < 1e-4)
        )

        explanation = generate_explanation("module6_tsp", {
            "num_locations": n,
            "summary": (
                f"Cost Agreement: {cost_match}. "
                f"Backtracking: {bt_res.states_explored} states in {bt_res.execution_time_ms:.2f} ms vs "
                f"Branch & Bound: {bb_res.states_explored} states ({bb_res.states_pruned} pruned) in {bb_res.execution_time_ms:.2f} ms."
            )
        })

        return ApiResponse(
            success=True,
            data={
                "num_locations": n,
                "cost_match": cost_match,
                "backtracking": bt_res.dict(),
                "branch_and_bound": bb_res.dict(),
                "pruning_ratio": round(bb_res.states_pruned / max(1, bb_res.states_explored + bb_res.states_pruned), 4),
                "speedup_factor": round(bt_res.execution_time_ms / max(0.001, bb_res.execution_time_ms), 2),
                "explanation": explanation.dict()
            },
            message="TSP solvers compared successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
