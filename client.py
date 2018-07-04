import socket
import time
UDP_IP = bytes("172.23.157.80", 'utf-8')
timeout = 50
address ="www.ceit.aut.ac.ir"
port = str(80)
NS = 0
MF = 0  # More fragment
iteration = 2
data = 'GET / HTTP/1.0\r\n\r\n'

def checksum(MESSAGE) :
    c = 0

    for x in MESSAGE:
        c = c + ord(x)
    checksum = bin(c)
    checksum = checksum.split('b')

    return checksum[1]


if len(data) > 65000:
    iteration = len(data)/65000 + 2
    MF = 1


for i in range(1, iteration):
    UDP_PORT = 5016
    if i == iteration - 1:
        MF = 0
    print("UDP target IP:", UDP_IP)
    print("UDP target port:", UDP_PORT)
    start = (i-1) * 65000
    end = i * 65000
    msg =   address + '@' + port + '@' + str(NS) + '@' + str(MF) + '@' + data[start:end]
    # MESSAGE = bytes(msg, 'utf-8')

    print('HERE' , msg)
    cmsg = msg.split('\r\n\r\n')
    print(cmsg[0])
    checksum = checksum(cmsg[0])
    newmsg = msg + '@' + str(checksum)
    MESSAGE = bytes(newmsg, 'utf-8')


    print("message with checksum :", MESSAGE)
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sock.close()
    while True:
        UDP_PORT = 5008
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.bind((UDP_IP, UDP_PORT))
        sock.settimeout(0.00001)
        data, addr = sock.recvfrom(1024)
        if not data :
            print("timeout")
        NR = int(data)
        print("ack : ", NR , NS)
        sock.close()
        if NR == int(not bool(NS)):
            NS = NR
            break
        else:
            UDP_PORT = 5016
            sock = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            sock.close()

        print("received data:", NR)

while True:
    print("here")
    UDP_PORT = 5007
    sock = socket.socket(socket.AF_INET,  # Internet
                           socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))
    data, addr = sock.recvfrom(1024)
    print("received data:", data)
    sock.close()
    break

