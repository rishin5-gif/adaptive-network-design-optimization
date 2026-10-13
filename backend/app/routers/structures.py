"""
Adaptive Network Design and Optimization Framework
Structures Router: Module 3 (B-Tree vs Red-Black Tree) & Module 4 (Binomial vs Fibonacci Heap)
"""

import time
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException
from ..models.schemas import (
    DeviceRecordSchema,
    TreeOperationRequest,
    TreeWorkloadRequest,
    HeapOperationRequest,
    HeapWorkloadRequest,
    ApiResponse
)
from ..algorithms.btree import BTree, DeviceRecord
from ..algorithms.red_black_tree import RedBlackTree
from ..algorithms.binomial_heap import BinomialHeap, MaintenanceEvent
from ..algorithms.fibonacci_heap import FibonacciHeap
from ..algorithms.explanation_engine import generate_explanation
from ..database import get_all_devices, get_all_maintenance_events

router = APIRouter(prefix="/api/structures", tags=["Advanced Data Structures"])

# Global in-memory data structures initialized with stored records
global_btree: BTree = BTree(t=3)
global_rbt: RedBlackTree = RedBlackTree()
global_binomial_heap: BinomialHeap = BinomialHeap()
global_fib_heap: FibonacciHeap = FibonacciHeap()


def sync_initial_structures():
    """Initializes in-memory trees and heaps from SQLite database."""
    global global_btree, global_rbt, global_binomial_heap, global_fib_heap
    global_btree = BTree(t=3)
    global_rbt = RedBlackTree()
    global_binomial_heap = BinomialHeap()
    global_fib_heap = FibonacciHeap()

    devices = get_all_devices()
    for d in devices:
        rec = DeviceRecord(
            device_id=d["device_id"],
            device_name=d["device_name"],
            network_location=d["network_location"],
            device_category=d["device_category"],
            operational_status=d["operational_status"],
            metadata=d.get("metadata", {})
        )
        global_btree.insert(rec)
        global_rbt.insert(rec)

    events = get_all_maintenance_events()
    for e in events:
        evt = MaintenanceEvent(
            event_id=e["event_id"],
            description=e["description"],
            priority=e["priority"],
            network_location=e["network_location"],
            created_at=e["created_at"]
        )
        global_binomial_heap.insert(evt)
        global_fib_heap.insert(evt)


sync_initial_structures()


@router.post("/btree/operations", response_model=ApiResponse)
def execute_btree_op(req: TreeOperationRequest):
    """Executes single operation on custom B-Tree."""
    global global_btree
    if req.order_t and req.order_t != global_btree.t:
        # Re-initialize tree with requested order
        records = global_btree.get_all_records()
        global_btree = BTree(t=req.order_t)
        for r in records:
            global_btree.insert(r)

    global_btree.reset_metrics()
    start_ns = time.perf_counter_ns()

    if req.operation == "search":
        if not req.device_id:
            raise HTTPException(status_code=400, detail="device_id required for search.")
        rec, comps = global_btree.search(req.device_id)
        elapsed = (time.perf_counter_ns() - start_ns) / 1_000_000
        return ApiResponse(
            success=True,
            data={
                "record": rec.to_dict() if rec else None,
                "found": rec is not None,
                "key_comparisons": comps,
                "execution_time_ms": elapsed,
                "invariants": global_btree.verify_invariants()
            },
            message=f"B-Tree search for '{req.device_id}' completed."
        )

    elif req.operation == "insert":
        if not req.record:
            raise HTTPException(status_code=400, detail="record payload required for insert.")
        rec = DeviceRecord(
            device_id=req.record.device_id,
            device_name=req.record.device_name,
            network_location=req.record.network_location,
            device_category=req.record.device_category,
            operational_status=req.record.operational_status,
            metadata=req.record.metadata or {}
        )
        global_btree.insert(rec)
        elapsed = (time.perf_counter_ns() - start_ns) / 1_000_000
        return ApiResponse(
            success=True,
            data={
                "splits": global_btree.splits_count,
                "key_comparisons": global_btree.key_comparisons,
                "execution_time_ms": elapsed,
                "invariants": global_btree.verify_invariants()
            },
            message=f"Record '{rec.device_id}' inserted into B-Tree."
        )

    elif req.operation == "delete":
        if not req.device_id:
            raise HTTPException(status_code=400, detail="device_id required for delete.")
        deleted = global_btree.delete(req.device_id)
        elapsed = (time.perf_counter_ns() - start_ns) / 1_000_000
        return ApiResponse(
            success=True,
            data={
                "deleted": deleted,
                "merges": global_btree.merges_count,
                "borrows": global_btree.borrows_count,
                "key_comparisons": global_btree.key_comparisons,
                "execution_time_ms": elapsed,
                "invariants": global_btree.verify_invariants()
            },
            message=f"Delete '{req.device_id}' result: {deleted}."
        )

    elif req.operation == "get_all":
        records = [r.to_dict() for r in global_btree.get_all_records()]
        return ApiResponse(
            success=True,
            data={
                "records": records,
                "count": len(records),
                "invariants": global_btree.verify_invariants(),
                "root_tree": global_btree.root.to_dict()
            },
            message="Retrieved all records from B-Tree."
        )

    elif req.operation == "verify_invariants":
        return ApiResponse(
            success=True,
            data=global_btree.verify_invariants(),
            message="B-Tree invariants verified."
        )

    raise HTTPException(status_code=400, detail=f"Unsupported operation: {req.operation}")


