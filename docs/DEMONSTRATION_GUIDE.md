# DAA Project Viva & Demonstration Guide

**Project:** Adaptive Network Design and Optimization Framework  
**Course:** Design and Analysis of Algorithms (Assignment 4)  
**Section:** AI ML Leopards  
**Faculty:** Professor Geeta Tripathi, Professor of Practice  

---

## 5-Minute Demonstration Walkthrough

Follow this step-by-step sequence during your project evaluation viva:

### Step 1: Framework Overview & Dashboard (0:00 - 0:45)
1. Open the running dashboard at `http://localhost:5173`.
2. Point out the **Live Key Performance Indicators (KPIs)**:
   - 10 Campus Network Locations & 15 Physical Links
   - Current Minimum Spanning Tree Cost ($123.6k)
   - 10 Registered Hardware Devices in Trees
   - 6 Pending Maintenance Events in Heaps
3. Explain the **Integrated Decision & Explanation Engine**: point out that every operation displays the real-world problem, mathematical formulation, selected algorithm, alternative considered, and theoretical complexity.

### Step 2: Module 1 - Network Design & Minimum Spanning Tree (0:45 - 1:30)
1. Navigate to **Module 1: Network Design (MST)**.
2. Click **Execute MST** in "Compare Both" mode.
3. Show the interactive topology graph where selected MST edges glow in emerald green.
4. Highlight the **Agreement Table**:
   - Prim total cost = Kruskal total cost = **$123.60k**
   - Both algorithms selected exactly $|V| - 1 = 9$ edges.
5. Use the Test Generator to switch between **Sparse** and **Dense** graphs, pointing out that Kruskal is asymptotically preferred for sparse networks, while Prim is preferred for dense networks.
6. Add or delete a vertex to show dynamic graph editing and disconnected component detection.

### Step 3: Module 2 - Communication Cost Analysis (1:30 - 2:15)
1. Navigate to **Module 2: Communication Cost (Floyd)**.
2. Click **Run Floyd-Warshall**.
3. Point out the $10 \times 10$ distance matrix:
   - Diagonal elements $D[i][i] = 0$.
   - Off-diagonal values show shortest multi-hop delays.
4. Use the **Route Inspector** to select `HQ-Core` to `Disaster-DR`:
   - Shows the intermediate hops (e.g. `HQ-Core → East-DC → Disaster-DR`).
   - Reconstructed using the Predecessor Matrix $\Pi$.
5. Click **Run Scaling Benchmark** to display the measured cubic growth curve $O(V^3)$.

### Step 4: Module 3 - Record Management (2:15 - 3:00)
1. Navigate to **Module 3: Record Management (Trees)**.
2. Enter Device ID `DEV-1002` in the search box and click **Search**:
   - Displays Juniper PTX10008 Spine.
   - Shows comparison count: B-Tree comparisons vs Red-Black Tree comparisons.
3. Show the **Invariant Audit Cards**:
   - B-Tree: uniform leaf depth and key bounds $[t-1, 2t-1]$.
   - Red-Black Tree: uniform black height and no double-red nodes.
4. Click **Run Identical Workload Comparison** to show side-by-side performance on 100 insertions, 40 searches, and 20 deletions.

### Step 5: Module 4 - Maintenance Event Prioritization (3:00 - 3:30)
1. Navigate to **Module 4: Maintenance Events (Heaps)**.
2. Note the **Next Urgent Maintenance Task**: `EVT-301` with Priority 1 (Emergency).
3. Click **Extract & Process Event**:
   - Observes that the minimum item is removed and the next urgent event (`EVT-302` Priority 2) is automatically elevated.
4. Demonstrate **Decrease-Key**: select `EVT-305` and decrease its priority from 5 to 1, showing instant re-prioritization.
5. Run the **Heap Comparison** to contrast Binomial tree links with Fibonacci cascading cuts.

### Step 6: Module 5 - Upgrade Budget Planner (3:30 - 4:15)
1. Navigate to **Module 5: Budget Planner (Knapsack)**.
2. Drag the **CapEx Budget Slider** (e.g. to $85,000).
3. Contrast **Fractional Knapsack** (divisible bandwidth) vs **0/1 Knapsack DP** (indivisible switches).
4. Explain the **Greedy Failure Callout**:
   - Point out why the greedy ratio heuristic fails on discrete items (with the textbook counterexample displayed on screen).

### Step 7: Module 6 - Route Planner (4:15 - 4:45)
1. Navigate to **Module 6: Route Planner (TSP)**.
2. Select 5 maintenance sites on the graph and choose `HQ-Core` as the depot.
3. Click **Solve Tour**:
   - Shows the optimal tour loop and minimum route distance.
   - Show the pruning metric: Branch & Bound explores significantly fewer states than exhaustive Backtracking.
4. Review the **NP-Hard Scalability Warning**.

### Step 8: Experiment Lab & Code Verification (4:45 - 5:00)
1. Navigate to **Experiment Lab**.
2. Select **Sparse vs Dense Graphs for Prim & Kruskal** and run 3 trials.
3. Display the interactive Recharts curve and click **Export All Results to CSV**.
4. Conclude by showing the automated test pass count: **35 passed in 0.29s**.
