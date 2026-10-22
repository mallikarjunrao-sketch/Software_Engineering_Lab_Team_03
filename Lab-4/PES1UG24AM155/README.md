# Traffic Classification System — SDN Mininet Project

**Student:** 31PES1UG24AM155 — MALLIKARJUNA RAO R V  
**Project:** V9 — Traffic Classification System  
**Course:** SDN Mininet-based Simulation (Orange Problem)

---

## Problem Statement

Classify network traffic based on protocol type using an SDN controller.  
The system identifies TCP, UDP, and ICMP packets in real-time, maintains per-protocol statistics, and displays traffic distribution using a live web dashboard.

---

## Topology

```
h1 (10.0.0.1) ─┐
h2 (10.0.0.2) ─┤── [OVS Switch s1] ──── [Ryu Controller :6633]
h3 (10.0.0.3) ─┘
```

- **3 hosts**, **1 OVS switch**, **1 remote Ryu controller**
- OpenFlow 1.3
- Links: 100 Mbps, 5 ms delay

---

## Features

- ✅ Classifies TCP, UDP, ICMP, and OTHER packets on every `packet_in`
- ✅ Installs proactive per-flow rules (match on IP + protocol + ports)
- ✅ MAC learning switch (no flooding after first packet)
- ✅ Per-protocol packet count, byte count, percentage
- ✅ REST API at `http://localhost:8080/stats`
- ✅ Live browser dashboard (`dashboard.html`)
- ✅ Flow log of last 50 classified packets

---

## Setup & Execution

### Prerequisites

```bash
sudo apt install mininet openvswitch-switch python3-pip -y
pip3 install ryu
```

### Step 1 — Start the Ryu Controller

```bash
ryu-manager traffic_classifier.py --observe-links --wsapi-port 8080
```

You should see:
```
=== Traffic Classification System Started ===
Dashboard available at: http://localhost:8080/stats
```

### Step 2 — Start Mininet Topology (new terminal)

```bash
sudo python3 topology.py
```

### Step 3 — Run Test Scenarios in Mininet CLI

**ICMP (Scenario 1):**
```
mininet> h1 ping -c 10 h2
mininet> h3 ping -c 5 h1
```

**TCP (Scenario 2):**
```
mininet> h2 iperf -s &
mininet> h1 iperf -c 10.0.0.2 -t 10
```

**UDP (Scenario 3):**
```
mininet> h3 iperf -u -s &
mininet> h1 iperf -u -c 10.0.0.3 -b 10M -t 10
```

**Mixed Traffic (Scenario 4):**
```
mininet> h2 iperf -s -D
mininet> h3 iperf -u -s -D
mininet> h1 ping -c 20 h2 &
mininet> h1 iperf -c 10.0.0.2 -t 15 &
mininet> h1 iperf -u -c 10.0.0.3 -b 5M -t 15
```

### Step 4 — View Statistics

**REST API:**
```bash
curl http://localhost:8080/stats
```

**Browser Dashboard:**  
Open `dashboard.html` in a browser (auto-refreshes every 2s).

**Flow Table:**
```bash
sudo ovs-ofctl -O OpenFlow13 dump-flows s1
sudo ovs-ofctl -O OpenFlow13 dump-ports s1
```

---

## Expected Output

### REST API Response
```json
{
  "uptime_seconds": 42.1,
  "total_packets": 87,
  "protocols": {
    "TCP":  { "count": 45, "bytes": 58320, "percent": 51.7 },
    "UDP":  { "count": 30, "bytes": 43200, "percent": 34.5 },
    "ICMP": { "count": 10, "bytes": 840,   "percent": 11.5 },
    "OTHER":{ "count": 2,  "bytes": 240,   "percent": 2.3  }
  },
  "recent_flows": [...]
}
```

### Flow Table (after traffic)
```
cookie=0x0, duration=5s, priority=10, tcp,
  nw_src=10.0.0.1,nw_dst=10.0.0.2,tp_src=5001,tp_dst=57234
  actions=output:"s1-eth2"
```

---

## Test Scenarios

| Scenario | Traffic Type | Expected Result |
|----------|-------------|----------------|
| 1 | ICMP ping h1→h2 | ICMP counter increments, echo reply seen |
| 2 | TCP iperf h1→h2 | TCP counter increments, flow rule installed |
| 3 | UDP iperf h1→h3 | UDP counter increments, separate flow rule |
| 4 | All mixed | Distribution across all 3 protocols shown |

---

## SDN Concepts Demonstrated

| Concept | Implementation |
|---------|---------------|
| Controller–switch interaction | `packet_in` events handled by Ryu |
| Match–action rules | OpenFlow rules match IP proto + ports |
| Flow rule installation | `OFPFlowMod` with priority 10, idle_timeout 30s |
| MAC learning | `mac_to_port` table per datapath |
| Traffic analysis | Per-protocol byte and packet counters |

---

## References

1. Ryu SDN Framework Documentation — https://ryu.readthedocs.io
2. OpenFlow 1.3 Specification — https://opennetworking.org/wp-content/uploads/2014/10/openflow-spec-v1.3.0.pdf
3. Mininet Documentation — http://mininet.org/docs/
4. Open vSwitch Documentation — https://docs.openvswitch.org
5. B. Lantz, B. Heller, N. McKeown, "A Network in a Laptop," HotNets 2010
