import subprocess, re

def get_local_ip():
    try:
        result = subprocess.run(
            ["ipconfig"],
            capture_output=True, text = True
        )

        ips = re.findall(r"IPv4.*?:\s*(192\.168\.\d+\.\d+)",result.stdout)
        if ips:
            parts = ips[0].split(".")
            return f"{parts[0]}.{parts[1]}.{parts[2]}"
        
    except:
        return None