# Adaptive Network Design and Optimization Framework

**Assignment Number:** 4  
**Course:** Design and Analysis of Algorithms  
**Course Section:** AI ML Leopards  
**Faculty:** Professor Geeta Tripathi, Professor of Practice  
**Repository Name:** `adaptive-network-design-optimization`  

---

## 1. Project Objective

The **Adaptive Network Design and Optimization Framework** is a complete, full-stack software system that integrates graph algorithms, advanced search trees, amortized priority heaps, dynamic programming, and combinatorial search into a single explainable framework.

The priority of this academic implementation is algorithmic correctness, unsimulated experimental comparisons, high-resolution monotonic timer measurements, and transparent decision rationales.

---

## 2. Problem Statement

Modern enterprise and metropolitan wide-area networks (WANs) require continuous optimization across multiple operational layers:
1. **Network Infrastructure Design:** Minimizing total optical cable deployment expenditure while ensuring complete graph reachability without cycles (Minimum Spanning Tree).
2. **Transit Delay & Latency Routing:** Calculating all-pairs shortest path delays across all node pairs, handling negative links and identifying negative cycle hazards (All-Pairs Shortest Path).
3. **Hardware Inventory Search & Indexing:** Maintaining hardware device records with guaranteed logarithmic lookup and structural invariants (B-Tree & Red-Black Tree).
4. **Maintenance Event Prioritization:** Managing network failure tickets with strictly minimized urgency values and constant-time priority escalations (Binomial & Fibonacci Heaps).
5. **Capital Budget Allocation:** Selecting network upgrade projects under financial limits, comparing divisible bandwidth slices against discrete physical equipment (Knapsack Problem).
6. **Maintenance Route Optimization:** Finding the optimal inspection tour visiting required maintenance sites exactly once and returning to depot (Travelling Salesperson Problem).

---

## 3. Implemented DAA Algorithms & Data Structures

| Module | Purpose | Implemented Solvers | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **Module 1** | Network Design & MST | **Prim's Algorithm** (Min-Heap)<br>**Kruskal's Algorithm** (DSU with Path Compression & Union by Rank) | $O((V+E)\log V)$<br>$O(E \log E)$ | $O(V+E)$<br>$O(V+E)$ |
| **Module 2** | Communication Latency | **Floyd-Warshall Algorithm** (3-loop Dynamic Programming)<br>Predecessor Matrix $\Pi$ Path Reconstruction | $O(V^3)$ | $O(V^2)$ |
| **Module 3** | Hardware Inventory Index | **B-Tree** (Degree $t \ge 2$, CLRS split, borrow, merge, delete)<br>**Red-Black Tree** (Color properties, rotations, delete fixup) | $O(\log_t n)$<br>$O(\log_2 n)$ | $O(n)$<br>$O(n)$ |
| **Module 4** | Event Prioritization | **Binomial Heap** (Root list of $B_k$ binomial trees)<br>**Fibonacci Heap** (Circular root list, cascading cuts, consolidation) | $O(\log n)$ all ops<br>$O(1)$ amortized dec-key | $O(n)$<br>$O(n)$ |
| **Module 5** | Upgrade Budget Planner | **Fractional Knapsack** (Greedy benefit-to-cost ratio)<br>**0/1 Knapsack** (Dynamic Programming table) | $O(n \log n)$<br>$O(nW)$ | $O(n)$<br>$O(nW)$ |
| **Module 6** | Maintenance Route Planner | **Exact Backtracking TSP** (Permutation search)<br>**Branch and Bound TSP** (Minimum outgoing edge lower bound) | $O((n-1)!)$<br>Exponential (pruned) | $O(n)$<br>$O(n)$ |

---

## 4. Key Features

