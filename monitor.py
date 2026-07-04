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
