import socket
import time
UDP_IP = bytes("172.23.157.80", 'utf-8')
UDP_PORT = 5006
address ="www.aut.ac.ir"
port = str(80)
MESSAGE = bytes(address + '@' + port + '@GET / HTTP/1.0\r\n\r\n'
                , 'utf-8')



for i in range(1, 2):
    time.sleep(1)
    print("UDP target IP:", UDP_IP)
    print("UDP target port:", UDP_PORT)
    print("message:", MESSAGE)
    sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sock.close()

while True :
    UDP_PORT = 5007
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))
    data, addr = sock.recvfrom(1024)
    print("received data:", data)
    sock.close()
    break

