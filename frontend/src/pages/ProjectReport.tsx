import React from 'react';
import { FileText, CheckCircle2, BookOpen, ShieldCheck, Cpu, Code2 } from 'lucide-react';

export const ProjectReport: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-8 bg-white border border-slate-200/90 rounded-2xl p-8 md:p-12 shadow-sm text-slate-800 leading-relaxed font-sans">
      {/* Title & Metadata Banner */}
      <div className="border-b border-slate-200 pb-6 space-y-2">
        <div className="flex items-center space-x-2 text-xs font-bold text-blue-600 uppercase tracking-widest">
          <span>Design and Analysis of Algorithms Course Project</span>
          <span>•</span>
          <span>Assignment 4</span>
        </div>
        <h1 className="text-2xl md:text-3xl font-extrabold text-slate-900 tracking-tight">
          Adaptive Network Design and Optimization Framework
        </h1>
        <div className="flex flex-wrap gap-4 text-xs text-slate-500 pt-2 font-medium">
          <span><strong>Course Section:</strong> AI ML Leopards</span>
          <span>•</span>
          <span><strong>Faculty:</strong> Professor Geeta Tripathi, Professor of Practice</span>
          <span>•</span>
          <span><strong>Framework:</strong> End-to-End Integrated Full-Stack Application</span>
        </div>
      </div>

      {/* Section 1: Problem Abstraction and Modeling */}
      <section className="space-y-3">
        <h2 className="text-lg font-bold text-slate-900 flex items-center">
          <BookOpen className="w-5 h-5 mr-2 text-blue-600" />
          1. Problem Abstraction and Modeling
        </h2>
        <p className="text-sm text-slate-600">
          Modern enterprise and metropolitan wide-area networks (WANs) represent interconnected distributed systems requiring rigorous algorithmic optimization across multiple operational lifecycles:
        </p>
        <ul className="list-disc list-inside text-xs space-y-1.5 text-slate-700 pl-2">
          <li><strong>Network Topology Interconnection:</strong> Formulated as finding a Minimum Spanning Tree (MST) on an undirected weighted graph \(G = (V, E, w)\), minimizing total fiber deployment CapEx while ensuring reachability across all sites.</li>
          <li><strong>Transit Delay Routing:</strong> Formulated as All-Pairs Shortest Paths (APSP) on a directed/undirected graph \(G = (V, E, w)\), providing the complete delay matrix \(D\) for route selection and SLA verification.</li>
          <li><strong>Hardware Inventory Indexing:</strong> Formulated as balanced search tree storage supporting logarithmic search, insert, and deletion on Device Records with strict invariant guarantees.</li>
          <li><strong>Emergency Ticket Scheduling:</strong> Formulated as priority queue dispatching where outage urgency is strictly minimized, supporting amortized \(O(1)\) priority escalations.</li>
          <li><strong>Capital Upgrade Allocation:</strong> Formulated as Knapsack optimization under budget constraint \(W\), contrasting divisible resources (fractional) and indivisible units (0/1 DP).</li>
          <li><strong>Field Inspection Route:</strong> Formulated as the Travelling Salesperson Problem (TSP) on complete metric topologies, seeking an exact minimum-cost Hamiltonian cycle.</li>
        </ul>
      </section>

      {/* Section 2: Algorithm Choice and Framework Design */}
      <section className="space-y-3">
        <h2 className="text-lg font-bold text-slate-900 flex items-center">
          <Cpu className="w-5 h-5 mr-2 text-blue-600" />
          2. Algorithm Choice and Framework Architecture
        </h2>
        <p className="text-sm text-slate-600">
          The framework implements an explainable, rule-based decision engine rather than isolated execution routines:
        </p>
        <div className="overflow-x-auto text-xs">
          <table className="w-full border-collapse border border-slate-200">
            <thead className="bg-slate-100 text-slate-700 font-semibold uppercase">
              <tr>
                <th className="p-2.5 border border-slate-200">Module</th>
                <th className="p-2.5 border border-slate-200">Implemented Solvers</th>
                <th className="p-2.5 border border-slate-200">Selection Criterion</th>
                <th className="p-2.5 border border-slate-200">Time Complexity</th>
              </tr>
            </thead>
            <tbody className="font-mono divide-y divide-slate-100 text-[11px]">
              <tr>
                <td className="p-2 border border-slate-200 font-sans font-bold">1. MST Design</td>
                <td className="p-2 border border-slate-200">Prim & Kruskal with DSU</td>
                <td className="p-2 border border-slate-200 font-sans">Kruskal for sparse (\(E \ll V^2\)); Prim for dense (\(E \approx V^2\))</td>
                <td className="p-2 border border-slate-200">\(O((V+E)\log V)\) vs \(O(E \log E)\)</td>
              </tr>
              <tr>
                <td className="p-2 border border-slate-200 font-sans font-bold">2. APSP Delays</td>
                <td className="p-2 border border-slate-200">Floyd-Warshall 3-loop DP</td>
                <td className="p-2 border border-slate-200 font-sans">Dense networks, negative link tolerance, negative cycle audit</td>
                <td className="p-2 border border-slate-200">\(O(V^3)\) time, \(O(V^2)\) space</td>
              </tr>
              <tr>
                <td className="p-2 border border-slate-200 font-sans font-bold">3. Device Index</td>
                <td className="p-2 border border-slate-200">B-Tree (\(t\)) & Red-Black Tree</td>
                <td className="p-2 border border-slate-200 font-sans">B-Tree for I/O block fanout; RBT for in-memory pointer lookups</td>
                <td className="p-2 border border-slate-200">\(O(\log_t n)\) vs \(O(\log_2 n)\)</td>
              </tr>
              <tr>
                <td className="p-2 border border-slate-200 font-sans font-bold">4. Event Queue</td>
                <td className="p-2 border border-slate-200">Binomial & Fibonacci Heaps</td>
                <td className="p-2 border border-slate-200 font-sans">Binomial for strict worst-case; Fibonacci for frequent decrease-key</td>
                <td className="p-2 border border-slate-200">\(O(\log n)\) vs \(O(1)\) amortized</td>
              </tr>
              <tr>
                <td className="p-2 border border-slate-200 font-sans font-bold">5. Upgrade Budget</td>
                <td className="p-2 border border-slate-200">Fractional Greedy & 0/1 DP</td>
                <td className="p-2 border border-slate-200 font-sans">Divisible bandwidth slices vs discrete hardware purchase</td>
                <td className="p-2 border border-slate-200">\(O(n \log n)\) vs \(O(nW)\)</td>
              </tr>
              <tr>
                <td className="p-2 border border-slate-200 font-sans font-bold">6. Inspection TSP</td>
                <td className="p-2 border border-slate-200">Backtracking & Branch & Bound</td>
                <td className="p-2 border border-slate-200 font-sans">Lower bound pruning for reduced permutation search</td>
                <td className="p-2 border border-slate-200">Worst-case \(O((n-1)!)\)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* Section 3: Complexity and Correctness Invariants */}
      <section className="space-y-3">
        <h2 className="text-lg font-bold text-slate-900 flex items-center">
          <ShieldCheck className="w-5 h-5 mr-2 text-emerald-600" />
          3. Complexity and Invariant Verification
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-1.5">
            <span className="font-bold text-slate-900 block">B-Tree Invariant Proof:</span>
            <p className="text-slate-600 leading-relaxed">
              Every node except root contains between \(t - 1\) and \(2t - 1\) keys. All leaves reside at uniform depth \(h \le \log_t((n+1)/2)\). Child splitting during insertion promotes the median key upward, guaranteeing balanced fanout.
            </p>
          </div>
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-1.5">
            <span className="font-bold text-slate-900 block">Red-Black Tree Invariant Proof:</span>
            <p className="text-slate-600 leading-relaxed">
              1. Root is BLACK. 2. No two consecutive RED nodes. 3. Uniform black height \(bh(x)\) across all root-to-NIL paths. Height is bounded by \(2\log_2(n+1)\). Insertion fixup uses at most 2 rotations; deletion uses at most 3 rotations.
            </p>
          </div>
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-1.5">
            <span className="font-bold text-slate-900 block">Fibonacci Heap Potential Method:</span>
            <p className="text-slate-600 leading-relaxed">
              Potential function \(\Phi(H) = t(H) + 2m(H)\), where \(t(H)\) is root trees count and \(m(H)\) is marked nodes count. Cascading cuts convert marked nodes to roots, paying for traversal and proving \(O(1)\) amortized decrease-key.
            </p>
          </div>
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-1.5">
            <span className="font-bold text-slate-900 block">0/1 Knapsack Optimal Substructure:</span>
            <p className="text-slate-600 leading-relaxed">
              Subproblem \(DP[i][w] = \max(DP[i-1][w], DP[i-1][w - w_i] + v_i)\). Demonstrates greedy ratio failure on counterexample (Budget=50, Items: (10, 60), (20, 100), (30, 120); Greedy=160, DP=220).
            </p>
          </div>
        </div>
      </section>

      {/* Section 4: Implementation and Test Verification */}
      <section className="space-y-3">
        <h2 className="text-lg font-bold text-slate-900 flex items-center">
          <Code2 className="w-5 h-5 mr-2 text-indigo-600" />
          4. Implementation and Test Validation
        </h2>
        <p className="text-sm text-slate-600">
          The test suite executes 35 automated unit and integration tests across all boundary conditions:
        </p>
        <div className="bg-slate-900 text-slate-200 p-4 rounded-xl font-mono text-xs space-y-1">
          <div className="text-emerald-400 font-bold">✓ 35 PASSED in 0.29s (100% Pass Rate)</div>
          <div>• test_mst.py: Single-vertex, disconnected forest warning, equal weights, duplicate links (6 tests)</div>
          <div>• test_all_pairs.py: Known shortest paths, infinity unreachable, negative weights, negative cycles (4 tests)</div>
          <div>• test_btree.py: Multi-level insert, leaf & internal deletion, borrowing, merging, invariants (3 tests)</div>
          <div>• test_red_black_tree.py: BST insert, uncle-red recoloring, triangle/line rotations, delete fixup (3 tests)</div>
          <div>• test_heaps.py: Binomial & Fibonacci insert, find-min, extract-min, decrease-key, heap agreement (5 tests)</div>
          <div>• test_knapsack.py: Zero budget, fractional slicing, 0/1 counterexample DP proof, negative weight rejection (4 tests)</div>
          <div>• test_tsp.py: 4-city known optimum, branch & bound pruning verification, infeasible disconnection (3 tests)</div>
          <div>• test_api.py: Health check, dashboard summary, network CRUD, algorithm execution, experiment runner (7 tests)</div>
        </div>
      </section>

      {/* Section 5: Demonstration Viva Checklist */}
      <section className="space-y-3 border-t border-slate-200 pt-6">
        <h2 className="text-lg font-bold text-slate-900 flex items-center">
          <CheckCircle2 className="w-5 h-5 mr-2 text-teal-600" />
          5. Faculty Viva Demonstration Sequence
        </h2>
        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs space-y-2 text-slate-700">
          <p className="font-semibold text-slate-900">Recommended demonstration flow during project evaluation:</p>
          <ol className="list-decimal list-inside space-y-1.5 pl-1">
            <li><strong>Dashboard:</strong> Showcase live KPIs aggregated dynamically from the SQLite database.</li>
            <li><strong>Module 1 (MST):</strong> Run Prim and Kruskal side-by-side on the default 10-node campus topology. Note verified identical total weight ($123.6k) and operation counts. Generate a disconnected graph to show error handling.</li>
            <li><strong>Module 2 (Floyd-Warshall):</strong> Display the 10×10 all-pairs delay matrix. Use the Route Inspector to trace multi-hop paths via the predecessor matrix Π.</li>
            <li><strong>Module 3 (Trees):</strong> Search for a device ID, compare key comparisons between B-Tree (t=3) and Red-Black Tree, and run the identical 100-operation workload benchmark.</li>
            <li><strong>Module 4 (Heaps):</strong> Extract the minimum urgent ticket (P1). Escalate another event using Decrease-Key, observing Fibonacci Heap cascading cuts vs Binomial tree links.</li>
            <li><strong>Module 5 (Knapsack):</strong> Slide the CapEx budget slider. Explain why the Greedy heuristic fails for indivisible servers and how 0/1 DP recovers the true global optimum.</li>
            <li><strong>Module 6 (TSP):</strong> Solve the 5-site inspection tour. Point out the number of search states pruned by Branch & Bound compared to exhaustive Backtracking.</li>
            <li><strong>Experiment Lab:</strong> Run an empirical benchmark (e.g. Floyd-Warshall cubic scaling or Sparse vs Dense MST) across 3 trials and export the CSV log.</li>
          </ol>
        </div>
      </section>
    </div>
  );
};
