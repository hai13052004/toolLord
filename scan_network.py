import socket, threading, time, subprocess, re
from servicess import *
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

console = Console()
console.print(Panel.fit("[bold cyan]NETWORK PORT SCANNER[/bold cyan]\n[white]v1.0[/white]",
    border_style="cyan"))

thoi_gian = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
ten_file = f"report_{thoi_gian}.txt"
file_lock = threading.Lock()

#quet port
def scan_port(ip, port):
    try:
        start = time.time()
        #tạo 1 socket tcp
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        ket_qua = sock.connect_ex((ip, port)) #kiểm tra trạng thái kết nối với 1 ip, nếu ket_qua == 0 là đang kết nối/ ==1 là đóng hoặc bị chặn
        elapsed = round((time.time()-start)*1000)
        if ket_qua == 0:
            console.print(f"[green]✓[/green] [white]{ip}[/white] | [green] {detect_os(ip) } [/green] | [white]{get_hostname(ip)}[/white] | [yellow]{banner_grab(ip, port)}[/yellow] | [cyan]Port {port}[/cyan] | [yellow]{services.get(port, 'Unknown')}[/yellow] | [red] {elapsed}ms[/red]")
            kq = f"{ip} | {detect_os(ip)} | {port} | {get_hostname(ip)} | {banner_grab(ip, port)} | {services.get(port, 'unknown')} | {elapsed}ms \n"
            with file_lock: 
                with open(f"{ten_file}", "a", encoding="utf-8") as f:
                    f.write(kq)
    except Exception as e:
        # print(f"Lỗi: {e}")
        pass
def scan_ip(ip):
    threads=[]
    for a_p in availble_port:
        p = threading.Thread(target=scan_port,args=(ip,a_p))
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
            return banner.strip().split("\n")[0]
    except:
        return "N/A"

def detect_os(ip):
    try:
        result = subprocess.run(
            ["ping", "-n" , "1", "-w", "1000", ip],
            capture_output=True, text = True
        )
        ttl=re.search(r"TTL=(\d+)",result.stdout, re.IGNORECASE)
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
    console.print(f"\n[bold white]Đang scan {ip}/24...[/bold white]\n")
    scan_ip(ip)  

