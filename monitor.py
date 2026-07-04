import platform
import socket
import psutil
from datetime import datetime

def get_system_info():
    """Vrací statické informace o systému s anonymizovanou IP adresou."""
    ip_address = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
    except Exception:
        pass

    # Anonymizace IP adresy (maskování posledních dvou oktetů)
    try:
        ip_parts = ip_address.split('.')
        if len(ip_parts) == 4:
            anonymized_ip = f"{ip_parts[0]}.{ip_parts[1]}.X.X"
        else:
            anonymized_ip = "Unknown"
    except Exception:
        anonymized_ip = "Unknown"

    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "hostname": socket.gethostname(),
        "cpu_count": psutil.cpu_count(logical=True),
        "cpu_freq": round(psutil.cpu_freq().max if psutil.cpu_freq() else 0),
        "ip_address": anonymized_ip
    }

def get_live_metrics():
    """Vrací dynamické metriky zatížení systému."""
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('C:')
    
    # Výpočet Uptime
    boot_time = psutil.boot_time()
    uptime_seconds = datetime.now().timestamp() - boot_time
    
    days = int(uptime_seconds // 86400)
    hours = int((uptime_seconds % 86400) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    uptime_str = f"{days}d {hours}h {minutes}m" if days > 0 else f"{hours}h {minutes}m"

    # Stav baterie
    battery = psutil.sensors_battery()
    if battery:
        battery_pct = round(battery.percent)
        battery_plugged = "Nabíjí se" if battery.power_plugged else "Vybíjí se"
        battery_str = f"{battery_pct}% ({battery_plugged})"
    else:
        battery_str = "Není k dispozici (Stolní PC)"

    return {
        "cpu_usage": psutil.cpu_percent(interval=None),
        "ram_usage": mem.percent,
        "ram_used_gb": round(mem.used / (1024**3), 2),
        "ram_total_gb": round(mem.total / (1024**3), 2),
        "disk_usage": disk.percent,
        "disk_used_gb": round(disk.used / (1024**3), 2),
        "disk_total_gb": round(disk.total / (1024**3), 2),
        "uptime": uptime_str,
        "battery": battery_str
    }
