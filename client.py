import socket
import time
import requests

turn = 0
IP = '192.168.1.33'
# IP = '192.168.1.55'



if turn:
    UDP_IP = bytes(IP, 'utf-8')
    timeout = 50
    address = 'www.google.com'
    port = str(80)
    NS = 0
    MF = 0  # More fragment
    iteration = 2
    data = 'GET / HTTP/1.0\r\n\r\n'
    newdata = ''


    def checksum1(MESSAGE):
        c = 0

        for x in MESSAGE:
            c = c + ord(x)
        checksum = bin(c)
        checksum = checksum.split('b')

        return checksum[1]


    if len(data) > 65000:
        iteration = len(data) / 65000 + 2
        MF = 1

    for i in range(1, iteration):
        UDP_PORT = 5016
        if i == iteration - 1:
            MF = 0
        print('UDP target IP:', UDP_IP)
        print('UDP target port:', UDP_PORT)
        start = (i - 1) * 65000
        end = i * 65000
        msg = address + '@' + port + '@' + str(NS) + '@' + str(MF) + '@' + data[start:end]
        # MESSAGE = bytes(msg, 'utf-8')

        print('HERE', msg)
        cmsg = msg.split('\r\n\r\n')
        print(cmsg[0])
        checksum = checksum1(cmsg[0])
        newmsg = msg + '@' + str(checksum)
        MESSAGE = bytes(newmsg, 'utf-8')

        print('message with checksum :', MESSAGE)
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
            try:
                data, addr = sock.recvfrom(1024)
            except socket.timeout:
                print('timeout')

            NR = int(data)
            print('ack : ', NR, NS)
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

        UDP_PORT = 5007
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.bind((UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(1024)
        newdata = str(data)
        newdata = newdata.split('\'')
        newdata2 = newdata[1].split('@')
        checks = checksum1(newdata2[0])
        print('received data:', data)
        sock.close()
        break

else:
    type = 'CNAME'
    target = 'www.soft98.ir'
    TCP_IP = bytes(IP, 'utf-8')
    TCP_PORT = 5012
    BUFFER_SIZE = 1024
    MESSAGE = bytes(type + '@' + target + '@', 'utf-8')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    s.close()
    print('received data:', data)