"""
Adaptive Network Design and Optimization Framework
Hypothetical Demonstration Dataset
Contains realistic metropolitan network sites, hardware devices, maintenance events, and upgrade projects.
"""

from typing import List, Dict, Any

# Clear hypothetical disclaimer
SAMPLE_DATA_DISCLAIMER = (
    "All network nodes, links, IP addresses, maintenance tickets, and upgrade project costs "
    "are purely hypothetical demonstration data designed for Design and Analysis of Algorithms Course Project 4."
)

SAMPLE_VERTICES: List[Dict[str, Any]] = [
    {"id": "HQ-Core", "label": "HQ Central Core", "x": 450, "y": 300, "tier": "Core"},
    {"id": "East-DC", "label": "East Data Center", "x": 700, "y": 200, "tier": "Core"},
    {"id": "North-Hub", "label": "North Regional Hub", "x": 480, "y": 100, "tier": "Distribution"},
    {"id": "South-POP", "label": "South Edge POP", "x": 400, "y": 520, "tier": "Access"},
    {"id": "West-Subnet", "label": "West Enterprise Subnet", "x": 160, "y": 300, "tier": "Distribution"},
    {"id": "Tech-Park", "label": "Tech Park Branch", "x": 220, "y": 140, "tier": "Access"},
    {"id": "Metro-IX", "label": "Metro Exchange Point", "x": 680, "y": 450, "tier": "Distribution"},
    {"id": "Cloud-Edge", "label": "Cloud Gateway Edge", "x": 650, "y": 70, "tier": "Core"},
    {"id": "RD-Lab", "label": "R&D AI Cluster Lab", "x": 220, "y": 480, "tier": "Access"},
    {"id": "Disaster-DR", "label": "DR Secondary Bunker", "x": 800, "y": 330, "tier": "Distribution"},
]

SAMPLE_EDGES: List[Dict[str, Any]] = [
    {"source": "HQ-Core", "target": "North-Hub", "weight": 14.5, "bandwidth_gbps": 100.0},
    {"source": "HQ-Core", "target": "East-DC", "weight": 18.2, "bandwidth_gbps": 100.0},
    {"source": "HQ-Core", "target": "West-Subnet", "weight": 22.0, "bandwidth_gbps": 40.0},
    {"source": "HQ-Core", "target": "South-POP", "weight": 16.0, "bandwidth_gbps": 40.0},
    {"source": "North-Hub", "target": "Cloud-Edge", "weight": 12.0, "bandwidth_gbps": 100.0},
    {"source": "East-DC", "target": "Cloud-Edge", "weight": 11.5, "bandwidth_gbps": 100.0},
    {"source": "East-DC", "target": "Disaster-DR", "weight": 9.8, "bandwidth_gbps": 100.0},
    {"source": "East-DC", "target": "Metro-IX", "weight": 20.4, "bandwidth_gbps": 40.0},
    {"source": "South-POP", "target": "Metro-IX", "weight": 15.0, "bandwidth_gbps": 40.0},
    {"source": "South-POP", "target": "RD-Lab", "weight": 13.2, "bandwidth_gbps": 20.0},
    {"source": "West-Subnet", "target": "RD-Lab", "weight": 11.8, "bandwidth_gbps": 20.0},
    {"source": "West-Subnet", "target": "Tech-Park", "weight": 10.4, "bandwidth_gbps": 20.0},
    {"source": "North-Hub", "target": "Tech-Park", "weight": 19.1, "bandwidth_gbps": 20.0},
    {"source": "Metro-IX", "target": "Disaster-DR", "weight": 17.6, "bandwidth_gbps": 40.0},
    {"source": "HQ-Core", "target": "Metro-IX", "weight": 21.0, "bandwidth_gbps": 40.0},
]

