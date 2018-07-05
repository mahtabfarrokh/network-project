import socket
import time
# import dns.resolver
import requests

# IP = '192.168.1.55'
# IP = "192.168.80.1"
IP = '192.168.1.33'
UDP_IP = bytes(IP, 'utf-8')
UDP_PORT = 5017
TCP_PORT = 80
TCP_IP = ''
realdata = ''
realdata1 = ''
NR = 1
turn = 0
index = 0
dnsindex = 0
httpCache = []
DNSCache = []
inCache = 0
inDNSCache = 0

def checksum(MESSAGE):
    c = 0

    for x in MESSAGE:
        c = c + ord(x)
    csum = bin(c)
    csum = csum.split('b')
    return csum[1]



def responseToClient(data) :

    UDP_PORT = 5007
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP

    newdata = str(data)
    newdata = newdata.split('\'')
    splitedData = newdata[1].split(' ')
    responseType = splitedData[1]
    # print('here',responseType)

    if int(responseType) == 200:
        # checksum = checksum(newdata[1])
        # newdata2 = bytes(newdata[1] + '@' + str(checksum), 'utf_8')
        print('ok ^^ , code = 200 !')
        sock.sendto(data, (UDP_IP, UDP_PORT))
        print("received data:", data)
        sock.close()

    elif int(responseType) == 404:
        print('error not found , code = 404 !')
        sock.sendto(bytes('error not found !','utf_8'), (UDP_IP, UDP_PORT))
        sock.close()

    elif int(responseType) == 400:
        print('bad req , code = 400 !')
        sock.sendto(bytes('bad request !','utf_8'), (UDP_IP, UDP_PORT))
        sock.close()

    elif int(responseType) == 301 or int(responseType) == 302:
        print('moved and redirect  , code = 301 or 302 !')
        for i in splitedData:
            if 'Location:' in i:
                # print(splitedData[splitedData.index(i) + 1])
                newLocation = splitedData[splitedData.index(i) + 1]
                newLocation = newLocation.split('//')
                newLocation = newLocation[1].split('\\')
                new_IP = newLocation[0]

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print((bytes(new_IP, 'utf-8')))
        # print(TCP_PORT)
        s.connect((bytes(new_IP, 'utf-8'), TCP_PORT))
        s.send(bytes(realdata, 'utf-8'))
        data = s.recv(BUFFER_SIZE)
        s.close()

        responseToClient(data)


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
            realdata = realdata + str(data[4][:])
            realdata1 = realdata1 + str(data[0][2:]) + '@' + str(data[1]) + '@' + str(data[2]) + '@' + str(
                data[3]) + '@' + str(data[4])

            cmsg = realdata1.split('\\')
            cacheSaveMsg = realdata1.split('\\')[0]

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

    print("real data : ", realdata[0:])


    for i in httpCache:
        if cacheSaveMsg in i:
            print('here', httpCache)
            responseToClient(i[1])
            inCache = 1


    if inCache == 0  : # if not in cache

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(TCP_IP)
        s.connect((TCP_IP, TCP_PORT))

        # we just send get request :)
        s.send(bytes('GET / HTTP/1.0\r\n\r\n', 'utf-8'))

        data = s.recv(BUFFER_SIZE)
        s.close()
        # print('old cache',httpCache)

        # save data in cache
        if len(httpCache) < 10 :
            httpCache.append([cacheSaveMsg,data])
        elif len(httpCache) == 10 :
            del httpCache[index]
            httpCache.insert(index,[cacheSaveMsg,data])
            index = index + 1
            if index == 10 :
                index = 0
        # print('index',index)
        # print('new cache',httpCache)

        responseToClient(data)

    inCache = 0

else:

    TCP_IP = bytes(IP, 'utf-8')
    TCP_PORT = 5012
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
            print('type: ', type)
            print('target: ', target)
            myResolver = dns.resolver.Resolver()  # create a new instance named 'myResolver'
            myResolver.timeout = 0.01

            for i in DNSCache:
                if data in i:
                    print('here', DNSCache)
                    conn.send(bytes(i[1], 'utf-8'))
                    inDNSCache = 1

            if (inDNSCache == 0) :   #if not in cache
                while True:
                    try:
                        myAnswers = myResolver.query(target, type)  # Lookup the 'A' record(s) for google.com
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