import socket, threading, time, subprocess, re, platform ,os
from servicess import *
from call_nvd import *
from get_ip import *
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

print("Chọn chế độ scan:\n [1] Tự động phát hiện IP\n [2] Nhập IP thủ công\n [3] Dùng IP đã thiết lập sẵn")
input_ip = ""
choice = input("Chọn chế độ [1/2/3]: ")
if choice == "1":
    input_ip = get_local_ip()
elif choice == "2":
    input_ip = input("Nhập dải IP (3 octet đầu): ")
elif choice == "3":
    input_ip = "192.168.1"

console = Console()
console.print(Panel.fit("[bold cyan]NETWORK PORT SCANNER[/bold cyan]\n[white]v1.0[/white]",
    border_style="cyan"))

thoi_gian = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


report_folder = "reports"
if not os.path.exists(report_folder):
    os.makedirs(report_folder)
ten_file = f"{report_folder}/report_{thoi_gian}.txt"
file_lock = threading.Lock()

#quet port
def scan_port(ip, port, os_info):
    try:
        start = time.time()
        #tạo 1 socket tcp
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        ket_qua = sock.connect_ex((ip, port)) #kiểm tra trạng thái kết nối với 1 ip, nếu ket_qua == 0 là đang kết nối/ ==1 là đóng hoặc bị chặn
        elapsed = round((time.time()-start)*1000)
        if ket_qua == 0:
            banner = banner_grab(ip, port)
            vuln = check_vuln(banner) if banner != "N/A" else "N/A"
            console.print(f"[green]✓[/green] [white]{ip} | {os_info} [/white] | [cyan]Port {port}[/cyan] | [white]{get_hostname(ip)}[/white] | [yellow]{banner}[/yellow]  | [yellow]{services.get(port, 'Unknown')}[/yellow] | [red] {elapsed}ms[/red]")
            
            kq = f"{ip} | {os_info} | {port} | {get_hostname(ip)} | {banner}| {services.get(port, 'unknown')} | {elapsed}ms \n"
            if vuln != "N/A" and vuln!="không tìm thấy CVE":
                console.print(f"  [red]⚠ {vuln}[/red]")
                kq += f"\n ⚠ {vuln}"
            kq +="\n"
            with file_lock: 
                with open(f"{ten_file}", "a", encoding="utf-8") as f:
                    f.write(kq)
    except Exception as e:
        # print(f"Lỗi: {e}")
        pass
def scan_ip(ip):
    os_info = detect_os(ip)
    threads=[]
    for a_p in availble_port:
        p = threading.Thread(target=scan_port,args=(ip, a_p, os_info))
        threads.append(p)
        p.start()
        
    for oke in threads:
        oke.join()

#check device
def get_hostname(ip):
    try:
        hostname =  socket.gethostbyaddr(ip)[0]
        return hostname
    except:
        return "Unknown"

#check info
def banner_grab(ip, port):
    try:    
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            sock.connect((ip, port))
            if port in [80,8080]:
                sock.send(b"GET / HTTP/1.0\r\n\r\n")
            banner = sock.recv(1024).decode(errors="ignore")
            #print(f"{banner}")
            return banner.strip().split("\n")[0]
    except:
        return "N/A"

def detect_os(ip):
    try:
        if platform.system() == "Windows":
            cmd = ["ping", "-n", "1", "-w", "1000", ip]
        else:  # Linux / macOS / Termux
            cmd = ["ping", "-c", "1", "-W", "1", ip]
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        ttl = re.search(r"TTL=(\d+)", result.stdout, re.IGNORECASE)
        if ttl:
            ttl_val = int(ttl.group(1))
            if ttl_val >= 128:
                return "Windows"
            elif ttl_val >= 64:
                return "Linux/Mac/Router"
            else:
                return "Network Device"
        return "Unknown"
    except:
        return "Unknown"                                    

#tìm xem có bao nhiêu thiết bị
for i in range(1,255):
    ip= f"{input_ip}.{i}"
    console.print(f"\n[bold white]Đang scan {ip}/24...[/bold white]")
    scan_ip(ip)  
    

