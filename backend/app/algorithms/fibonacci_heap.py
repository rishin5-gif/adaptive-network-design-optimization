"""
Adaptive Network Design and Optimization Framework
Module 4: Maintenance Event Prioritization - Fibonacci Heap
Circular doubly linked list representation with consolidation and cascading cuts.
Theoretical Complexity:
- Insert, Find-Min, Union, Decrease-Key: O(1) amortized
- Extract-Min, Delete: O(log n) amortized
"""

import math
from typing import Optional, Dict, Any, List
from .binomial_heap import MaintenanceEvent


class FibNode:
    def __init__(self, key: int, event: MaintenanceEvent):
        self.key: int = key
        self.event: MaintenanceEvent = event
        self.degree: int = 0
        self.parent: Optional['FibNode'] = None
        self.child: Optional['FibNode'] = None
        self.left: 'FibNode' = self
        self.right: 'FibNode' = self
        self.marked: bool = False

    def to_dict(self) -> Dict[str, Any]:
        children = []
        if self.child:
            curr = self.child
            while True:
                children.append(curr.to_dict())
                curr = curr.right
                if curr == self.child:
                    break
        return {
            "key": self.key,
            "degree": self.degree,
            "marked": self.marked,
            "event": self.event.to_dict(),
            "children": children
        }


