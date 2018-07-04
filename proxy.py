import socket
import time
import dns.resolver

UDP_IP = bytes("172.23.157.80", 'utf-8')
UDP_PORT = 5016
TCP_PORT = 80
TCP_IP = ''
realdata = ''
realdata1 = ''
NR = 1
turn = 0

def checksum(MESSAGE) :
    c = 0

    for x in MESSAGE:
        c = c + ord(x)
    checksum = bin(c)
    checksum = checksum.split('b')

    return checksum[1]
if turn:

    while True:
        UDP_PORT = 5016
        BUFFER_SIZE = 1024
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.bind((UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print('first data :', data)
        sock.close()

        if data:
            data = str(data).split("@")
            TCP_IP = bytes(data[0][2:], 'utf-8')
            TCP_PORT = int(data[1])
            NS = int(data[2])
            MF = int(data[3])
            MESSAGE = bytes(data[4], 'utf-8')
            realdata = realdata + str(data[4][:-1])
            realdata1 = realdata1 + str(data[0][2:]) + '@' + str(data[1]) + '@' + str(data[2]) + '@' + str(
                data[3]) + '@' + str(data[4])

            cmsg = realdata1.split('\\')

            print(realdata1)
            print("received message:", MESSAGE)
            print("tcpIP: ", TCP_IP)
            print("tcpPORT", TCP_PORT)
            print("N Next ", NR)
            print('checksum', data[5][:-1], checksum(cmsg[0]))
            if NS == int(not bool(NR) and int(checksum(cmsg[0])) == int(data[5][-1])):
                UDP_PORT = 5008
                ack = bytes(str(NR), 'utf-8')
                sock = socket.socket(socket.AF_INET,  # Internet
                                     socket.SOCK_DGRAM)  # UDP
                sock.sendto(ack, (UDP_IP, UDP_PORT))
                sock.close()
                NR = NS

            if MF == 0:
                break

    print("real data : ", realdata)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(bytes(realdata, 'utf-8'))
    data = s.recv(BUFFER_SIZE)
    s.close()

    UDP_PORT = 5007
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP

    newdata = str(data)
    newdata = newdata.split('\'')
    checksum = checksum(newdata[1])
    newdata2 = bytes(newdata[1] + '@' + str(checksum), 'utf_8')
    sock.sendto(newdata2, (UDP_IP, UDP_PORT))
    print("received data:", data)
    sock.close()
else:
    TCP_IP = bytes("172.23.157.80", 'utf-8')
    TCP_PORT = 5010
    BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(2)

    conn, addr = s.accept()
    print('Connection address:', addr)
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        else:
            print("received data:", data)
            data1 = str(data).split('@')
            type = str(data1[0][2:])
            target = str(data1[1])
            print("type: ", type)
            print("target: ", target)
            myResolver = dns.resolver.Resolver()  # create a new instance named 'myResolver'
            myAnswers = myResolver.query(target, type)  # Lookup the 'A' record(s) for google.com
            result = ''
            for rdata in myAnswers:  # for each response
                result += str(rdata) + ' '
                print(rdata)  # print the data
            conn.send(bytes(result, 'utf-8'))# echo
    conn.close()