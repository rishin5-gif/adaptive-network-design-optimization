"""
Adaptive Network Design and Optimization Framework
SQLite Database Access Layer
Provides clean relational persistence for network topologies, device inventories,
maintenance events, upgrade projects, and experiment logs.
"""

import sqlite3
import json
import os
from typing import List, Dict, Any, Optional
from .data.sample_data import (
    SAMPLE_VERTICES,
    SAMPLE_EDGES,
    SAMPLE_DEVICES,
    SAMPLE_MAINTENANCE_EVENTS,
    SAMPLE_UPGRADE_PROJECTS
)

DB_PATH = os.path.join(os.path.dirname(__file__), "network_framework.db")


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes tables and seeds default hypothetical sample data if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS vertices (
        id TEXT PRIMARY KEY,
        label TEXT NOT NULL,
        x REAL,
        y REAL,
        tier TEXT DEFAULT 'Distribution'
    );

    CREATE TABLE IF NOT EXISTS edges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        target TEXT NOT NULL,
        weight REAL NOT NULL,
        bandwidth_gbps REAL DEFAULT 10.0,
        FOREIGN KEY (source) REFERENCES vertices(id) ON DELETE CASCADE,
        FOREIGN KEY (target) REFERENCES vertices(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS device_records (
        device_id TEXT PRIMARY KEY,
        device_name TEXT NOT NULL,
        network_location TEXT NOT NULL,
        device_category TEXT NOT NULL,
        operational_status TEXT NOT NULL,
        metadata_json TEXT DEFAULT '{}'
    );

    CREATE TABLE IF NOT EXISTS maintenance_events (
        event_id TEXT PRIMARY KEY,
        description TEXT NOT NULL,
        priority INTEGER NOT NULL,
        network_location TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS upgrade_projects (
        project_id TEXT PRIMARY KEY,
        project_name TEXT NOT NULL,
        cost REAL NOT NULL,
        expected_benefit REAL NOT NULL,
        divisibility TEXT DEFAULT 'indivisible'
    );

    CREATE TABLE IF NOT EXISTS experiment_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        experiment_family TEXT NOT NULL,
        params_json TEXT NOT NULL,
        results_json TEXT NOT NULL,
        execution_timestamp TEXT NOT NULL
    );
    """)

    conn.commit()

    # Check if empty; if so, seed sample data
    cursor.execute("SELECT COUNT(*) FROM vertices")
    if cursor.fetchone()[0] == 0:
        seed_sample_data(conn)
    else:
        conn.close()


def seed_sample_data(conn: Optional[sqlite3.Connection] = None):
    """Populates or resets the database to the clean demonstration dataset."""
    close_after = False
    if conn is None:
        conn = get_db_connection()
        close_after = True

    cursor = conn.cursor()
    cursor.execute("DELETE FROM edges")
    cursor.execute("DELETE FROM vertices")
    cursor.execute("DELETE FROM device_records")
    cursor.execute("DELETE FROM maintenance_events")
    cursor.execute("DELETE FROM upgrade_projects")

    for v in SAMPLE_VERTICES:
        cursor.execute(
            "INSERT INTO vertices (id, label, x, y, tier) VALUES (?, ?, ?, ?, ?)",
            (v["id"], v["label"], v["x"], v["y"], v["tier"])
        )

    for e in SAMPLE_EDGES:
        cursor.execute(
            "INSERT INTO edges (source, target, weight, bandwidth_gbps) VALUES (?, ?, ?, ?)",
            (e["source"], e["target"], e["weight"], e["bandwidth_gbps"])
        )

    for d in SAMPLE_DEVICES:
        cursor.execute(
            "INSERT INTO device_records (device_id, device_name, network_location, device_category, operational_status, metadata_json) VALUES (?, ?, ?, ?, ?, ?)",
            (d["device_id"], d["device_name"], d["network_location"], d["device_category"], d["operational_status"], json.dumps(d.get("metadata", {})))
        )

    for m in SAMPLE_MAINTENANCE_EVENTS:
        cursor.execute(
            "INSERT INTO maintenance_events (event_id, description, priority, network_location, created_at) VALUES (?, ?, ?, ?, ?)",
            (m["event_id"], m["description"], m["priority"], m["network_location"], m["created_at"])
        )

    for u in SAMPLE_UPGRADE_PROJECTS:
        cursor.execute(
            "INSERT INTO upgrade_projects (project_id, project_name, cost, expected_benefit, divisibility) VALUES (?, ?, ?, ?, ?)",
            (u["project_id"], u["project_name"], u["cost"], u["expected_benefit"], u["divisibility"])
        )

    conn.commit()
    if close_after:
        conn.close()


# Database Queries
def get_all_vertices() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT id, label, x, y, tier FROM vertices ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_edges() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT id, source, target, weight, bandwidth_gbps FROM edges").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_devices() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT device_id, device_name, network_location, device_category, operational_status, metadata_json FROM device_records ORDER BY device_id").fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        d["metadata"] = json.loads(d.pop("metadata_json", "{}"))
        results.append(d)
    return results


def get_all_maintenance_events() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT event_id, description, priority, network_location, created_at FROM maintenance_events ORDER BY priority ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_upgrade_projects() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT project_id, project_name, cost, expected_benefit, divisibility FROM upgrade_projects ORDER BY project_id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def save_experiment_run(family: str, params: Dict[str, Any], results: Dict[str, Any], timestamp: str):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO experiment_history (experiment_family, params_json, results_json, execution_timestamp) VALUES (?, ?, ?, ?)",
        (family, json.dumps(params), json.dumps(results), timestamp)
    )
    conn.commit()
    conn.close()


def get_recent_experiments(limit: int = 20) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT id, experiment_family, params_json, results_json, execution_timestamp FROM experiment_history ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "experiment_family": r["experiment_family"],
            "params": json.loads(r["params_json"]),
            "results": json.loads(r["results_json"]),
            "execution_timestamp": r["execution_timestamp"]
        })
    return results


# Auto-initialize SQLite database on module import
init_db()
