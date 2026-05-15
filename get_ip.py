import subprocess, re, platform

def get_local_ip():
    try:
        system = platform.system()
        
        
        if system == "Windows":
            result = subprocess.run(["ipconfig"], capture_output=True, text=True).stdout
            adapters = re.split(r'\n(?=[^\s])', result)
            for adapter in adapters:
                
                if any(x in adapter for x in ["VMware", "Virtual", "vboxnet"]):
                    continue
                
                ip_match = re.search(r"IPv4.*?:\s*([\d.]+)", adapter)
                if ip_match:
                    ip = ip_match.group(1)
                    if not ip.startswith("127."):
                        parts = ip.split(".")
                        return f"{parts[0]}.{parts[1]}.{parts[2]}"

        else:
            gw = subprocess.run(["ip", "route"], capture_output=True, text=True).stdout
            gw_match = re.search(r"default via ([\d.]+)", gw)
            if gw_match:
                gw_ip = gw_match.group(1)
                gw_prefix = ".".join(gw_ip.split(".")[:3])
                result = subprocess.run(["ip", "-4", "addr", "show"], capture_output=True, text=True).stdout
                all_ips = re.findall(r'inet\s+([\d.]+)', result)
                for ip in all_ips:
                    if ip.startswith(gw_prefix):
                        parts = ip.split(".")
                        return f"{parts[0]}.{parts[1]}.{parts[2]}"
                
    except Exception:
        return None
    return None

print(f"Dải IP xác định được: {get_local_ip()}")