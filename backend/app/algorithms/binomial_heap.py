"""
Adaptive Network Design and Optimization Framework
Module 4: Maintenance Event Prioritization - Binomial Heap
Fully linked node structure with parent, child, sibling, and degree.
Operations: insert, find-min, extract-min, merge, decrease-key.
Convention: Lower numeric key = Higher urgency priority.
"""

from typing import Optional, Dict, Any, List, Tuple


class MaintenanceEvent:
    def __init__(
        self,
        event_id: str,
        description: str,
        priority: int,
        network_location: str,
        created_at: Optional[str] = None
    ):
        self.event_id = event_id
        self.description = description
        self.priority = priority  # Lower is higher urgency
        self.network_location = network_location
        self.created_at = created_at or "2026-10-13T10:00:00Z"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "description": self.description,
            "priority": self.priority,
            "network_location": self.network_location,
            "created_at": self.created_at
        }


class BinomialNode:
    def __init__(self, key: int, event: MaintenanceEvent):
        self.key: int = key
        self.event: MaintenanceEvent = event
        self.degree: int = 0
        self.parent: Optional['BinomialNode'] = None
        self.child: Optional['BinomialNode'] = None
        self.sibling: Optional['BinomialNode'] = None

    def to_dict(self) -> Dict[str, Any]:
        children = []
        curr = self.child
        while curr:
            children.append(curr.to_dict())
            curr = curr.sibling
        return {
            "key": self.key,
            "degree": self.degree,
            "event": self.event.to_dict(),
            "children": children
        }


class BinomialHeap:
    """
    Binomial Heap implementation.
    Collection of Binomial Trees satisfying min-heap property.
    Root list strictly ordered by ascending degrees.
    """
    def __init__(self):
        self.head: Optional[BinomialNode] = None
        self.size: int = 0
        self.links_count: int = 0
        self.merges_count: int = 0
        self.comparisons_count: int = 0

    def reset_metrics(self):
        self.links_count = 0
        self.merges_count = 0
        self.comparisons_count = 0

    def is_empty(self) -> bool:
        return self.head is None

    def find_min(self) -> Optional[BinomialNode]:
        """Finds minimum key node. Scans root list in O(log n)."""
        if not self.head:
            return None
        min_node = self.head
        curr = self.head.sibling
        while curr:
            self.comparisons_count += 1
            if curr.key < min_node.key:
                min_node = curr
            curr = curr.sibling
        return min_node

    def _link_trees(self, y: BinomialNode, z: BinomialNode):
        """Makes node y a child of node z, where z.key <= y.key."""
        self.links_count += 1
        y.parent = z
        y.sibling = z.child
        z.child = y
        z.degree += 1

    def _merge_root_lists(self, h1: Optional[BinomialNode], h2: Optional[BinomialNode]) -> Optional[BinomialNode]:
        """Merges two root lists in ascending order of degree."""
        if not h1:
            return h2
        if not h2:
            return h1

        dummy = BinomialNode(0, None)  # type: ignore
        tail = dummy
        p1, p2 = h1, h2

        while p1 and p2:
            if p1.degree <= p2.degree:
                tail.sibling = p1
                p1 = p1.sibling
            else:
                tail.sibling = p2
                p2 = p2.sibling
            tail = tail.sibling

        tail.sibling = p1 if p1 else p2
        return dummy.sibling

    def union(self, other: 'BinomialHeap'):
        """Unions this heap with another Binomial Heap in O(log n)."""
        self.merges_count += 1
        new_head = self._merge_root_lists(self.head, other.head)
        self.head = None
        other.head = None
        self.size += other.size

        if not new_head:
            return

        prev = None
        curr = new_head
        next_node = curr.sibling

        while next_node:
            self.comparisons_count += 1
            # Case 1 & 2: Degrees differ or three consecutive same degrees
            if (curr.degree != next_node.degree) or (next_node.sibling and next_node.sibling.degree == curr.degree):
                prev = curr
                curr = next_node
            else:
                # Case 3: curr.key <= next_node.key -> link next_node under curr
                if curr.key <= next_node.key:
                    curr.sibling = next_node.sibling
                    self._link_trees(next_node, curr)
                # Case 4: next_node.key < curr.key -> link curr under next_node
                else:
                    if not prev:
                        new_head = next_node
                    else:
                        prev.sibling = next_node
                    self._link_trees(curr, next_node)
                    curr = next_node
            next_node = curr.sibling

        self.head = new_head

    def insert(self, event: MaintenanceEvent) -> BinomialNode:
        """Inserts an event by creating a single-node heap and unioning."""
        node = BinomialNode(event.priority, event)
        temp_heap = BinomialHeap()
        temp_heap.head = node
        temp_heap.size = 1
        self.union(temp_heap)
        return node

    def extract_min(self) -> Optional[MaintenanceEvent]:
        """Extracts and returns the event with the minimum priority key."""
        if not self.head:
            return None

        # 1. Find min root and its predecessor
        min_prev = None
        min_node = self.head
        prev = None
        curr = self.head

        while curr:
            self.comparisons_count += 1
            if curr.key < min_node.key:
                min_node = curr
                min_prev = prev
            prev = curr
            curr = curr.sibling

        # 2. Remove min_node from root list
        if not min_prev:
            self.head = min_node.sibling
        else:
            min_prev.sibling = min_node.sibling

        # 3. Reverse min_node's children to form a new Binomial Heap
        child = min_node.child
        rev_head = None
        while child:
            next_child = child.sibling
            child.sibling = rev_head
            child.parent = None
            rev_head = child
            child = next_child

        child_heap = BinomialHeap()
        child_heap.head = rev_head
        child_heap.size = (1 << min_node.degree) - 1

        self.size -= (1 << min_node.degree)
        self.union(child_heap)

        return min_node.event

    def decrease_key(self, event_id: str, new_priority: int) -> bool:
        """Finds node with event_id and decreases priority, bubbling up if needed."""
        target_node = self._find_node_by_event(self.head, event_id)
        if not target_node:
            return False

        if new_priority > target_node.key:
            raise ValueError(f"New priority {new_priority} cannot be greater than current key {target_node.key}.")

        target_node.key = new_priority
        target_node.event.priority = new_priority

        # Bubble up along parent pointers
        curr = target_node
        parent = curr.parent
        while parent and curr.key < parent.key:
            self.comparisons_count += 1
            # Swap keys and events
            curr.key, parent.key = parent.key, curr.key
            curr.event, parent.event = parent.event, curr.event
            curr = parent
            parent = curr.parent

        return True

    def _find_node_by_event(self, root: Optional[BinomialNode], event_id: str) -> Optional[BinomialNode]:
        """Searches all trees for node with matching event_id."""
        if not root:
            return None
        curr = root
        while curr:
            if curr.event and curr.event.event_id == event_id:
                return curr
            child_res = self._find_node_by_event(curr.child, event_id)
            if child_res:
                return child_res
            curr = curr.sibling
        return None

    def get_all_events(self) -> List[MaintenanceEvent]:
        """Returns all events currently stored in heap."""
        events = []
        def _collect(node: Optional[BinomialNode]):
            curr = node
            while curr:
                if curr.event:
                    events.append(curr.event)
                _collect(curr.child)
                curr = curr.sibling
        _collect(self.head)
        return events
