services = {
    21: "FTP",
    23: "Telnet",
    22: "SSH",
    53: "DNS",
    80: "HTTP",
    135: "RPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    1433: "MSSQL",
    3306: "MySQL",
    3389: "RDP",
    5000: "UPnP",
    8080: "HTTP-Alt",
    5357: "WSD (Web Services for Devices)",
    7680: "WUDO (Windows Update Delivery Optimization)"
}

availble_port = [80, 443, 22, 445, 8080, 8443, 554, 9000, 1883,23, 53, 135, 139, 143, 1433, 3389, 5000, 5357, 7680]

input_ip = "192.168.1"
#input_ip = input(f"Nhập vào dải ip cần scan (3 octet đầu):  ")