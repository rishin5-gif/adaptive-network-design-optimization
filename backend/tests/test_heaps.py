"""
Tests for Module 4: Binomial Heap and Fibonacci Heap priority queues
"""

import pytest
from app.algorithms.binomial_heap import BinomialHeap, MaintenanceEvent
from app.algorithms.fibonacci_heap import FibonacciHeap


def test_binomial_heap_operations():
    bh = BinomialHeap()
    assert bh.is_empty() is True

    # Insert events with priorities: 5, 2, 8, 1, 9
    events = [
        MaintenanceEvent("E1", "Desc 1", 5, "HQ"),
        MaintenanceEvent("E2", "Desc 2", 2, "HQ"),
        MaintenanceEvent("E3", "Desc 3", 8, "HQ"),
        MaintenanceEvent("E4", "Desc 4", 1, "HQ"),
        MaintenanceEvent("E5", "Desc 5", 9, "HQ"),
    ]
    for e in events:
        bh.insert(e)

    assert bh.size == 5

    # Find min should be E4 with priority 1
    min_node = bh.find_min()
    assert min_node is not None
    assert min_node.event.event_id == "E4"
    assert min_node.key == 1

    # Extract min
    extracted = bh.extract_min()
    assert extracted.event_id == "E4"

    # Next min should be E2 with priority 2
    next_min = bh.extract_min()
    assert next_min.event_id == "E2"


def test_binomial_heap_decrease_key():
    bh = BinomialHeap()
    e1 = MaintenanceEvent("E1", "Desc 1", 10, "HQ")
    e2 = MaintenanceEvent("E2", "Desc 2", 20, "HQ")
    bh.insert(e1)
    bh.insert(e2)

    # Decrease E2 from 20 to 1 (becomes new highest urgency)
    bh.decrease_key("E2", 1)
    min_evt = bh.extract_min()
    assert min_evt.event_id == "E2"
    assert min_evt.priority == 1


def test_fibonacci_heap_operations():
    fh = FibonacciHeap()
    assert fh.is_empty() is True

    events = [
        MaintenanceEvent("F1", "Desc 1", 15, "POP"),
        MaintenanceEvent("F2", "Desc 2", 4, "POP"),
        MaintenanceEvent("F3", "Desc 3", 22, "POP"),
        MaintenanceEvent("F4", "Desc 4", 3, "POP"),
        MaintenanceEvent("F5", "Desc 5", 11, "POP"),
    ]
    for e in events:
        fh.insert(e)

    assert fh.total_nodes == 5
    assert fh.find_min().key == 3

    # Extract min should be F4
    first_min = fh.extract_min()
    assert first_min.event_id == "F4"
    assert fh.total_nodes == 4

    # Next min should be F2 (priority 4)
    second_min = fh.extract_min()
    assert second_min.event_id == "F2"
    assert fh.total_nodes == 3


def test_fibonacci_heap_decrease_key():
    fh = FibonacciHeap()
    e1 = MaintenanceEvent("F1", "Desc", 30, "DC")
    e2 = MaintenanceEvent("F2", "Desc", 40, "DC")
    fh.insert(e1)
    fh.insert(e2)

    fh.decrease_key("F2", 5)
    extracted = fh.extract_min()
    assert extracted.event_id == "F2"
    assert extracted.priority == 5


def test_heaps_agreement_on_workload():
    # Insert random priorities into both, extract-min should match exactly
    priorities = [45, 12, 89, 3, 27, 64, 1, 99, 15]
    bh = BinomialHeap()
    fh = FibonacciHeap()

    for idx, p in enumerate(priorities):
        evt = MaintenanceEvent(f"EVT-{idx}", f"Alert {idx}", p, "HQ")
        bh.insert(evt)
        fh.insert(evt)

    b_extracted = []
    f_extracted = []
    while not bh.is_empty():
        b_extracted.append(bh.extract_min().priority)
    while not fh.is_empty():
        f_extracted.append(fh.extract_min().priority)

    assert b_extracted == sorted(priorities)
    assert f_extracted == sorted(priorities)
    assert b_extracted == f_extracted
