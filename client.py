import socket
import time
import requests

turn = 1
# IP = '192.168.1.33'
IP = '192.168.1.55'



if turn:
    UDP_IP = bytes(IP, 'utf-8')
    timeout = 50
    address = 'www.google.com'
    port = str(80)
    NS = 0
    MF = 0  # More fragment
    iteration = 2
    data = 'GET / HTTP/1.0'
    newdata = ''
    realdata = ''
    realdata1 = ''

    def checksum1(message):
        c = 0
        for x in message:
            c = c + ord(x)
        csum = bin(c)
        csum = csum.split('b')

        return csum[1]

    segment_size = 5
    print("leeeeeeeeeeeeen:")
    print(len(data))
    if len(data) > segment_size:
        iteration = int(len(data) / segment_size) + 2
        MF = 1
        print("fragment happened")
    else:
        MF = 0
    for i in range(1, iteration):
        UDP_PORT = 5016
        if i == iteration - 1:
            MF = 0
        print('UDP target IP:', UDP_IP)
        print('UDP target port:', UDP_PORT)
        start = (i - 1) * segment_size
        end = i * segment_size
        if end > len(data):
            end = len(data)
        print(address)
        print(port)
        print(NS)
        print(MF)
        print(data)
        msg = address + '@' + port + '@' + str(NS) + '@' + str(MF) + '@' + data[start:end]
        print('HERE', msg)
        cmsg = msg.split('\\')
        print('check', msg)
        # checksum = checksum1(cmsg[0])
        checksum = checksum1(msg)
        msg = msg + '\r\n\r\n'
        newmsg = msg + '@' + str(checksum)
        MESSAGE = bytes(newmsg, 'utf-8')

        print('message with checksum :', MESSAGE)
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        sock.close()
        counter = 0
        while True:
            counter += 1
            print("counter :", counter)
            UDP_PORT = 5008
            sock = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP
            sock.bind((UDP_IP, UDP_PORT))
            sock.settimeout(1)
            try:
                data2, addr = sock.recvfrom(1024)
                NR = str(data2)[2]
                print('ack : ', NR, NS)
                sock.close()
                print("NR & NS :", NR, int(not bool(NS)))
                if int(NR) == int(not bool(NS)):
                    NS = int(NR)
                    print("aaaaaalaaaaaaaah ooo akkkbaaaarrrrrr")
                    break

                print("received data:", NR)
            except socket.timeout:
                print('timeout')
                print('retransmit: ', MESSAGE)
                UDP_PORT = 5016
                sock = socket.socket(socket.AF_INET,  # Internet
                                     socket.SOCK_DGRAM)  # UDP
                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                sock.close()

    while True:
        UDP_PORT = 5017
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.bind((UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(1024)
        sock.close()

        if data:
            data = str(data).split("@")
            print(data)
            NS = int(data[0][2:])
            MF = int(data[1])
            MESSAGE = data[0][2:] + '@' + data[1] + '@' + data[2]
            # cmsg = realdata1.split('\\')
            # print(cmsg)
            # cacheSaveMsg = realdata1.split('\\')[0]

            print("received message:", MESSAGE)
            print("N Next ", NR)
            print(MESSAGE)
            print('checksum', data[3][:-9], checksum1(MESSAGE))
            if NS == int(not bool(NR)) and (checksum1(MESSAGE) == data[3][:-9]):
                print("heeeeeeeeeeeeereeeeeeeeeeeeee")
                realdata = realdata + str(data[2][:-8])
                UDP_PORT = 5008
                ack = bytes(str(NR), 'utf-8')
                print("NR:", ack, NR, NS)
                sock = socket.socket(socket.AF_INET,  # Internet
                                     socket.SOCK_DGRAM)  # UDP
                sock.sendto(ack, (UDP_IP, UDP_PORT))
                sock.close()
                NR = NS
                print("******************************")
            if MF == 0:
                break
    realdata += '\r\n\r\n'
    print("real data : ", realdata)

else:
    dnstype = 'CNAME'
    target = 'www.soft98.ir'
    TCP_IP = bytes(IP, 'utf-8')
    TCP_PORT = 5013
    BUFFER_SIZE = 1024
    MESSAGE = bytes(dnstype + '@' + target + '@', 'utf-8')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    s.close()
    print('received data:', data)