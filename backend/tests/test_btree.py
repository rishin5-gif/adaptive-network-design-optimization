"""
Tests for Module 3: B-Tree data structure
"""

import pytest
from app.algorithms.btree import BTree, DeviceRecord


def test_btree_insertion_and_search():
    btree = BTree(t=3)  # Max keys = 5, min keys = 2

    # Insert 10 records
    for i in range(1, 11):
        rec = DeviceRecord(
            device_id=f"DEV-{i:03d}",
            device_name=f"Device {i}",
            network_location="HQ",
            device_category="Switch",
            operational_status="Active"
        )
        btree.insert(rec)

    assert btree.size == 10

    # Search existing key
    found_rec, comps = btree.search("DEV-005")
    assert found_rec is not None
    assert found_rec.device_name == "Device 5"
    assert comps > 0

    # Search non-existent key
    absent_rec, _ = btree.search("DEV-999")
    assert absent_rec is None

    # Check invariants
    inv = btree.verify_invariants()
    assert inv["valid"] is True
    assert inv["leaf_depth_uniform"] is True


def test_btree_update_existing_key():
    btree = BTree(t=2)
    rec1 = DeviceRecord("DEV-01", "Old Name", "HQ", "Router", "Active")
    btree.insert(rec1)

    rec2 = DeviceRecord("DEV-01", "New Name", "HQ", "Router", "Maintenance")
    btree.insert(rec2)

    assert btree.size == 1
    found, _ = btree.search("DEV-01")
    assert found.device_name == "New Name"
    assert found.operational_status == "Maintenance"


def test_btree_deletion_leaf_and_internal():
    btree = BTree(t=2)
    # Insert keys 1 to 15
    for i in range(1, 16):
        btree.insert(DeviceRecord(f"K{i:02d}", f"Dev {i}", "HQ", "Switch", "Active"))

    assert btree.size == 15
    inv = btree.verify_invariants()
    assert inv["valid"] is True

    # Delete leaf key
    assert btree.delete("K15") is True
    assert btree.size == 14
    assert btree.search("K15")[0] is None
    assert btree.verify_invariants()["valid"] is True

    # Delete internal key
    assert btree.delete("K08") is True
    assert btree.size == 13
    assert btree.search("K08")[0] is None
    assert btree.verify_invariants()["valid"] is True

    # Delete non-existent key
    assert btree.delete("K99") is False
    assert btree.size == 13