@router.post("/red-black-tree/operations", response_model=ApiResponse)
def execute_rbt_op(req: TreeOperationRequest):
    """Executes single operation on custom Red-Black Tree."""
    global global_rbt
    global_rbt.reset_metrics()
    start_ns = time.perf_counter_ns()

    if req.operation == "search":
        if not req.device_id:
            raise HTTPException(status_code=400, detail="device_id required for search.")
        rec, comps = global_rbt.search(req.device_id)
        elapsed = (time.perf_counter_ns() - start_ns) / 1_000_000
        return ApiResponse(
            success=True,
            data={
                "record": rec.to_dict() if rec else None,
                "found": rec is not None,
                "key_comparisons": comps,
                "execution_time_ms": elapsed,
                "invariants": global_rbt.verify_invariants()
            },
            message=f"Red-Black Tree search for '{req.device_id}' completed."
        )

    elif req.operation == "insert":
        if not req.record:
            raise HTTPException(status_code=400, detail="record payload required for insert.")
        rec = DeviceRecord(
            device_id=req.record.device_id,
            device_name=req.record.device_name,
            network_location=req.record.network_location,
            device_category=req.record.device_category,
            operational_status=req.record.operational_status,
            metadata=req.record.metadata or {}
        )
        global_rbt.insert(rec)
        elapsed = (time.perf_counter_ns() - start_ns) / 1_000_000
        return ApiResponse(
            success=True,
            data={
                "left_rotations": global_rbt.left_rotations,
                "right_rotations": global_rbt.right_rotations,
                "recolorings": global_rbt.recolorings,
                "key_comparisons": global_rbt.key_comparisons,
                "execution_time_ms": elapsed,
                "invariants": global_rbt.verify_invariants()
            },
            message=f"Record '{rec.device_id}' inserted into Red-Black Tree."
        )

    elif req.operation == "delete":
        if not req.device_id:
            raise HTTPException(status_code=400, detail="device_id required for delete.")
        deleted = global_rbt.delete(req.device_id)
        elapsed = (time.perf_counter_ns() - start_ns) / 1_000_000
        return ApiResponse(
            success=True,
            data={
                "deleted": deleted,
                "left_rotations": global_rbt.left_rotations,
                "right_rotations": global_rbt.right_rotations,
                "recolorings": global_rbt.recolorings,
                "key_comparisons": global_rbt.key_comparisons,
                "execution_time_ms": elapsed,
                "invariants": global_rbt.verify_invariants()
            },
            message=f"Delete '{req.device_id}' result: {deleted}."
        )

    elif req.operation == "get_all":
        records = [r.to_dict() for r in global_rbt.get_all_records()]
        return ApiResponse(
            success=True,
            data={
                "records": records,
                "count": len(records),
                "invariants": global_rbt.verify_invariants(),
                "root_tree": global_rbt.root.to_dict() if global_rbt.root != global_rbt.NIL else None
            },
            message="Retrieved all records from Red-Black Tree."
        )

    elif req.operation == "verify_invariants":
        return ApiResponse(
            success=True,
            data=global_rbt.verify_invariants(),
            message="Red-Black Tree invariants verified."
        )

    raise HTTPException(status_code=400, detail=f"Unsupported operation: {req.operation}")


