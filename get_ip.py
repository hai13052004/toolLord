import subprocess, re, platform

def get_local_ip():
    try:
        system = platform.system()
        
        # TRƯỜNG HỢP WINDOWS
        if system == "Windows":
            result = subprocess.run(["ipconfig"], capture_output=True, text=True).stdout
            adapters = re.split(r'\n(?=[^\s])', result)
            for adapter in adapters:
                # Lọc bỏ VMware và VirtualBox
                if any(x in adapter for x in ["VMware", "Virtual", "vboxnet"]):
                    continue
                # Tìm IPv4 trong adapter còn lại
                ip_match = re.search(r"IPv4.*?:\s*([\d.]+)", adapter)
                if ip_match:
                    ip = ip_match.group(1)
                    if not ip.startswith("127."):
                        parts = ip.split(".")
                        return f"{parts[0]}.{parts[1]}.{parts[2]}"

        else:
            cmd = ["ip", "-4", "addr", "show"] if system == "Linux" else ["ifconfig"]
            result = subprocess.run(cmd, capture_output=True, text=True).stdout
            
            # ƯU TIÊN: Tìm giao diện wlan0 (Wifi trên Android/Termux) trước
            wlan_match = re.search(r'wlan0.*?inet\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', result, re.DOTALL)
            if wlan_match:
                ip = wlan_match.group(1)
                parts = ip.split(".")
                return f"{parts[0]}.{parts[1]}.{parts[2]}"

            # NẾU KHÔNG CÓ WLAN0: Tìm các giao diện khác nhưng loại bỏ đồ ảo
            interfaces = re.split(r'\n\d+: ', result) if system == "Linux" else re.split(r'\n(?=[^\s])', result)
            for iface in interfaces:
                # Bỏ qua loopback và các card ảo phổ biến
                if any(x in iface for x in ["lo", "vmnet", "docker", "vboxnet", "dummy"]):
                    continue
                
                ip_match = re.search(r'inet\s+(?:addr:)?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', iface)
                if ip_match:
                    ip = ip_match.group(1)
                    parts = ip.split(".")
                    return f"{parts[0]}.{parts[1]}.{parts[2]}"
                
    except Exception:
        return None
    return None

print(f"Dải IP xác định được: {get_local_ip()}")