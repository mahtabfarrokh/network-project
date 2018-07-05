import socket
import time
import dns.resolver
import requests

IP = '192.168.1.55'
# IP = "192.168.80.1"
# IP = '192.168.1.33'
UDP_IP = bytes(IP, 'utf-8')
UDP_PORT = 5017
TCP_PORT = 80
TCP_IP = ''
realdata = ''
realdata1 = ''
cacheSaveMsg = ''
NR = 1
turn = 1
index = 0
dnsindex = 0
httpCache = []
DNSCache = []
inCache = 0
inDNSCache = 0


def checksum(message):
    c = 0
    for x in message:
        c = c + ord(x)
    csum = bin(c)
    csum = csum.split('b')
    return csum[1]



def response_to_client(data):
    print("------------------>>>>>>>")
    print(data)
    udp_port = 5017
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP

    newdata = str(data)
    newdata = newdata.split('\'')
    splitedData = newdata[1].split(' ')
    response_type = splitedData[1]
    # print('here',response_type)
    NS = 0
    MF = 0  # More fragment
    iteration = 2
    if int(response_type) == 200:
        print('ok ^^ , code = 200 !')
        # sock.sendto(data, (UDP_IP, udp_port))
        # print("received data:", data)
        # sock.close()

        segment_size = 15
        print("leeeeeeeeeeeeen:")
        print(len(data))
        if len(data) > segment_size:
            iteration = int(len(data) / segment_size) + 2
            MF = 1
            print("fragment happened")
        else:
                MF = 0

        data = str(data)[2:-1]
        print("====================")
        print(data)
        print("====================")
        for i in range(1, iteration):
            if i == iteration - 1:
                MF = 0
            start = (i - 1) * segment_size
            end = i * segment_size
            if end > len(data):
                end = len(data)
            print("====================")
            print(data[start:end])
            print("====================")
            msg = str(NS) + '@' + str(MF) + '@' + data[start:end]
            print('HERE', msg)
            print('check', msg)
            msg = msg.replace('\\n', '\n')
            msg = msg.replace('\\r', '\r')
            csum = checksum(msg)
            # msg = msg + '\r\n\r\n'
            newmsg = msg + '@' + str(csum) + '\r\n\r\n'
            MESSAGE = bytes(newmsg, 'utf-8')

            print('message with checksum :', MESSAGE)

            sock.sendto(MESSAGE, (UDP_IP, udp_port))
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
                        print("ssssaaaallllaaaavvvvaaaaatttt")
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

    elif int(response_type) == 404:
        print('error not found , code = 404 !')
        sock.sendto(bytes('error not found !', 'utf_8'), (UDP_IP, udp_port))
        sock.close()

    elif int(response_type) == 400:
        print('bad req , code = 400 !')
        sock.sendto(bytes('bad request !', 'utf_8'), (UDP_IP, udp_port))
        sock.close()

    elif int(response_type) == 301 or int(response_type) == 302:
        print('moved and redirect  , code = 301 or 302 !')
        for i in splitedData:
            if 'Location:' in i:
                # print(splitedData[splitedData.index(i) + 1])
                new_location = splitedData[splitedData.index(i) + 1]
                new_location = new_location.split('//')
                new_location = new_location[1].split('\\')
                new_ip = new_location[0]

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print((bytes(new_ip, 'utf-8')))
        # print(TCP_PORT)
        s.connect((bytes(new_ip, 'utf-8'), TCP_PORT))
        s.send(bytes(realdata, 'utf-8'))
        data = s.recv(BUFFER_SIZE)
        s.close()

        response_to_client(data)


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
            MESSAGE = data[0][2:] + '@' + data[1] + '@' + data[2] + '@' + data[3] + '@' + data[4][:-8]
            # cmsg = realdata1.split('\\')
            # print(cmsg)
            # cacheSaveMsg = realdata1.split('\\')[0]

            print("received message:", MESSAGE)
            print("tcpIP: ", TCP_IP)
            print("tcpPORT", TCP_PORT)
            print("N Next ", NR)
            print(MESSAGE)
            print('checksum', data[5][:-1], checksum(MESSAGE))
            if NS == int(not bool(NR)) and (checksum(MESSAGE) == data[5][:-1]):
                print("heeeeeeeeeeeeereeeeeeeeeeeeee")
                realdata = realdata + str(data[4][:-8])
                realdata1 = realdata1 + str(data[0][2:]) + '@' + str(data[1]) + '@' + str(data[2]) + '@' + str(
                    data[3]) + '@' + str(data[4])

                cacheSaveMsg = realdata1.split('\\')[0]

                UDP_PORT = 5008
                ack = bytes(str(NR), 'utf-8')
                print("NR:", ack, NR, NS)
                sock = socket.socket(socket.AF_INET,  # Internet
                                     socket.SOCK_DGRAM)  # UDP
                sock.sendto(ack, (UDP_IP, UDP_PORT))
                sock.close()
                NR = NS

            if MF == 0:
                break
    realdata += '\r\n\r\n'
    print("real data : ", realdata)


    for i in httpCache:
        if cacheSaveMsg in i:
            print('here', httpCache)
            response_to_client(i[1])
            inCache = 1


    if inCache == 0:  # if not in cache

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(TCP_IP)
        s.connect((TCP_IP, TCP_PORT))

        # we just send get request :)
        s.send(bytes('GET / HTTP/1.0\r\n\r\n', 'utf-8'))

        data = s.recv(BUFFER_SIZE)
        s.close()
        # print('old cache',httpCache)

        # save data in cache
        if len(httpCache) < 10:
            httpCache.append([cacheSaveMsg, data])
        elif len(httpCache) == 10:
            del httpCache[index]
            httpCache.insert(index, [cacheSaveMsg, data])
            index = index + 1
            if index == 10:
                index = 0
        # print('index',index)
        # print('new cache',httpCache)

        response_to_client(data)

    inCache = 0

else:

    TCP_IP = bytes(IP, 'utf-8')
    TCP_PORT = 5013
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
            dns_type = str(data1[0][2:])
            target = str(data1[1])
            print('type: ', dns_type)
            print('target: ', target)
            myResolver = dns.resolver.Resolver()  # create a new instance named 'myResolver'
            myResolver.timeout = 0.01

            for i in DNSCache:
                if data in i:
                    print('here', DNSCache)
                    conn.send(bytes(i[1], 'utf-8'))
                    inDNSCache = 1

            if inDNSCache == 0:   #if not in cache
                while True:
                    try:
                        myAnswers = myResolver.query(target, dns_type)  # Lookup the 'A' record(s) for google.com
                        break
                    except dns.exception.Timeout:
                        print('time out')
                result = ''
                for rdata in myAnswers:  # for each response
                    result += str(rdata) + ' '
                    print(rdata)  # print the data

                # save data in cache
                if len(DNSCache) < 10:
                    DNSCache.append([data, result])
                elif len(httpCache) == 10:
                    del httpCache[dnsindex]
                    DNSCache.insert(dnsindex, [data, result])
                    dnsindex = dnsindex + 1
                    if dnsindex == 10:
                        dnsindex = 0

                conn.send(bytes(result, 'utf-8'))  # echo
            inDNSCache = 0
    conn.close()