- **Integrated Decision and Explanation Engine:** Every operation presents a structured 11-point DAA breakdown (Real-world problem, mathematical formulation, input properties, selected algorithm, alternative considered, selection reason, time & space complexities, correctness assumptions, actual result, and scalability warnings).
- **Interactive SVG Canvas Topology Visualizer:** Draggable nodes, live edge weight badges, tier color coding, and dynamic highlights for MST links and TSP tours.
- **Dedicated Experiment Lab:** Runs multi-trial repeated benchmarks across 6 families using monotonic microsecond timers (`time.perf_counter_ns()`), counts structural operations, visualizes curves with Recharts, and exports results to CSV.
- **Enterprise Dashboard:** Real-time KPIs computed directly from database records (never fabricated).
- **Persistence Layer:** SQLite relational database storing topologies, hardware inventories, maintenance tickets, and project pools with a single-click restore sample data action.

---

## 5. Technology Stack

- **Frontend:** React 19, TypeScript, Vite 6, Tailwind CSS, React Router, Recharts, Lucide Icons.
- **Backend:** Python 3.9+, FastAPI, Pydantic, Uvicorn development server.
- **Database:** SQLite (`backend/app/network_framework.db`).
- **Testing:** pytest for backend algorithm and API tests; Vitest and React Testing Library for frontend component tests.
- **Version Control:** Git & GitHub CLI.

---

## 6. Directory Structure

```
adaptive-network-framework/
├── backend/
│   ├── app/
│   │   ├── algorithms/
│   │   │   ├── mst.py                # Prim and Kruskal + DisjointSetUnion
│   │   │   ├── all_pairs.py          # Floyd-Warshall + negative cycle audit
│   │   │   ├── btree.py              # Custom B-Tree with deletion & invariants
│   │   │   ├── red_black_tree.py     # Custom Red-Black Tree with fixup
│   │   │   ├── binomial_heap.py      # Custom Binomial Heap with decrease-key
│   │   │   ├── fibonacci_heap.py     # Custom Fibonacci Heap with cascading cuts
│   │   │   ├── knapsack.py           # Fractional Greedy & 0/1 DP Knapsack
│   │   │   ├── tsp.py                # Backtracking & Branch and Bound TSP
│   │   │   └── explanation_engine.py # 11-point Decision & Explanation Engine
│   │   ├── data/
│   │   │   └── sample_data.py        # Hypothetical 10-node campus dataset
│   │   ├── models/
│   │   │   └── schemas.py            # Pydantic request & response schemas
│   │   ├── routers/
│   │   │   ├── dashboard.py          # Real-time aggregated KPI endpoints
│   │   │   ├── network.py            # Graph CRUD & generator endpoints
│   │   │   ├── algorithms.py         # MST & Floyd-Warshall endpoints
│   │   │   ├── structures.py         # Tree & Heap operations & workloads
│   │   │   ├── optimization.py       # Knapsack & TSP endpoints
│   │   │   └── experiments.py        # Controlled benchmark runner & export
│   │   ├── database.py               # SQLite connection, seeding, and queries
│   │   └── main.py                   # FastAPI application gateway & CORS
│   ├── tests/
│   │   ├── test_mst.py               # MST boundary and correctness tests
│   │   ├── test_all_pairs.py         # Floyd-Warshall and cycle tests
│   │   ├── test_btree.py             # B-Tree insertion, search, deletion tests
│   │   ├── test_red_black_tree.py    # Red-Black Tree invariant tests
│   │   ├── test_heaps.py             # Binomial & Fibonacci Heap tests
│   │   ├── test_knapsack.py          # Greedy counterexample & DP tests
│   │   ├── test_tsp.py               # TSP Backtracking & B&B tests
│   │   └── test_api.py               # FastAPI endpoint integration tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout.tsx            # Header, sidebar, and disclaimer
│   │   │   ├── NetworkGraph.tsx      # Draggable SVG canvas visualizer
│   │   │   ├── ExplanationCard.tsx   # 11-point Decision Engine component
│   │   │   └── MetricsCard.tsx       # Reusable KPI card
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx         # Overview KPIs & quick actions
│   │   │   ├── NetworkDesign.tsx     # Module 1: Prim & Kruskal MST
│   │   │   ├── CommunicationCost.tsx # Module 2: Floyd-Warshall APSP
│   │   │   ├── RecordManagement.tsx  # Module 3: B-Tree & Red-Black Tree
│   │   │   ├── MaintenancePrioritization.tsx # Module 4: Priority Heaps
│   │   │   ├── BudgetPlanner.tsx     # Module 5: Knapsack Solvers
│   │   │   ├── RoutePlanner.tsx      # Module 6: TSP Backtracking & B&B
│   │   │   ├── ExperimentLab.tsx     # Module 7: Performance Experiments Lab
│   │   │   └── ProjectReport.tsx     # Formal in-app DAA Project Report
│   │   ├── services/
│   │   │   └── api.ts                # Strongly typed fetch client
│   │   ├── tests/
│   │   │   ├── setup.ts              # Vitest matchers
│   │   │   └── components.test.tsx   # React component tests
│   │   ├── types/
│   │   │   └── index.ts              # TypeScript domain interfaces
│   │   ├── App.tsx                   # React Router routing
│   │   ├── main.tsx                  # React DOM entrypoint
│   │   └── index.css                 # Tailwind directives
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── vite.config.ts
├── docs/
│   ├── ARCHITECTURE.md               # Mermaid system architecture & layer design
│   ├── DAA_PROJECT_REPORT.md         # Formal academic submission report
│   └── DEMONSTRATION_GUIDE.md        # 5-minute viva demonstration script
├── setup_and_run.sh                  # One-click startup script
└── README.md
```

