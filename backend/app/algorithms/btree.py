"""
Adaptive Network Design and Optimization Framework
Module 3: Advanced Data Structures - B-Tree Implementation
Fully compliant with CLRS B-Tree specification with search, insert, split, delete, borrow, and merge.
"""

from typing import List, Optional, Tuple, Dict, Any


class DeviceRecord:
    def __init__(
        self,
        device_id: str,
        device_name: str,
        network_location: str,
        device_category: str,
        operational_status: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.device_id = device_id
        self.device_name = device_name
        self.network_location = network_location
        self.device_category = device_category
        self.operational_status = operational_status
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "device_id": self.device_id,
            "device_name": self.device_name,
            "network_location": self.network_location,
            "device_category": self.device_category,
            "operational_status": self.operational_status,
            "metadata": self.metadata
        }


class BTreeNode:
    def __init__(self, leaf: bool = True):
        self.leaf: bool = leaf
        self.keys: List[str] = []
        self.values: List[DeviceRecord] = []
        self.children: List['BTreeNode'] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "keys": self.keys,
            "is_leaf": self.leaf,
            "num_keys": len(self.keys),
            "records": [v.to_dict() for v in self.values],
            "children": [c.to_dict() for c in self.children]
        }


class BTree:
    """
    B-Tree with minimum degree t >= 2.
    Invariants:
    1. Every node has at most 2t - 1 keys.
    2. Every non-root node has at least t - 1 keys.
    3. An internal node with k keys has k + 1 children.
    4. All leaves have the same depth.
    """
    def __init__(self, t: int = 3):
        if t < 2:
            raise ValueError("B-Tree minimum degree t must be >= 2.")
        self.t: int = t
        self.root: BTreeNode = BTreeNode(leaf=True)
        self.key_comparisons: int = 0
        self.splits_count: int = 0
        self.merges_count: int = 0
        self.borrows_count: int = 0
        self.size: int = 0

    def reset_metrics(self):
        self.key_comparisons = 0
        self.splits_count = 0
        self.merges_count = 0
        self.borrows_count = 0

    def search(self, key: str, node: Optional[BTreeNode] = None) -> Tuple[Optional[DeviceRecord], int]:
        """Search for a key. Returns (record, comparisons)."""
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys):
            self.key_comparisons += 1
            if key <= node.keys[i]:
                break
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i], self.key_comparisons

        if node.leaf:
            return None, self.key_comparisons

        return self.search(key, node.children[i])

    def insert(self, record: DeviceRecord) -> bool:
        """Insert or update a DeviceRecord."""
        key = record.device_id
        root = self.root

        # Check if root is full (has 2t - 1 keys)
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0, root)
            self.root = new_root
            self._insert_non_full(new_root, record)
        else:
            self._insert_non_full(root, record)

        return True

    def _split_child(self, parent: BTreeNode, index: int, child: BTreeNode):
        """Splits full child (2t - 1 keys) into two nodes with t - 1 keys each."""
        self.splits_count += 1
        t = self.t
        sibling = BTreeNode(leaf=child.leaf)

        # Median index is t - 1
        median_key = child.keys[t - 1]
        median_val = child.values[t - 1]

        # Sibling gets right half (keys from t to 2t - 2)
        sibling.keys = child.keys[t:]
        sibling.values = child.values[t:]
        if not child.leaf:
            sibling.children = child.children[t:]

        # Child retains left half (keys from 0 to t - 2)
        child.keys = child.keys[:t - 1]
        child.values = child.values[:t - 1]
        if not child.leaf:
            child.children = child.children[:t]

        # Insert median into parent
        parent.children.insert(index + 1, sibling)
        parent.keys.insert(index, median_key)
        parent.values.insert(index, median_val)

    def _insert_non_full(self, node: BTreeNode, record: DeviceRecord):
        key = record.device_id
        i = len(node.keys) - 1

        if node.leaf:
            # Check for existing duplicate key to update
            while i >= 0:
                self.key_comparisons += 1
                if key == node.keys[i]:
                    node.values[i] = record
                    return
                elif key > node.keys[i]:
                    break
                i -= 1

            node.keys.insert(i + 1, key)
            node.values.insert(i + 1, record)
            self.size += 1
        else:
            while i >= 0:
                self.key_comparisons += 1
                if key == node.keys[i]:
                    node.values[i] = record
                    return
                elif key > node.keys[i]:
                    break
                i -= 1
            i += 1

            # If child is full, split it first
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i, node.children[i])
                self.key_comparisons += 1
                if key == node.keys[i]:
                    node.values[i] = record
                    return
                elif key > node.keys[i]:
                    i += 1

            self._insert_non_full(node.children[i], record)

    def delete(self, key: str) -> bool:
        """Deletes key from B-Tree maintaining all invariants."""
        if not self.root.keys:
            return False

        existed = self._delete_key(self.root, key)
        if existed:
            self.size -= 1
            # If root becomes empty, shrink tree height
            if len(self.root.keys) == 0 and not self.root.leaf:
                self.root = self.root.children[0]
        return existed

    def _delete_key(self, node: BTreeNode, key: str) -> bool:
        t = self.t
        i = 0
        while i < len(node.keys):
            self.key_comparisons += 1
            if key <= node.keys[i]:
                break
            i += 1

        # Case 1 & 2: Key found in current node
        if i < len(node.keys) and node.keys[i] == key:
            if node.leaf:
                # Case 1: Key is in a leaf node
                node.keys.pop(i)
                node.values.pop(i)
                return True
            else:
                # Case 2: Key is in an internal node
                # Case 2a: Left child has >= t keys
                if len(node.children[i].keys) >= t:
                    pred_key, pred_val = self._get_predecessor(node.children[i])
                    node.keys[i] = pred_key
                    node.values[i] = pred_val
                    return self._delete_key(node.children[i], pred_key)
                # Case 2b: Right child has >= t keys
                elif len(node.children[i + 1].keys) >= t:
                    succ_key, succ_val = self._get_successor(node.children[i + 1])
                    node.keys[i] = succ_key
                    node.values[i] = succ_val
                    return self._delete_key(node.children[i + 1], succ_key)
                # Case 2c: Both children have t - 1 keys -> merge them
                else:
                    self._merge_children(node, i)
                    return self._delete_key(node.children[i], key)
        else:
            # Case 3: Key not in current node
            if node.leaf:
                return False  # Key does not exist

            # Ensure child node.children[i] has at least t keys
            if len(node.children[i].keys) < t:
                self._fill_child(node, i)

            # If merging happened, index might need adjusting
            if i > len(node.keys):
                i = len(node.keys)

            return self._delete_key(node.children[i], key)

    def _get_predecessor(self, node: BTreeNode) -> Tuple[str, DeviceRecord]:
        curr = node
        while not curr.leaf:
            curr = curr.children[-1]
        return curr.keys[-1], curr.values[-1]

    def _get_successor(self, node: BTreeNode) -> Tuple[str, DeviceRecord]:
        curr = node
        while not curr.leaf:
            curr = curr.children[0]
        return curr.keys[0], curr.values[0]

    def _fill_child(self, node: BTreeNode, idx: int):
        t = self.t
        # Borrow from left sibling
        if idx > 0 and len(node.children[idx - 1].keys) >= t:
            self.borrows_count += 1
            child = node.children[idx]
            sibling = node.children[idx - 1]

            child.keys.insert(0, node.keys[idx - 1])
            child.values.insert(0, node.values[idx - 1])
            if not child.leaf:
                child.children.insert(0, sibling.children.pop())

            node.keys[idx - 1] = sibling.keys.pop()
            node.values[idx - 1] = sibling.values.pop()

        # Borrow from right sibling
        elif idx < len(node.children) - 1 and len(node.children[idx + 1].keys) >= t:
            self.borrows_count += 1
            child = node.children[idx]
            sibling = node.children[idx + 1]

            child.keys.append(node.keys[idx])
            child.values.append(node.values[idx])
            if not child.leaf:
                child.children.append(sibling.children.pop(0))

            node.keys[idx] = sibling.keys.pop(0)
            node.values[idx] = sibling.values.pop(0)

        # Merge with sibling
        else:
            if idx < len(node.children) - 1:
                self._merge_children(node, idx)
            else:
                self._merge_children(node, idx - 1)

    def _merge_children(self, parent: BTreeNode, idx: int):
        self.merges_count += 1
        left_child = parent.children[idx]
        right_child = parent.children[idx + 1]

        # Pull down key from parent into left child
        left_child.keys.append(parent.keys.pop(idx))
        left_child.values.append(parent.values.pop(idx))

        # Append right child keys and children to left child
        left_child.keys.extend(right_child.keys)
        left_child.values.extend(right_child.values)
        if not left_child.leaf:
            left_child.children.extend(right_child.children)

        parent.children.pop(idx + 1)

    def get_all_records(self) -> List[DeviceRecord]:
        """In-order traversal returning all records."""
        records: List[DeviceRecord] = []

        def _traverse(node: BTreeNode):
            for i in range(len(node.keys)):
                if not node.leaf and i < len(node.children):
                    _traverse(node.children[i])
                records.append(node.values[i])
            if not node.leaf and len(node.children) > len(node.keys):
                _traverse(node.children[-1])

        if self.root.keys:
            _traverse(self.root)
        return records

    def verify_invariants(self) -> Dict[str, Any]:
        """Validates all CLRS B-Tree invariants."""
        leaf_depths: List[int] = []

        def _check(node: BTreeNode, depth: int, is_root: bool) -> bool:
            # 1. Key count invariant
            max_keys = 2 * self.t - 1
            min_keys = 1 if is_root else (self.t - 1)
            if len(node.keys) > max_keys:
                return False
            if not is_root and len(node.keys) < min_keys:
                return False

            # 2. Key sortedness
            for i in range(len(node.keys) - 1):
                if node.keys[i] >= node.keys[i + 1]:
                    return False

            # 3. Children count
            if not node.leaf:
                if len(node.children) != len(node.keys) + 1:
                    return False
                for child in node.children:
                    if not _check(child, depth + 1, False):
                        return False
            else:
                leaf_depths.append(depth)

            return True

        if not self.root.keys:
            return {"valid": True, "size": 0, "height": 0, "leaf_depth_uniform": True}

        is_valid = _check(self.root, 1, True)
        uniform_leaves = len(set(leaf_depths)) <= 1
        height = max(leaf_depths) if leaf_depths else 1

        return {
            "valid": is_valid and uniform_leaves,
            "size": self.size,
            "height": height,
            "leaf_depth_uniform": uniform_leaves,
            "minimum_degree": self.t
        }
