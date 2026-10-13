"""
Adaptive Network Design and Optimization Framework
Integrated Decision and Explanation Engine
Provides transparent rule-based algorithm selection, analytical justifications,
theoretical vs empirical trade-offs, and structured explanations across all 6 modules.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel


class AlgorithmExplanation(BaseModel):
    module_name: str
    real_world_question: str
    mathematical_formulation: str
    input_properties: Dict[str, Any]
    selected_algorithm: str
    alternative_considered: str
    selection_reason: str
    expected_time_complexity: str
    expected_space_complexity: str
    correctness_assumptions: str
    actual_result_summary: str
    limitations_and_warnings: str


def generate_explanation(
    module_name: str,
    context: Dict[str, Any]
) -> AlgorithmExplanation:
    """
    Evaluates runtime context and produces a structured 11-point DAA explanation.
    """
    if module_name == "module1_mst":
        density = context.get("density", 0.3)
        num_v = context.get("num_vertices", 10)
        num_e = context.get("num_edges", 15)
        selected_algo = "Prim's Algorithm" if density > 0.5 else "Kruskal's Algorithm"
        alt_algo = "Kruskal's Algorithm" if selected_algo == "Prim's Algorithm" else "Prim's Algorithm"
        
        reason = (
            f"The network has {num_v} vertices, {num_e} links, and a graph density of {density:.2f}. "
            + ("With high density (E ≈ V²), Prim's adjacency-based min-heap operates efficiently in O(E + V log V). "
               if density > 0.5 else
               "With low density (E ≪ V²), Kruskal's edge sorting with Disjoint-Set Union operates in O(E log E) with minimal overhead.")
        )
        return AlgorithmExplanation(
            module_name="Module 1: Network Design & MST",
            real_world_question="How can we interconnect all network locations with fiber cables at the absolute minimum total infrastructure deployment cost?",
            mathematical_formulation="Given an undirected weighted graph G = (V, E, w) where w: E -> R+, find an acyclic subgraph T = (V, E_T) spanning all vertices that minimizes sum_{e in E_T} w(e).",
            input_properties={"vertices": num_v, "edges": num_e, "density": round(density, 3), "is_dense": density > 0.5},
            selected_algorithm=selected_algo,
            alternative_considered=alt_algo,
            selection_reason=reason,
            expected_time_complexity="Prim: O((V + E) log V) | Kruskal: O(E log E)",
            expected_space_complexity="Prim: O(V + E) [Adjacency List + Heap] | Kruskal: O(V + E) [Edge List + DSU Arrays]",
            correctness_assumptions="Graph G must be connected and undirected with non-negative edge weights. A disconnected graph yields a forest rather than a spanning tree.",
            actual_result_summary=context.get("summary", "Optimal minimum spanning tree identified spanning all vertices."),
            limitations_and_warnings="MST assumes direct point-to-point links can be installed between any adjacent pair without path redundancy or multi-commodity capacity bottlenecks."
        )

    elif module_name == "module2_all_pairs":
        num_v = context.get("num_vertices", 10)
        has_neg = context.get("has_negative_weights", False)
        return AlgorithmExplanation(
            module_name="Module 2: All-Pairs Communication Cost Analysis",
            real_world_question="What is the lowest latency and transit cost between every pair of sites for network routing tables and SLA latency verification?",
            mathematical_formulation="For directed/undirected graph G = (V, E, w), compute distance matrix D where D[i][j] = min path weight from i to j using recurrence D^{(k)}[i][j] = min(D^{(k-1)}[i][j], D^{(k-1)}[i][k] + D^{(k-1)}[k][j]).",
            input_properties={"vertices": num_v, "has_negative_weights": has_neg, "intermediate_steps": num_v},
            selected_algorithm="Floyd-Warshall Dynamic Programming",
            alternative_considered="Johnson's Algorithm or Running Dijkstra V times",
            selection_reason="Floyd-Warshall operates in an elegant 3-loop dynamic programming structure with O(V^2) space, easily supports negative link costs, and detects negative-weight feedback cycles.",
            expected_time_complexity="O(V^3)",
            expected_space_complexity="O(V^2)",
            correctness_assumptions="Graph contains no negative-weight cycles. If D[i][i] < 0 after completion, a negative cycle exists and shortest paths are undefined.",
            actual_result_summary=context.get("summary", f"Computed complete {num_v}x{num_v} communication cost matrix."),
            limitations_and_warnings="Cubic time complexity O(V^3) scales poorly for massive graphs (V > 1,000 nodes). For sparse networks without negative edges, V x Dijkstra is asymptotically faster."
        )

    elif module_name == "module3_records":
        workload = context.get("workload_type", "balanced")
        b_degree = context.get("b_tree_order", 3)
        return AlgorithmExplanation(
            module_name="Module 3: Network Record Management",
            real_world_question="How should network hardware inventories (switches, routers, firewalls) be indexed for fast searches, concurrent updates, and storage efficiency?",
            mathematical_formulation="Balanced search tree maintaining ordered keys with worst-case search, insertion, and deletion bounded by O(log n).",
            input_properties={"b_tree_degree": b_degree, "workload": workload, "target_invariants": "Height balance & strict key ordering"},
            selected_algorithm="B-Tree (order t) vs Red-Black Tree",
            alternative_considered="AVL Trees or Hash Tables",
            selection_reason=(
                f"B-Tree (t={b_degree}) optimizes I/O by storing multiple keys per node, maximizing cache-line and disk block utilization. "
                "Red-Black Tree provides strict binary balance with at most 3 rotations per insertion/deletion, ideal for in-memory pointer lookups."
            ),
            expected_time_complexity="B-Tree: O(log_t n) | Red-Black Tree: O(log_2 n)",
            expected_space_complexity="O(n) for both structures",
            correctness_assumptions="Device IDs are unique and totally ordered. Structural invariants (uniform leaf depth in B-Tree; uniform black-height and no double-red in RBT) must hold after every operation.",
            actual_result_summary=context.get("summary", "Both structures verified invariant integrity and completed workloads."),
            limitations_and_warnings="In-memory pointer trees incur pointer overhead. For millions of pure exact-match lookups without range queries, hash tables provide O(1) average lookup."
        )

    elif module_name == "module4_heaps":
        num_events = context.get("num_events", 8)
        dec_key_freq = context.get("decrease_key_frequency", "high")
        return AlgorithmExplanation(
            module_name="Module 4: Maintenance Event Prioritization",
            real_world_question="How should network outages and hardware alert tickets be prioritized so engineers always address the highest-urgency emergency first?",
            mathematical_formulation="Priority Queue data structure maintaining min-priority key invariant with operations: Insert, Find-Min, Extract-Min, Union, Decrease-Key.",
            input_properties={"events_count": num_events, "decrease_key_frequency": dec_key_freq, "urgency_convention": "Lower value = higher urgency"},
            selected_algorithm="Fibonacci Heap vs Binomial Heap",
            alternative_considered="Binary Min-Heap or Pairing Heap",
            selection_reason=(
                "Fibonacci Heap provides theoretical O(1) amortized decrease-key and insert operations via lazy consolidation and cascading cuts. "
                "Binomial Heap provides strict worst-case O(log n) guarantees across all operations without complex amortized potential tracking."
            ),
            expected_time_complexity="Binomial: O(log n) all ops | Fibonacci: O(1) amortized Insert/Decrease-Key, O(log n) Extract-Min",
            expected_space_complexity="O(n) node pointers",
            correctness_assumptions="Priorities are numeric and updates only decrease values (escalating urgency). Extract-min must always retrieve the global minimum.",
            actual_result_summary=context.get("summary", "Heaps maintained correct priority ordering and extracted highest urgency events."),
            limitations_and_warnings="Fibonacci Heap has higher constant-factor pointer manipulation overhead. For small n, Binary or Binomial Heaps often outperform Fibonacci Heap in measured wall-clock time."
        )

    elif module_name == "module5_knapsack":
        divisible = context.get("is_divisible", False)
        budget = context.get("budget", 100000)
        n = context.get("num_projects", 6)
        if divisible:
            selected = "Fractional Knapsack (Greedy)"
            alt = "0/1 Knapsack Dynamic Programming"
            reason = "Upgrade resources (e.g. bandwidth allocations, leased optical spectrum) are divisible. The greedy choice property guarantees optimal total value by sorting ratio v_i / w_i."
            time_comp = "O(n log n)"
            space_comp = "O(n)"
        else:
            selected = "0/1 Knapsack (Dynamic Programming)"
            alt = "Greedy Ratio Approximation or Branch-and-Bound"
            reason = "Physical equipment upgrades (routers, redundant UPS units) are indivisible. Greedy heuristics fail to guarantee optimality. Dynamic programming evaluates optimal subproblems exactly."
            time_comp = f"O(n * W) pseudo-polynomial"
            space_comp = "O(n * W)"

        return AlgorithmExplanation(
            module_name="Module 5: Network Upgrade Budget Planner",
            real_world_question="Given a fixed capital expenditure (CapEx) budget, which combination of network upgrade projects yields the maximum reliability and capacity benefit?",
            mathematical_formulation=f"Maximize sum(v_i * x_i) subject to sum(w_i * x_i) <= W, where x_i in {'[0, 1]' if divisible else '{0, 1}'}.",
            input_properties={"budget": budget, "num_projects": n, "divisible": divisible},
            selected_algorithm=selected,
            alternative_considered=alt,
            selection_reason=reason,
            expected_time_complexity=time_comp,
            expected_space_complexity=space_comp,
            correctness_assumptions="Project costs and benefits are non-negative. Budget is non-negative.",
            actual_result_summary=context.get("summary", "Computed globally optimal allocation within budget constraints."),
            limitations_and_warnings="0/1 Knapsack DP is pseudo-polynomial in capacity W. If budget W is astronomical with many decimal digits, polynomial time is not guaranteed without scaling or FPTAS."
        )

    elif module_name == "module6_tsp":
        n = context.get("num_locations", 5)
        selected = "Branch and Bound" if n >= 6 else "Exact Backtracking"
        alt = "Exact Backtracking" if selected == "Branch and Bound" else "Branch and Bound"
        return AlgorithmExplanation(
            module_name="Module 6: Maintenance Route Planner (TSP)",
            real_world_question="What is the cheapest inspection route for a field technician to visit all maintenance locations exactly once and return to the headquarters depot?",
            mathematical_formulation="Find a Hamiltonian cycle of minimum total weight in complete/connected weighted graph G = (V, E, c): min sum_{(u, v) in Cycle} c(u, v).",
            input_properties={"locations_count": n, "theoretical_permutations": "O((n-1)!)", "instance_size": "Small exact instance"},
            selected_algorithm=selected,
            alternative_considered=alt,
            selection_reason=(
                f"For n={n}, Branch and Bound utilizes minimum outgoing edge lower bounding to prune inferior search subtrees early, "
                "substantially outperforming exhaustive backtracking on non-trivial topologies."
            ),
            expected_time_complexity="Worst-case: O((n-1)!) | Pruned: Sub-exponential depending on bound sharpness",
            expected_space_complexity="O(n) recursion stack & state representation",
            correctness_assumptions="Graph contains a valid Hamiltonian cycle. Tour must visit each selected vertex exactly once before returning to depot.",
            actual_result_summary=context.get("summary", f"Established exact minimum-cost inspection tour visiting all {n} locations."),
            limitations_and_warnings="Optimization TSP is NP-Hard. Exact algorithms become computationally infeasible for n > 15 without heuristics (e.g. Christofides 1.5-approximation, 2-Opt local search)."
        )

    return AlgorithmExplanation(
        module_name="Adaptive Framework Engine",
        real_world_question="General network design and optimization question.",
        mathematical_formulation="Algorithmic problem formulation.",
        input_properties=context,
        selected_algorithm="Selected algorithm",
        alternative_considered="Alternative algorithm",
        selection_reason="Optimization criteria satisfied.",
        expected_time_complexity="O(f(n))",
        expected_space_complexity="O(g(n))",
        correctness_assumptions="Valid inputs required.",
        actual_result_summary="Completed successfully.",
        limitations_and_warnings="Scalability limits apply."
    )
