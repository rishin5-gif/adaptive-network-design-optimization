"""
Adaptive Network Design and Optimization Framework
Experiment Lab Router: Controlled High-Resolution Benchmarking & Export
Mandatory Families:
1. sparse_vs_dense_mst
2. floyd_warshall_scaling
3. tree_workloads
4. heap_workloads
5. knapsack_divisibility
6. tsp_scaling
"""

import time
import random
import statistics
import tracemalloc
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional
from fastapi import APIRouter, HTTPException, Response
from ..models.schemas import ExperimentRunRequest, ApiResponse
from ..algorithms.mst import run_prim, run_kruskal
from ..algorithms.all_pairs import run_floyd_warshall
from ..algorithms.btree import BTree, DeviceRecord
from ..algorithms.red_black_tree import RedBlackTree
from ..algorithms.binomial_heap import BinomialHeap, MaintenanceEvent
from ..algorithms.fibonacci_heap import FibonacciHeap
from ..algorithms.knapsack import UpgradeProject, run_fractional_knapsack, run_01_knapsack
from ..algorithms.tsp import solve_tsp_backtracking, solve_tsp_branch_and_bound
from ..database import save_experiment_run, get_recent_experiments

router = APIRouter(prefix="/api/experiments", tags=["Performance Experiment Lab"])


def _measure_memory(func, *args, **kwargs) -> Tuple[Any, str]:
    """Measures peak memory allocation using tracemalloc, or returns 'Not measured'."""
    try:
        tracemalloc.start()
        res = func(*args, **kwargs)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return res, f"{peak / 1024:.2f} KB"
    except Exception:
        return func(*args, **kwargs), "Not measured"