@router.post("/trees/compare-workload", response_model=ApiResponse)
def compare_tree_workloads(req: TreeWorkloadRequest):
    """
    Executes identical sequence of Insert, Search, and Delete operations
    on both B-Tree and Red-Black Tree, measuring key comparisons and structural operations.
    """
    try:
        t_val = req.b_tree_order or 3
        btree = BTree(t=t_val)
        rbt = RedBlackTree()

        # 1. Benchmark B-Tree
        btree_start = time.perf_counter_ns()
        for r_s in req.records:
            rec = DeviceRecord(r_s.device_id, r_s.device_name, r_s.network_location, r_s.device_category, r_s.operational_status, r_s.metadata)
            btree.insert(rec)
        for s_id in req.search_ids:
            btree.search(s_id)
        for d_id in req.delete_ids:
            btree.delete(d_id)
        btree_elapsed_ms = (time.perf_counter_ns() - btree_start) / 1_000_000

        # 2. Benchmark Red-Black Tree
        rbt_start = time.perf_counter_ns()
        for r_s in req.records:
            rec = DeviceRecord(r_s.device_id, r_s.device_name, r_s.network_location, r_s.device_category, r_s.operational_status, r_s.metadata)
            rbt.insert(rec)
        for s_id in req.search_ids:
            rbt.search(s_id)
        for d_id in req.delete_ids:
            rbt.delete(d_id)
        rbt_elapsed_ms = (time.perf_counter_ns() - rbt_start) / 1_000_000

        explanation = generate_explanation("module3_records", {
            "b_tree_order": t_val,
            "workload_type": f"{len(req.records)} inserts, {len(req.search_ids)} searches, {len(req.delete_ids)} deletes",
            "summary": (
                f"B-Tree (t={t_val}): {btree.key_comparisons} comparisons, {btree.splits_count} splits in {btree_elapsed_ms:.3f} ms. "
                f"Red-Black Tree: {rbt.key_comparisons} comparisons, {rbt.left_rotations + rbt.right_rotations} rotations in {rbt_elapsed_ms:.3f} ms."
            )
        })

        return ApiResponse(
            success=True,
            data={
                "b_tree": {
                    "minimum_degree": t_val,
                    "execution_time_ms": btree_elapsed_ms,
                    "key_comparisons": btree.key_comparisons,
                    "splits": btree.splits_count,
                    "merges": btree.merges_count,
                    "borrows": btree.borrows_count,
                    "invariants": btree.verify_invariants()
                },
                "red_black_tree": {
                    "execution_time_ms": rbt_elapsed_ms,
                    "key_comparisons": rbt.key_comparisons,
                    "left_rotations": rbt.left_rotations,
                    "right_rotations": rbt.right_rotations,
                    "total_rotations": rbt.left_rotations + rbt.right_rotations,
                    "recolorings": rbt.recolorings,
                    "invariants": rbt.verify_invariants()
                },
                "explanation": explanation.dict()
            },
            message="Identical workload executed across both tree data structures."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/binomial-heap/operations", response_model=ApiResponse)
def execute_binomial_heap_op(req: HeapOperationRequest):
    """Executes single operation on custom Binomial Heap."""
    global global_binomial_heap
    global_binomial_heap.reset_metrics()
    start_ns = time.perf_counter_ns()

    if req.operation == "insert":
        if not req.event:
            raise HTTPException(status_code=400, detail="event payload required.")
        evt = MaintenanceEvent(req.event.event_id, req.event.description, req.event.priority, req.event.network_location, req.event.created_at)
        global_binomial_heap.insert(evt)
        elapsed = (time.perf_counter_ns() - start_ns) / 1_000_000
        return ApiResponse(
            success=True,
            data={"size": global_binomial_heap.size, "links": global_binomial_heap.links_count, "execution_time_ms": elapsed},
            message=f"Event '{evt.event_id}' inserted into Binomial Heap."
        )

    elif req.operation == "find_min":
        min_node = global_binomial_heap.find_min()
        elapsed = (time.perf_counter_ns() - start_ns) / 1_000_000
        return ApiResponse(
            success=True,
            data={
                "event": min_node.event.to_dict() if min_node else None,
                "priority": min_node.key if min_node else None,
                "execution_time_ms": elapsed
            },
            message="Minimum urgency event located."
        )

    elif req.operation == "extract_min":
        min_evt = global_binomial_heap.extract_min()
        elapsed = (time.perf_counter_ns() - start_ns) / 1_000_000
        return ApiResponse(
            success=True,
            data={
                "extracted_event": min_evt.to_dict() if min_evt else None,
                "size_remaining": global_binomial_heap.size,
                "execution_time_ms": elapsed
            },
            message="Extracted minimum urgency event from Binomial Heap."
        )

    elif req.operation == "decrease_key":
        if not req.event_id or req.new_priority is None:
            raise HTTPException(status_code=400, detail="event_id and new_priority required.")
        success = global_binomial_heap.decrease_key(req.event_id, req.new_priority)
        elapsed = (time.perf_counter_ns() - start_ns) / 1_000_000
        return ApiResponse(
            success=True,
            data={"updated": success, "comparisons": global_binomial_heap.comparisons_count, "execution_time_ms": elapsed},
            message=f"Priority of event '{req.event_id}' decreased to {req.new_priority}."
        )

    elif req.operation == "get_all":
        events = [e.to_dict() for e in global_binomial_heap.get_all_events()]
        return ApiResponse(
            success=True,
            data={"events": events, "count": len(events)},
            message="Retrieved all events from Binomial Heap."
        )

    raise HTTPException(status_code=400, detail=f"Unsupported operation: {req.operation}")


@router.post("/fibonacci-heap/operations", response_model=ApiResponse)
def execute_fib_heap_op(req: HeapOperationRequest):
    """Executes single operation on custom Fibonacci Heap."""
    global global_fib_heap
    global_fib_heap.reset_metrics()
    start_ns = time.perf_counter_ns()

    if req.operation == "insert":
        if not req.event:
            raise HTTPException(status_code=400, detail="event payload required.")
        evt = MaintenanceEvent(req.event.event_id, req.event.description, req.event.priority, req.event.network_location, req.event.created_at)
        global_fib_heap.insert(evt)
        elapsed = (time.perf_counter_ns() - start_ns) / 1_000_000
        return ApiResponse(
            success=True,
            data={"total_nodes": global_fib_heap.total_nodes, "execution_time_ms": elapsed},
            message=f"Event '{evt.event_id}' inserted into Fibonacci Heap."
        )

    elif req.operation == "find_min":
        min_node = global_fib_heap.find_min()
        elapsed = (time.perf_counter_ns() - start_ns) / 1_000_000
        return ApiResponse(
            success=True,
            data={
                "event": min_node.event.to_dict() if min_node else None,
                "priority": min_node.key if min_node else None,
                "execution_time_ms": elapsed
            },
            message="Minimum urgency event located."
        )

    elif req.operation == "extract_min":
        min_evt = global_fib_heap.extract_min()
        elapsed = (time.perf_counter_ns() - start_ns) / 1_000_000
        return ApiResponse(
            success=True,
            data={
                "extracted_event": min_evt.to_dict() if min_evt else None,
                "total_nodes_remaining": global_fib_heap.total_nodes,
                "links": global_fib_heap.links_count,
                "execution_time_ms": elapsed
            },
            message="Extracted minimum urgency event from Fibonacci Heap."
        )

    elif req.operation == "decrease_key":
        if not req.event_id or req.new_priority is None:
            raise HTTPException(status_code=400, detail="event_id and new_priority required.")
        success = global_fib_heap.decrease_key(req.event_id, req.new_priority)
        elapsed = (time.perf_counter_ns() - start_ns) / 1_000_000
        return ApiResponse(
            success=True,
            data={
                "updated": success,
                "cuts": global_fib_heap.cuts_count,
                "cascading_cuts": global_fib_heap.cascading_cuts_count,
                "execution_time_ms": elapsed
            },
            message=f"Priority of event '{req.event_id}' decreased to {req.new_priority}."
        )

    elif req.operation == "get_all":
        events = [e.to_dict() for e in global_fib_heap.get_all_events()]
        return ApiResponse(
            success=True,
            data={"events": events, "count": len(events)},
            message="Retrieved all events from Fibonacci Heap."
        )

    raise HTTPException(status_code=400, detail=f"Unsupported operation: {req.operation}")


@router.post("/heaps/compare-workload", response_model=ApiResponse)
def compare_heap_workloads(req: HeapWorkloadRequest):
    """
    Executes identical sequence of Insert, Decrease-Key, and Extract-Min
    on both Binomial Heap and Fibonacci Heap, measuring operations and execution time.
    """
    try:
        b_heap = BinomialHeap()
        f_heap = FibonacciHeap()

        # 1. Binomial Heap workload
        b_start = time.perf_counter_ns()
        for e in req.events:
            evt = MaintenanceEvent(e.event_id, e.description, e.priority, e.network_location, e.created_at)
            b_heap.insert(evt)
        for dec in req.priority_decreases:
            try:
                b_heap.decrease_key(dec["event_id"], dec["new_priority"])
            except Exception:
                pass
        b_extracted = []
        for _ in range(req.extract_count or 2):
            ext = b_heap.extract_min()
            if ext:
                b_extracted.append(ext.to_dict())
        b_elapsed_ms = (time.perf_counter_ns() - b_start) / 1_000_000

        # 2. Fibonacci Heap workload
        f_start = time.perf_counter_ns()
        for e in req.events:
            evt = MaintenanceEvent(e.event_id, e.description, e.priority, e.network_location, e.created_at)
            f_heap.insert(evt)
        for dec in req.priority_decreases:
            try:
                f_heap.decrease_key(dec["event_id"], dec["new_priority"])
            except Exception:
                pass
        f_extracted = []
        for _ in range(req.extract_count or 2):
            ext = f_heap.extract_min()
            if ext:
                f_extracted.append(ext.to_dict())
        f_elapsed_ms = (time.perf_counter_ns() - f_start) / 1_000_000

        explanation = generate_explanation("module4_heaps", {
            "num_events": len(req.events),
            "decrease_key_frequency": "active",
            "summary": (
                f"Binomial Heap: {b_heap.links_count} links in {b_elapsed_ms:.3f} ms. "
                f"Fibonacci Heap: {f_heap.cuts_count} cuts, {f_heap.cascading_cuts_count} cascading cuts in {f_elapsed_ms:.3f} ms."
            )
        })

        return ApiResponse(
            success=True,
            data={
                "binomial_heap": {
                    "execution_time_ms": b_elapsed_ms,
                    "links_count": b_heap.links_count,
                    "merges_count": b_heap.merges_count,
                    "comparisons_count": b_heap.comparisons_count,
                    "extracted_events": b_extracted
                },
                "fibonacci_heap": {
                    "execution_time_ms": f_elapsed_ms,
                    "links_count": f_heap.links_count,
                    "cuts_count": f_heap.cuts_count,
                    "cascading_cuts_count": f_heap.cascading_cuts_count,
                    "comparisons_count": f_heap.comparisons_count,
                    "extracted_events": f_extracted
                },
                "explanation": explanation.dict()
            },
            message="Identical workload executed across both priority heap structures."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