---

## 7. Installation and Setup Instructions

### Prerequisites
- **Python 3.9+** with `venv`
- **Node.js 18+** with `npm`
- **macOS, Linux, or Windows**

### Step 1: Clone or Navigate to the Project
```bash
cd /Users/rishi/.gemini/antigravity/scratch/adaptive-network-framework
```

### Step 2: Backend Setup
```bash
# Create virtual environment
python3 -m venv backend/venv

# Activate virtual environment
# On macOS/Linux:
source backend/venv/bin/activate
# On Windows:
# backend\venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Step 3: Frontend Setup
```bash
cd frontend
npm install
cd ..
```

---

## 8. Running the Application

### Option A: Using the Automated Startup Script
```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

### Option B: Running Separately in Two Terminals

**Terminal 1 (Backend Server):**
```bash
cd /Users/rishi/.gemini/antigravity/scratch/adaptive-network-framework
source backend/venv/bin/activate
PYTHONPATH=backend uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
- API Base: `http://localhost:8000`
- Interactive OpenAPI Docs: `http://localhost:8000/docs`

**Terminal 2 (Frontend Client):**
```bash
cd /Users/rishi/.gemini/antigravity/scratch/adaptive-network-framework/frontend
npm run dev
```
- Dashboard Interface: `http://localhost:5173`

---

## 9. Running the Automated Test Suites

### Backend Tests (pytest)
```bash
cd /Users/rishi/.gemini/antigravity/scratch/adaptive-network-framework
PYTHONPATH=backend ./backend/venv/bin/python3 -m pytest backend/tests/ -v
```
**Verified Result:** `35 passed in 0.29s` (100% Pass Rate).

### Frontend Tests (Vitest)
```bash
cd /Users/rishi/.gemini/antigravity/scratch/adaptive-network-framework/frontend
npm run test
```
**Verified Result:** `3 passed in 0.66s` (100% Pass Rate).

---

## 10. Known Limitations & Scalability Bounds

1. **TSP Exact Intractability:** TSP optimization is NP-Hard. The branch-and-bound solver introduces a safety threshold ($n \le 12$) and a 4.0s timeout to prevent thread blocking.
2. **0/1 Knapsack Pseudo-Polynomial Nature:** Conventional dynamic programming runs in $O(nW)$ time. For astronomical budget values $W$ with fractional cents, scaling factors are required.
3. **Floyd-Warshall Cubic Growth:** Doubling the number of vertices $V$ increases relaxation steps by $8\times$. Not recommended for graphs with $V > 500$ vertices.