@router.post("/run", response_model=ApiResponse)
def run_experiment(req: ExperimentRunRequest):
    """Executes a benchmark experiment family across trials and records high-resolution metrics."""
    family = req.experiment_family
    trials = max(1, min(req.trials or 3, 10))
    params = req.params

    results_data: Dict[str, Any] = {}

    try:
        if family == "sparse_vs_dense_mst":
            sizes = params.get("sizes", [8, 16, 24, 32])
            series = []
            for n in sizes:
                # Generate sparse graph
                v_ids = [f"V{i}" for i in range(n)]
                sparse_edges = []
                for i in range(1, n):
                    sparse_edges.append((v_ids[i - 1], v_ids[i], round(random.uniform(5, 50), 1)))
                for _ in range(n // 2):
                    u, v = random.sample(v_ids, 2)
                    sparse_edges.append((u, v, round(random.uniform(5, 50), 1)))

                # Generate dense graph
                dense_edges = list(sparse_edges)
                all_possible = [(v_ids[i], v_ids[j]) for i in range(n) for j in range(i + 1, n)]
                random.shuffle(all_possible)
                target_e = int(0.7 * (n * (n - 1) // 2))
                for u, v in all_possible[:target_e]:
                    dense_edges.append((u, v, round(random.uniform(5, 50), 1)))

                # Time Prim on sparse & dense
                p_sparse_times = []
                k_sparse_times = []
                p_dense_times = []
                k_dense_times = []

                for _ in range(trials):
                    t0 = time.perf_counter_ns()
                    run_prim(v_ids, sparse_edges)
                    p_sparse_times.append((time.perf_counter_ns() - t0) / 1_000_000)

                    t0 = time.perf_counter_ns()
                    run_kruskal(v_ids, sparse_edges)
                    k_sparse_times.append((time.perf_counter_ns() - t0) / 1_000_000)

                    t0 = time.perf_counter_ns()
                    run_prim(v_ids, dense_edges)
                    p_dense_times.append((time.perf_counter_ns() - t0) / 1_000_000)

                    t0 = time.perf_counter_ns()
                    run_kruskal(v_ids, dense_edges)
                    k_dense_times.append((time.perf_counter_ns() - t0) / 1_000_000)

                series.append({
                    "num_vertices": n,
                    "sparse_edges_count": len(sparse_edges),
                    "dense_edges_count": len(dense_edges),
                    "prim_sparse_median_ms": round(statistics.median(p_sparse_times), 4),
                    "kruskal_sparse_median_ms": round(statistics.median(k_sparse_times), 4),
                    "prim_dense_median_ms": round(statistics.median(p_dense_times), 4),
                    "kruskal_dense_median_ms": round(statistics.median(k_dense_times), 4),
                })
            results_data = {"series": series, "trials": trials}

        elif family == "floyd_warshall_scaling":
            sizes = params.get("sizes", [5, 10, 15, 20, 25, 30])
            series = []
            for n in sizes:
                v_ids = [f"N{i}" for i in range(n)]
                edges = []
                for i in range(n):
                    for j in range(i + 1, n):
                        if random.random() < 0.6:
                            edges.append((v_ids[i], v_ids[j], round(random.uniform(5, 50), 1)))

                trial_times = []
                relaxations = 0
                for _ in range(trials):
                    t0 = time.perf_counter_ns()
                    res = run_floyd_warshall(v_ids, edges)
                    trial_times.append((time.perf_counter_ns() - t0) / 1_000_000)
                    relaxations = res.total_triplet_relaxations

                median_time = statistics.median(trial_times)
                theoretical_cube = n ** 3
                series.append({
                    "num_vertices": n,
                    "theoretical_v3": theoretical_cube,
                    "actual_triplet_relaxations": relaxations,
                    "median_time_ms": round(median_time, 4),
                    "mean_time_ms": round(statistics.mean(trial_times), 4),
                    "min_time_ms": round(min(trial_times), 4),
                    "max_time_ms": round(max(trial_times), 4)
                })
            results_data = {"series": series, "trials": trials}

        elif family == "tree_workloads":
            scales = params.get("scales", [50, 100, 200, 400])
            b_order = params.get("b_tree_order", 3)
            series = []
            for n in scales:
                keys = [f"DEV-{1000 + i}" for i in range(n)]
                random.shuffle(keys)
                records = [DeviceRecord(k, f"Dev-{k}", "HQ", "Router", "Active", {}) for k in keys]
                search_sample = random.sample(keys, min(n, 30))
                delete_sample = random.sample(keys, min(n // 4, 20))

                b_times = []
                r_times = []
                b_comps = 0
                r_comps = 0
                b_splits = 0
                r_rots = 0

                for _ in range(trials):
                    # B-Tree
                    btree = BTree(t=b_order)
                    t0 = time.perf_counter_ns()
                    for r in records:
                        btree.insert(r)
                    for k in search_sample:
                        btree.search(k)
                    for k in delete_sample:
                        btree.delete(k)
                    b_times.append((time.perf_counter_ns() - t0) / 1_000_000)
                    b_comps = btree.key_comparisons
                    b_splits = btree.splits_count

                    # RBT
                    rbt = RedBlackTree()
                    t0 = time.perf_counter_ns()
                    for r in records:
                        rbt.insert(r)
                    for k in search_sample:
                        rbt.search(k)
                    for k in delete_sample:
                        rbt.delete(k)
                    r_times.append((time.perf_counter_ns() - t0) / 1_000_000)
                    r_comps = rbt.key_comparisons
                    r_rots = rbt.left_rotations + rbt.right_rotations

                series.append({
                    "workload_size": n,
                    "btree_median_ms": round(statistics.median(b_times), 4),
                    "rbt_median_ms": round(statistics.median(r_times), 4),
                    "btree_comparisons": b_comps,
                    "rbt_comparisons": r_comps,
                    "btree_splits": b_splits,
                    "rbt_rotations": r_rots
                })
            results_data = {"series": series, "trials": trials, "b_tree_order": b_order}

        elif family == "heap_workloads":
            scales = params.get("scales", [20, 50, 100, 200])
            series = []
            for n in scales:
                events = [MaintenanceEvent(f"EVT-{i}", f"Desc {i}", random.randint(1, 100), "LOC", "") for i in range(n)]

                b_times = []
                f_times = []
                b_links = 0
                f_cuts = 0

                for _ in range(trials):
                    bh = BinomialHeap()
                    t0 = time.perf_counter_ns()
                    for e in events:
                        bh.insert(e)
                    for _ in range(min(n // 2, 15)):
                        bh.extract_min()
                    b_times.append((time.perf_counter_ns() - t0) / 1_000_000)
                    b_links = bh.links_count

                    fh = FibonacciHeap()
                    t0 = time.perf_counter_ns()
                    for e in events:
                        fh.insert(e)
                    for _ in range(min(n // 2, 15)):
                        fh.extract_min()
                    f_times.append((time.perf_counter_ns() - t0) / 1_000_000)
                    f_cuts = fh.cuts_count

                series.append({
                    "events_count": n,
                    "binomial_median_ms": round(statistics.median(b_times), 4),
                    "fibonacci_median_ms": round(statistics.median(f_times), 4),
                    "binomial_links": b_links,
                    "fibonacci_cuts": f_cuts
                })
            results_data = {"series": series, "trials": trials}

        elif family == "knapsack_divisibility":
            budgets = params.get("budgets", [20000, 50000, 80000, 120000])
            projects = [
                UpgradeProject(project_id="P1", project_name="Transceiver Stack", cost=30000, expected_benefit=70, divisibility="divisible"),
                UpgradeProject(project_id="P2", project_name="BGP Gateway", cost=40000, expected_benefit=85, divisibility="indivisible"),
                UpgradeProject(project_id="P3", project_name="Perimeter Firewall", cost=25000, expected_benefit=60, divisibility="indivisible"),
                UpgradeProject(project_id="P4", project_name="Optical Leased Fiber", cost=50000, expected_benefit=110, divisibility="divisible"),
                UpgradeProject(project_id="P5", project_name="Edge Server AI", cost=20000, expected_benefit=45, divisibility="indivisible"),
                UpgradeProject(project_id="P6", project_name="Transit Bandwidth", cost=15000, expected_benefit=35, divisibility="divisible")
            ]
            series = []
            for b in budgets:
                frac = run_fractional_knapsack(projects, b)
                dp = run_01_knapsack(projects, b)
                series.append({
                    "budget": b,
                    "fractional_benefit": frac.total_benefit_gained,
                    "fractional_cost_spent": frac.total_cost_spent,
                    "dp_benefit": dp.total_benefit_gained,
                    "dp_cost_spent": dp.total_cost_spent,
                    "benefit_gap": round(frac.total_benefit_gained - dp.total_benefit_gained, 2)
                })
            results_data = {"series": series}

        elif family == "tsp_scaling":
            sizes = params.get("sizes", [4, 5, 6, 7, 8])
            series = []
            for n in sizes:
                locs = [f"Site-{i}" for i in range(n)]
                matrix: Dict[str, Dict[str, float]] = {u: {} for u in locs}
                # Create symmetric metric TSP matrix
                coords = {u: (random.randint(10, 100), random.randint(10, 100)) for u in locs}
                for u in locs:
                    for v in locs:
                        if u == v:
                            matrix[u][v] = 0.0
                        else:
                            dx = coords[u][0] - coords[v][0]
                            dy = coords[u][1] - coords[v][1]
                            dist = round((dx**2 + dy**2)**0.5, 2)
                            matrix[u][v] = dist

                bt_times = []
                bb_times = []
                bt_res = None
                bb_res = None

                for _ in range(trials):
                    t0 = time.perf_counter_ns()
                    bt_res = solve_tsp_backtracking(locs, matrix, locs[0])
                    bt_times.append((time.perf_counter_ns() - t0) / 1_000_000)

                    t0 = time.perf_counter_ns()
                    bb_res = solve_tsp_branch_and_bound(locs, matrix, locs[0])
                    bb_times.append((time.perf_counter_ns() - t0) / 1_000_000)

                series.append({
                    "num_locations": n,
                    "theoretical_permutations": math.factorial(n - 1) if n > 1 else 1,
                    "bt_median_ms": round(statistics.median(bt_times), 4),
                    "bb_median_ms": round(statistics.median(bb_times), 4),
                    "bt_states_explored": bt_res.states_explored if bt_res else 0,
                    "bb_states_explored": bb_res.states_explored if bb_res else 0,
                    "bb_states_pruned": bb_res.states_pruned if bb_res else 0,
                    "optimal_tour_cost": bb_res.total_tour_cost if bb_res else None
                })
            results_data = {"series": series, "trials": trials}

        else:
            raise HTTPException(status_code=400, detail=f"Unknown experiment family: {family}")

        timestamp = datetime.utcnow().isoformat()
        save_experiment_run(family, params, results_data, timestamp)

        return ApiResponse(
            success=True,
            data={
                "experiment_family": family,
                "timestamp": timestamp,
                "results": results_data
            },
            message=f"Experiment '{family}' executed successfully."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Experiment execution failed: {str(e)}")


@router.get("/history", response_model=ApiResponse)
def list_experiment_history():
    """Lists saved experiment runs from database."""
    runs = get_recent_experiments()
    return ApiResponse(
        success=True,
        data={"runs": runs, "count": len(runs)},
        message="Retrieved experiment history."
    )


@router.get("/export")
def export_experiments_csv(family: Optional[str] = None):
    """Exports benchmark results in CSV format."""
    runs = get_recent_experiments(limit=50)
    if family:
        runs = [r for r in runs if r["experiment_family"] == family]

    lines = ["id,family,timestamp,data_points,summary"]
    for r in runs:
        s_count = len(r["results"].get("series", []))
        summary = f"{s_count} data points"
        lines.append(f"{r['id']},{r['experiment_family']},{r['execution_timestamp']},{s_count},\"{summary}\"")

    csv_content = "\n".join(lines)
    return Response(content=csv_content, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=experiments_results.csv"})
