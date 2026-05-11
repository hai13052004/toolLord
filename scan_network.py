import socket, threading
from servicess import *
device_done = []
input_ip = input("Nhập vào dải ip cần scan (192.168.x):  ")

availble_port = [80, 443, 22, 445, 8080, 8443, 554, 9000, 1883]
#quet port
def scan_port(ip, port):
    try:
        #tạo 1 socket tcp
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        ket_qua = sock.connect_ex((ip, port)) #kiểm tra trạng thái kết nối với 1 ip, nếu ket_qua == 0 là đang kết nối/ ==1 là đóng hoặc bị chặn
        if ket_qua == 0:
            print(f"{ip} | Cổng {port} chạy dịch vụ {services.get(port, 'unknown')} đang mở!")
            
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

