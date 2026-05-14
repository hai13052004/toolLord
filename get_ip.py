import subprocess, re,platform

def get_local_ip():
    try:
        system = platform.system()
        if system == "Windows":
            result = subprocess.run(["ipconfig"],capture_output=True, text = True)
            wifi_match = re.search(r"Wi-Fi.*?IPv4.*?:\s*([\d.]+)",result.stdout, re.DOTALL)
            if wifi_match:
                parts = wifi_match.group(1).split(".")
                return f"{parts[0]}.{parts[1]}.{parts[2]}"
        elif system == "Darwin":
            result = subprocess.run(["ifconfig"], capture_output=True, text=True)
            ip = re.search(r"inet (192\.168\.\d+)\.\d+", result.stdout)
            if ip:
                return ip.group(1)
        else:
            result = subprocess.run(["ip", "a"], capture_output=True, text=True)
            ip = re.search(r"inet (192\.168\.\d+)\.\d+", result.stdout)
            if ip:
                return ip.group(1)
                
    except:
        return None
    
print(get_local_ip())