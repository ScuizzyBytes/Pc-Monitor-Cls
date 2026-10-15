# 🖥️ PC-Monitor Cls (Hardware Telemetry Engine)

A lightweight, high-performance Python system monitoring engine designed for real-time hardware telemetry ingestion. Built to run inside isolated background workers, it provides non-blocking data feeds for user interfaces, HUDs, and system dashboards.

---

## 📐 Architecture & Core Concepts

1. **Zero UI Blocking:** Designed specifically to run inside secondary background threads (`threading.Thread`) or thread pools.
2. **Atomic Metric Collection:** CPU, RAM, Disk, and Network stats are gathered on demand in isolated, dictionary-formatted data payloads.
3. **Cross-Platform Compatibility:** Utilizes standard OS hooks via `psutil` to deliver unified hardware metrics across Windows, Linux, and macOS.

---

## 📂 System Integration Structure

```
cyberpunk-hud/
│
├── system_monitor.py      # Contains PC-Monitor Cls (Telemetry Engine)             # CustomTkinter interface listening for updates
└── main.py                # Application entry point
```

---

## ⚡ Data Payload Specification

When queried, the monitor class yields structured dictionaries ready for immediate dispatch to the main thread:

```python
{
    "cpu_percent": 24.5,
    "ram_percent": 68.2,
    "ram_used_gb": 10.9,
    "ram_total_gb": 16.0,
    "disk_percent": 45.0,
    "network_sent_mb": 120.4,
    "network_recv_mb": 450.8
}
```

---

## 🛠️ Requirements & Setup

### Install Dependency
```bash
pip install psutil
```

---

## 🔄 Integration Workflow

```
[ Hardware Layer ]
       │
       ▼
[ PC-Monitor Cls ]  <--- (Queries CPU / RAM / Disk / Net)
       │
       ▼
[ Background Worker ]  --->  [ queue.Queue / self.after ]  --->  [ CustomTkinter HUD UI ]
```

1. Instantiate `SystemMonitor` once during thread bootstrap.
2. Poll `get_telemetry()` on each background worker cycle.
3. Pass the resulting dictionary payload safely to the UI thread using `self.after(0, update_callback, payload)`.

---

## 🚀 Key Metric Features

* **CPU Utilization:** Global or per-core percentage sampling.
* **RAM Footprint:** Active percentage along with absolute GB allocations.
* **Storage Metrics:** Disk partition load and availability statistics.
* **Network I/O:** Real-time throughput (bytes sent / received).
