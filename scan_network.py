import socket, threading
from servicess import *
from datetime import datetime

thoi_gian = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
ten_file = f"report_{thoi_gian}.txt"
file_lock = threading.Lock()
# input_ip = "192.168.1"
input_ip = input(f"Nhập vào dải ip cần scan (3 octet đầu):  ")


#quet port
def scan_port(ip, port):
    try:
        #tạo 1 socket tcp
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        ket_qua = sock.connect_ex((ip, port)) #kiểm tra trạng thái kết nối với 1 ip, nếu ket_qua == 0 là đang kết nối/ ==1 là đóng hoặc bị chặn
        if ket_qua == 0:
            print(f"{ip} | Cổng {port} chạy dịch vụ {services.get(port, 'unknown')} đang mở!\n")
            kq = f"{ip} | Cổng {port} chạy dịch vụ {services.get(port, 'unknown')} đang mở!\n"
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

                                    

#tìm xem có bao nhiêu thiết bị
for i in range(1,255):
    ip= f"{input_ip}.{i}"
    scan_ip(ip)  