class FibonacciHeap:
    """
    Fredman & Tarjan Fibonacci Heap.
    Supports O(1) amortized decrease-key and O(log n) extract-min.
    """
    def __init__(self):
        self.min_node: Optional[FibNode] = None
        self.total_nodes: int = 0
        self.links_count: int = 0
        self.cuts_count: int = 0
        self.cascading_cuts_count: int = 0
        self.comparisons_count: int = 0
        self.node_map: Dict[str, FibNode] = {}  # event_id -> FibNode for O(1) lookup

    def reset_metrics(self):
        self.links_count = 0
        self.cuts_count = 0
        self.cascading_cuts_count = 0
        self.comparisons_count = 0

    def is_empty(self) -> bool:
        return self.min_node is None

    def find_min(self) -> Optional[FibNode]:
        """Returns pointer to minimum node in O(1)."""
        return self.min_node

    def insert(self, event: MaintenanceEvent) -> FibNode:
        """Inserts a new event into root list in O(1) actual and amortized."""
        node = FibNode(event.priority, event)
        self.node_map[event.event_id] = node

        if not self.min_node:
            self.min_node = node
        else:
            self._add_to_root_list(node)
            self.comparisons_count += 1
            if node.key < self.min_node.key:
                self.min_node = node

        self.total_nodes += 1
        return node

    def _add_to_root_list(self, node: FibNode):
        if not self.min_node:
            self.min_node = node
            node.left = node
            node.right = node
        else:
            # Splice into circular list next to min_node
            node.right = self.min_node.right
            node.left = self.min_node
            self.min_node.right.left = node
            self.min_node.right = node
        node.parent = None

    def _remove_from_root_list(self, node: FibNode):
        if node.right == node:
            self.min_node = None
        else:
            node.left.right = node.right
            node.right.left = node.left
            if self.min_node == node:
                self.min_node = node.right

    def union(self, other: 'FibonacciHeap'):
        """Merges two Fibonacci Heaps in O(1) actual and amortized."""
        if not other.min_node:
            return
        if not self.min_node:
            self.min_node = other.min_node
            self.total_nodes = other.total_nodes
            self.node_map.update(other.node_map)
            return

        # Splice root lists together
        self_next = self.min_node.right
        other_prev = other.min_node.left

        self.min_node.right = other.min_node
        other.min_node.left = self.min_node

        self_next.left = other_prev
        other_prev.right = self_next

        self.comparisons_count += 1
        if other.min_node.key < self.min_node.key:
            self.min_node = other.min_node

        self.total_nodes += other.total_nodes
        self.node_map.update(other.node_map)

    def extract_min(self) -> Optional[MaintenanceEvent]:
        """Extracts and consolidates minimum node in O(log n) amortized."""
        z = self.min_node
        if not z:
            return None

        # Add all children of z to the root list
        if z.child:
            children = []
            curr = z.child
            while True:
                children.append(curr)
                curr = curr.right
                if curr == z.child:
                    break
            for child in children:
                child.parent = None
                self._add_to_root_list(child)

        self._remove_from_root_list(z)
        if z.event.event_id in self.node_map:
            del self.node_map[z.event.event_id]

        self.total_nodes -= 1

        if self.min_node:
            self._consolidate()

        return z.event

    def _consolidate(self):
        """Consolidates root list by linking trees of equal degree."""
        # Max degree bound: D(n) <= floor(log_phi(n))
        phi = (1 + math.sqrt(5)) / 2
        max_deg = int(math.log(max(self.total_nodes, 1), phi)) + 5
        A: List[Optional[FibNode]] = [None] * max_deg

        # Collect current root nodes
        roots = []
        curr = self.min_node
        if curr:
            while True:
                roots.append(curr)
                curr = curr.right
                if curr == self.min_node:
                    break

        for w in roots:
            x = w
            d = x.degree
            while d < len(A) and A[d] is not None:
                y = A[d]
                if y == x:
                    break
                self.comparisons_count += 1
                if x.key > y.key:
                    x, y = y, x  # Ensure x has smaller key
                self._link(y, x)
                A[d] = None
                d += 1
            if d < len(A):
                A[d] = x

        # Reconstruct root list and find new min
        self.min_node = None
        for node in A:
            if node:
                node.left = node
                node.right = node
                if not self.min_node:
                    self.min_node = node
                else:
                    self._add_to_root_list(node)
                    self.comparisons_count += 1
                    if node.key < self.min_node.key:
                        self.min_node = node

    def _link(self, y: FibNode, x: FibNode):
        """Links root y to become a child of root x."""
        self.links_count += 1
        # Remove y from root list
        y.left.right = y.right
        y.right.left = y.left

        # Add y to child list of x
        y.parent = x
        if not x.child:
            x.child = y
            y.left = y
            y.right = y
        else:
            y.right = x.child.right
            y.left = x.child
            x.child.right.left = y
            x.child.right = y

        x.degree += 1
        y.marked = False

    def decrease_key(self, event_id: str, new_priority: int) -> bool:
        """Decreases priority in O(1) amortized using cut and cascading cut."""
        if event_id not in self.node_map:
            return False

        x = self.node_map[event_id]
        if new_priority > x.key:
            raise ValueError(f"New priority {new_priority} cannot be greater than current key {x.key}.")

        x.key = new_priority
        x.event.priority = new_priority
        y = x.parent

        self.comparisons_count += 1
        if y and x.key < y.key:
            self._cut(x, y)
            self._cascading_cut(y)

        if x.key < self.min_node.key:
            self.min_node = x

        return True

    def _cut(self, x: FibNode, y: FibNode):
        """Cuts node x from child list of y and moves x to root list."""
        self.cuts_count += 1
        # Remove x from y's child list
        if x.right == x:
            y.child = None
        else:
            x.left.right = x.right
            x.right.left = x.left
            if y.child == x:
                y.child = x.right

        y.degree -= 1
        self._add_to_root_list(x)
        x.marked = False

    def _cascading_cut(self, y: FibNode):
        """Cascading cut: if y is marked, cut y and recurse up; else mark y."""
        z = y.parent
        if z:
            if not y.marked:
                y.marked = True
            else:
                self.cascading_cuts_count += 1
                self._cut(y, z)
                self._cascading_cut(z)

    def get_all_events(self) -> List[MaintenanceEvent]:
        """Returns all events currently stored in heap."""
        return [node.event for node in self.node_map.values()]
