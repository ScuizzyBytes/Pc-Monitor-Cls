import psutil

class SystemMonitor:
    def __init__(self):
        pass

    def cpu_info(self):
        return {
            "overall": psutil.cpu_percent(interval=None),
            "cores": psutil.cpu_percent(percpu=True)
        }

    def get_ram_info(self):
        ram = psutil.virtual_memory()
        return {
            "percent": ram.percent,
            "used_gb": round(ram.used / (1024 * 3), 2),
            "total_gb": round(ram.total / (1024 * 3), 2)
        }

    def get_disk_info(self):
        disk = psutil.disk_usage("/")
        return {
            "percent": disk.percent,
            "used_gb": round(disk.used / (1024 * 3), 2),
            "total_gb": round(disk.total / (1024 * 3), 2)
        }

    def get_top_processes(self, limit = 5):
        process = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                process.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        sorted_procs = sorted(process, key=lambda p: p['memory_percent'] or 0, reverse=True)
        return sorted_procs[:limit]
                