SAMPLE_DEVICES: List[Dict[str, Any]] = [
    {
        "device_id": "DEV-1001",
        "device_name": "Cisco Nexus 9508 Core Director",
        "network_location": "HQ-Core",
        "device_category": "Router",
        "operational_status": "Active",
        "metadata": {"firmware": "NX-OS 10.3", "ports": 128, "ip": "10.0.0.1", "rack": "Rack-A1"}
    },
    {
        "device_id": "DEV-1002",
        "device_name": "Juniper PTX10008 Spine",
        "network_location": "East-DC",
        "device_category": "Router",
        "operational_status": "Active",
        "metadata": {"firmware": "Junos 23.2", "ports": 64, "ip": "10.0.1.1", "rack": "Rack-E2"}
    },
    {
        "device_id": "DEV-1003",
        "device_name": "Arista 7050SX3 Leaf Switch",
        "network_location": "West-Subnet",
        "device_category": "Switch",
        "operational_status": "Active",
        "metadata": {"firmware": "EOS 4.29", "ports": 48, "ip": "10.0.2.1", "rack": "Rack-W1"}
    },
    {
        "device_id": "DEV-1004",
        "device_name": "Palo Alto PA-5450 NextGen Firewall",
        "network_location": "North-Hub",
        "device_category": "Firewall",
        "operational_status": "Active",
        "metadata": {"firmware": "PAN-OS 11.1", "throughput_gbps": 120, "ip": "10.0.3.1", "rack": "Rack-N3"}
    },
    {
        "device_id": "DEV-1005",
        "device_name": "Cisco ASR 9904 BGP Peering Gateway",
        "network_location": "Metro-IX",
        "device_category": "Gateway",
        "operational_status": "Active",
        "metadata": {"firmware": "IOS-XR 7.9", "ports": 32, "ip": "10.0.4.1", "rack": "Rack-M1"}
    },
    {
        "device_id": "DEV-1006",
        "device_name": "Dell PowerEdge R760xa AI Inference Edge",
        "network_location": "RD-Lab",
        "device_category": "Edge Server",
        "operational_status": "Active",
        "metadata": {"gpu": "4x NVIDIA L40S", "cores": 64, "ip": "10.0.5.1", "rack": "Rack-R1"}
    },
    {
        "device_id": "DEV-1007",
        "device_name": "Fortinet FortiGate 3700F Carrier Firewall",
        "network_location": "Cloud-Edge",
        "device_category": "Firewall",
        "operational_status": "Active",
        "metadata": {"firmware": "FortiOS 7.4", "ports": 24, "ip": "10.0.6.1", "rack": "Rack-C1"}
    },
    {
        "device_id": "DEV-1008",
        "device_name": "HPE Aruba CX 8325 Aggregation Switch",
        "network_location": "South-POP",
        "device_category": "Switch",
        "operational_status": "Active",
        "metadata": {"firmware": "AOS-CX 10.12", "ports": 48, "ip": "10.0.7.1", "rack": "Rack-S2"}
    },
    {
        "device_id": "DEV-1009",
        "device_name": "Nokia 7750 SR-1 Optical Aggregator",
        "network_location": "Disaster-DR",
        "device_category": "Gateway",
        "operational_status": "Maintenance",
        "metadata": {"firmware": "SR OS 23.5", "ip": "10.0.8.1", "rack": "Rack-D1"}
    },
    {
        "device_id": "DEV-1010",
        "device_name": "Extreme Networks 5720 Access Switch",
        "network_location": "Tech-Park",
        "device_category": "Switch",
        "operational_status": "Active",
        "metadata": {"firmware": "SwitchEngine 32.2", "ports": 24, "ip": "10.0.9.1", "rack": "Rack-T1"}
    }
]

SAMPLE_MAINTENANCE_EVENTS: List[Dict[str, Any]] = [
    {
        "event_id": "EVT-301",
        "description": "Fiber optical splice degradation on East-DC to Disaster-DR trunk (attenuation > 4dB)",
        "priority": 1,  # P1 - Emergency
        "network_location": "East-DC",
        "created_at": "2026-10-13T08:15:00Z"
    },
    {
        "event_id": "EVT-302",
        "description": "BGP session flapping with upstream transit Tier-1 carrier",
        "priority": 2,  # P2 - Critical
        "network_location": "Metro-IX",
        "created_at": "2026-10-13T08:30:00Z"
    },
    {
        "event_id": "EVT-303",
        "description": "Redundant power supply unit (PSU 2) failure on core router",
        "priority": 3,  # P3 - High
        "network_location": "HQ-Core",
        "created_at": "2026-10-13T08:45:00Z"
    },
    {
        "event_id": "EVT-304",
        "description": "Cooling fan module thermal threshold alert in distribution rack",
        "priority": 4,  # P4 - Medium
        "network_location": "West-Subnet",
        "created_at": "2026-10-13T09:00:00Z"
    },
    {
        "event_id": "EVT-305",
        "description": "Firmware security patch CVE-2026-3841 staged for access switch stack",
        "priority": 5,  # P5 - Low / Scheduled
        "network_location": "Tech-Park",
        "created_at": "2026-10-13T09:15:00Z"
    },
    {
        "event_id": "EVT-306",
        "description": "Quarterly optical transceiver calibration & cleaning",
        "priority": 6,  # P6 - Routine
        "network_location": "RD-Lab",
        "created_at": "2026-10-13T09:30:00Z"
    }
]

SAMPLE_UPGRADE_PROJECTS: List[Dict[str, Any]] = [
    {
        "project_id": "PRJ-01",
        "project_name": "Metro Core 400Gbps ZR+ Coherent Optics Transceivers",
        "cost": 45000.0,
        "expected_benefit": 92.0,
        "divisibility": "indivisible"
    },
    {
        "project_id": "PRJ-02",
        "project_name": "Multi-Tenant Cloud Direct-Connect 100Gbps Cross-Connect",
        "cost": 30000.0,
        "expected_benefit": 75.0,
        "divisibility": "indivisible"
    },
    {
        "project_id": "PRJ-03",
        "project_name": "Zero-Trust Enterprise SASE Perimeter Firewall Cluster",
        "cost": 25000.0,
        "expected_benefit": 60.0,
        "divisibility": "indivisible"
    },
    {
        "project_id": "PRJ-04",
        "project_name": "Dedicated Submarine DWDM Leased Optical Spectrum (MHz Slices)",
        "cost": 50000.0,
        "expected_benefit": 110.0,
        "divisibility": "divisible"
    },
    {
        "project_id": "PRJ-05",
        "project_name": "Edge AI Inference Acceleration Blade for Packet Inspection",
        "cost": 20000.0,
        "expected_benefit": 42.0,
        "divisibility": "indivisible"
    },
    {
        "project_id": "PRJ-06",
        "project_name": "Burstable Tier-1 Internet Transit Bandwidth (Mbps Pool)",
        "cost": 15000.0,
        "expected_benefit": 38.0,
        "divisibility": "divisible"
    }
]
