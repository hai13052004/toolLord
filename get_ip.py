import subprocess, re, platform

def get_local_ip():
    try:
        system = platform.system()
        
        if system == "Windows":
            result = subprocess.run(["ipconfig"], capture_output=True, text=True).stdout
            adapters = re.split(r'\n(?=[^\s])', result)
            
            for adapter in adapters:
            
                if "VMware" in adapter or "Virtual" in adapter:
                    continue
                
                ip_match = re.search(r"IPv4.*?:\s*([\d.]+)", adapter)
                if ip_match:
                    ip = ip_match.group(1)
                    if not ip.startswith("127."):
                        parts = ip.split(".")
                        return f"{parts[0]}.{parts[1]}.{parts[2]}"

        else:
            cmd = ["ip", "-4", "addr", "show"] if system == "Linux" else ["ifconfig"]
            result = subprocess.run(cmd, capture_output=True, text=True).stdout
            interfaces = re.split(r'\n\d+: ', result) if system == "Linux" else re.split(r'\n(?=[^\s])', result)
            
            for iface in interfaces:
                if "vmnet" in iface or "lo" in iface or "docker" in iface:
                    continue
                
                ip_match = re.search(r'inet\s+(?:addr:)?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', iface)
                if ip_match:
                    ip = ip_match.group(1)
                    parts = ip.split(".")
                    return f"{parts[0]}.{parts[1]}.{parts[2]}"
                
    except Exception:
        return None
    return None

print(f"Dải IP: {get_local_ip()}")