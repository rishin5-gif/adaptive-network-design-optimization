"""
Tests for Module 3: Red-Black Tree data structure
"""

import pytest
from app.algorithms.red_black_tree import RedBlackTree, Color
from app.algorithms.btree import DeviceRecord


def test_rbt_insertion_and_invariants():
    rbt = RedBlackTree()

    # Insert 15 items in ascending order (worst case for normal BST, RBT handles via rotations)
    for i in range(1, 16):
        rec = DeviceRecord(f"ID-{i:02d}", f"Device {i}", "Site", "Router", "Active")
        rbt.insert(rec)

    assert rbt.size == 15
    inv = rbt.verify_invariants()
    assert inv["valid"] is True
    assert inv["no_double_red"] is True
    assert inv["uniform_black_height"] is True
    assert rbt.root.color == Color.BLACK


def test_rbt_search():
    rbt = RedBlackTree()
    for i in [10, 5, 20, 3, 7, 15, 30]:
        rbt.insert(DeviceRecord(f"K{i}", f"Name {i}", "Site", "Switch", "Active"))

    rec, comps = rbt.search("K15")
    assert rec is not None
    assert rec.device_name == "Name 15"
    assert comps > 0

    absent, _ = rbt.search("K99")
    assert absent is None


def test_rbt_deletion_and_fixup():
    rbt = RedBlackTree()
    keys = ["M", "F", "S", "B", "H", "P", "U", "A", "C", "G", "J", "O", "R", "T", "Z"]
    for k in keys:
        rbt.insert(DeviceRecord(k, f"Dev {k}", "Site", "Gateway", "Active"))

    assert rbt.size == len(keys)
    assert rbt.verify_invariants()["valid"] is True

    # Delete several keys, verifying invariants after each deletion
    for k in ["A", "M", "S", "Z", "F"]:
        deleted = rbt.delete(k)
        assert deleted is True
        assert rbt.search(k)[0] is None
        inv = rbt.verify_invariants()
        assert inv["valid"] is True, f"Invariant broken after deleting {k}"

    assert rbt.size == len(keys) - 5
