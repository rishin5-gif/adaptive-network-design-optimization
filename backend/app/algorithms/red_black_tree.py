"""
Adaptive Network Design and Optimization Framework
Module 3: Advanced Data Structures - Red-Black Tree Implementation
Fully compliant with CLRS Red-Black Tree specification with insertion fixup, deletion fixup, and invariant verification.
"""

from typing import Optional, Dict, Any, List, Tuple
from enum import Enum


class Color(str, Enum):
    RED = "RED"
    BLACK = "BLACK"


class RBTNode:
    def __init__(
        self,
        key: str,
        value: Any,
        color: Color = Color.RED,
        left: Optional['RBTNode'] = None,
        right: Optional['RBTNode'] = None,
        parent: Optional['RBTNode'] = None
    ):
        self.key = key
        self.value = value
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "color": self.color.value,
            "record": self.value.to_dict() if hasattr(self.value, "to_dict") else self.value,
            "left": self.left.to_dict() if self.left and self.left.key is not None else None,
            "right": self.right.to_dict() if self.right and self.right.key is not None else None
        }


class RedBlackTree:
    """
    CLRS Red-Black Tree Implementation.
    Invariants:
    1. Every node is either RED or BLACK.
    2. The root is BLACK.
    3. Every leaf (NIL sentinel) is BLACK.
    4. If a node is RED, then both its children are BLACK (no consecutive red nodes).
    5. For each node, all simple paths from the node to descendant leaves contain the same number of black nodes (Black-Height).
    """
    def __init__(self):
        # NIL sentinel node
        self.NIL = RBTNode(key=None, value=None, color=Color.BLACK)
        self.root: RBTNode = self.NIL
        self.size: int = 0
        self.key_comparisons: int = 0
        self.left_rotations: int = 0
        self.right_rotations: int = 0
        self.recolorings: int = 0

    def reset_metrics(self):
        self.key_comparisons = 0
        self.left_rotations = 0
        self.right_rotations = 0
        self.recolorings = 0

    def search(self, key: str) -> Tuple[Optional[Any], int]:
        """Search for a key. Returns (record, comparisons)."""
        curr = self.root
        while curr != self.NIL:
            self.key_comparisons += 1
            if key == curr.key:
                return curr.value, self.key_comparisons
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return None, self.key_comparisons

    def left_rotate(self, x: RBTNode):
        """Left rotation on node x."""
        self.left_rotations += 1
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None or x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, y: RBTNode):
        """Right rotation on node y."""
        self.right_rotations += 1
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent
        if y.parent is None or y.parent == self.NIL:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    def insert(self, record: Any) -> bool:
        """Inserts record into Red-Black Tree, maintaining invariants."""
        key = record.device_id
        z = RBTNode(key=key, value=record, color=Color.RED, left=self.NIL, right=self.NIL)

        y = self.NIL
        x = self.root

        # Standard BST Insertion
        while x != self.NIL:
            y = x
            self.key_comparisons += 1
            if z.key == x.key:
                # Update existing record
                x.value = record
                return True
            elif z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y == self.NIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        self.size += 1
        self._insert_fixup(z)
        return True

    def _insert_fixup(self, z: RBTNode):
        """Restores Red-Black invariants after insertion."""
        while z.parent and z.parent.color == Color.RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right  # Uncle
                if y.color == Color.RED:
                    # Case 1: Uncle is RED -> Recolor
                    self.recolorings += 3
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        # Case 2: Uncle is BLACK & z is right child -> Left rotate to line
                        z = z.parent
                        self.left_rotate(z)
                    # Case 3: Uncle is BLACK & z is left child -> Right rotate & recolor
                    self.recolorings += 2
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.right_rotate(z.parent.parent)
            else:
                # Symmetric case: z.parent is right child
                y = z.parent.parent.left  # Uncle
                if y.color == Color.RED:
                    # Case 1: Uncle is RED
                    self.recolorings += 3
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        # Case 2: Left child
                        z = z.parent
                        self.right_rotate(z)
                    # Case 3: Right child
                    self.recolorings += 2
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.left_rotate(z.parent.parent)

            if z == self.root:
                break

        if self.root.color != Color.BLACK:
            self.root.color = Color.BLACK
            self.recolorings += 1

    def _transplant(self, u: RBTNode, v: RBTNode):
        if u.parent == self.NIL or u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node: RBTNode) -> RBTNode:
        curr = node
        while curr.left != self.NIL:
            curr = curr.left
        return curr

    def delete(self, key: str) -> bool:
        """Deletes key from Red-Black tree maintaining all invariants."""
        z = self.root
        while z != self.NIL:
            self.key_comparisons += 1
            if key == z.key:
                break
            elif key < z.key:
                z = z.left
            else:
                z = z.right

        if z == self.NIL:
            return False  # Key not found

        y = z
        y_orig_color = y.color

        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_orig_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        self.size -= 1
        if y_orig_color == Color.BLACK:
            self._delete_fixup(x)

        return True

    def _delete_fixup(self, x: RBTNode):
        """Restores Red-Black invariants after deletion of a black node."""
        while x != self.root and x.color == Color.BLACK:
            if x == x.parent.left:
                w = x.parent.right  # Sibling
                if w.color == Color.RED:
                    # Case 1: Sibling is RED
                    self.recolorings += 2
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.left_rotate(x.parent)
                    w = x.parent.right

                if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
                    # Case 2: Sibling is BLACK and both sibling's children are BLACK
                    self.recolorings += 1
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.right.color == Color.BLACK:
                        # Case 3: Sibling is BLACK, left child is RED, right is BLACK
                        self.recolorings += 2
                        w.left.color = Color.BLACK
                        w.color = Color.RED
                        self.right_rotate(w)
                        w = x.parent.right
                    # Case 4: Sibling is BLACK and right child is RED
                    self.recolorings += 2
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.right.color = Color.BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                # Symmetric case: x is right child
                w = x.parent.left  # Sibling
                if w.color == Color.RED:
                    # Case 1
                    self.recolorings += 2
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.right_rotate(x.parent)
                    w = x.parent.left

                if w.right.color == Color.BLACK and w.left.color == Color.BLACK:
                    # Case 2
                    self.recolorings += 1
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.left.color == Color.BLACK:
                        # Case 3
                        self.recolorings += 2
                        w.right.color = Color.BLACK
                        w.color = Color.RED
                        self.left_rotate(w)
                        w = x.parent.left
                    # Case 4
                    self.recolorings += 2
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.left.color = Color.BLACK
                    self.right_rotate(x.parent)
                    x = self.root

        if x.color != Color.BLACK:
            x.color = Color.BLACK
            self.recolorings += 1

    def get_all_records(self) -> List[Any]:
        """In-order traversal."""
        records = []
        def _inorder(node: RBTNode):
            if node != self.NIL:
                _inorder(node.left)
                records.append(node.value)
                _inorder(node.right)
        _inorder(self.root)
        return records

    def verify_invariants(self) -> Dict[str, Any]:
        """Checks CLRS properties: Root is Black, No Double Red, Uniform Black Height."""
        if self.root == self.NIL:
            return {"valid": True, "size": 0, "black_height": 0, "no_double_red": True}

        # 1. Root must be BLACK
        if self.root.color != Color.BLACK:
            return {"valid": False, "reason": "Root is not BLACK"}

        black_heights: List[int] = []
        no_double_red = True

        def _traverse(node: RBTNode, current_black_count: int) -> bool:
            nonlocal no_double_red
            if node == self.NIL:
                black_heights.append(current_black_count + 1)
                return True

            next_count = current_black_count + (1 if node.color == Color.BLACK else 0)

            # Check no double red
            if node.color == Color.RED:
                if (node.left != self.NIL and node.left.color == Color.RED) or \
                   (node.right != self.NIL and node.right.color == Color.RED):
                    no_double_red = False

            return _traverse(node.left, next_count) and _traverse(node.right, next_count)

        valid_tree = _traverse(self.root, 0)
        uniform_black_height = len(set(black_heights)) <= 1
        black_height = black_heights[0] if black_heights else 0

        return {
            "valid": valid_tree and uniform_black_height and no_double_red,
            "size": self.size,
            "black_height": black_height,
            "no_double_red": no_double_red,
            "uniform_black_height": uniform_black_height
        }
