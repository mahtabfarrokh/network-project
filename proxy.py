import socket
import time
import dns.resolver
import requests


class Proxy :

    def __init__(self):

        #monireIP = '192.168.1.33'
        #mahtabIP = '192.168.1.55'
        self.IP = ''
        self.UDP_IP = ''
        self.UDP_PORT = 0
        self.TCP_PORT = 80
        self.TCP_IP = ''
        self.realdata = ''
        # self.realdata1 = ''
        self.cacheSaveMsg = ''
        self.NR = 1
        #turn = 0
        self.index = 0
        self.dnsindex = 0
        self.httpCache = []
        self.DNSCache = []
        self.inCache = 0
        self.inDNSCache = 0
        self.udp_to_tcp = False
        self.tcp_to_udp = False
        self.file = open("index2.txt", "w")


    def checksum(self, message):
        c = 0
        # print(message)
        print("staaaaaaaart")
        for x in message:
            if not (x == '\\' or x == '\\n' or x == '\n' or x == 'n' or x == '\''
                    or x == '\\t' or x == '\t' or x == 't'):
                # print(x + " - ", end='', flush=True)
                c = c + ord(x)
                self.file.write(x)
                # c = c + x
        csum = bin(c)
        csum = csum.split('b')
        return csum[1]



    def response_to_client(self,data):

        print("------------------>>>>>>>")
        # print(data)
        udp_port = 5017

        # newdata = str(data)
        # newdata = newdata.split('\'')
        # splitedData = newdata[1].split(' ')
        # response_type = splitedData[1]

        response_type = data.status_code
        # print('here',response_type)
        NS = 0
        MF = 0  # More fragment
        data = data.text
        iteration = 2
        if int(response_type) == 200:

            print('ok ^^ , code = 200 !')
            # sock.sendto(data, (UDP_IP, udp_port))
            # print("received data:", data)
            # sock.close()

            segment_size = 5000
            # print("leeeeeeeeeeeeen:")
            # print(len(data))
            print('len : ', len(data))

            if len(data) > segment_size:

                iteration = int(len(data) / segment_size) + 2
                print('number of iteration : ', iteration)
                MF = 1
                print("fragment happened")
            else:
                    MF = 0

            data = str(data)[:-1]
            # file.write(data)
            data = data.replace('\'', '\\\'')
            for i in range(1, iteration):
                print("iteration : ", i)
                if i == iteration - 1:
                    MF = 0
                start = (i - 1) * segment_size
                end = i * segment_size
                if end > len(data):
                    end = len(data)

                msg = str(NS) + '!@#$%^&*()_+' + str(MF) + '!@#$%^&*()_+' + data[start:end]
                msg = msg.replace('\\n', '\n')
                msg = msg.replace('\\r', '\r')
                msg = msg.replace('\\\\', '\\')
                csum = self.checksum(msg)
                msg = msg.replace('\\n', '\n')
                msg = msg.replace('\\r', '\r')
                msg = msg.replace('\\\\', '\\')

                newmsg = msg + '!@#$%^&*()_+' + str(csum) + '\r\n\r\n'
                MESSAGE = bytes(newmsg, 'utf-8')

                sock = socket.socket(socket.AF_INET,  # Internet
                                     socket.SOCK_DGRAM)  # UDP
                # print('sent message :' ,MESSAGE)
                sock.sendto(MESSAGE, (self.UDP_IP, udp_port))
                sock.close()
                counter = 0
                while True:
                    print('man injam!!')
                    counter += 1
                    # print("counter :", counter)
                    UDP_PORT = 5018
                    sock = socket.socket(socket.AF_INET,  # Internet
                                         socket.SOCK_DGRAM)  # UDP
                    print(self.UDP_IP)
                    sock.bind((self.UDP_IP, UDP_PORT))
                    sock.settimeout(1)
                    try:
                        data2, addr = sock.recvfrom(10000)
                        NR = str(data2)[2]
                        print('ack : ', NR, NS)
                        sock.close()
                        print(int(NR) , int(not bool(NS)) )
                        if int(NR) == int(not bool(NS)):
                            NS = int(NR)
                            print("ssssaaaallllaaaavvvvaaaaatttt")
                            break
                        print("received data:", NR)

                    except socket.timeout:

                        print('timeout')
                        print('retransmit: ')
                        # break
                        UDP_PORT = 5018
                        sock = socket.socket(socket.AF_INET,  # Internet
                                             socket.SOCK_DGRAM)  # UDP
                        sock.sendto(MESSAGE, (self.UDP_IP, UDP_PORT))
                        sock.close()
            self.file.close()
        elif int(response_type) == 4040:
            print('error not found , code = 404 !')
            sock = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP
            sock.sendto(bytes('error not found !', 'utf_8'), (self.UDP_IP, udp_port))
            sock.close()

        elif int(response_type) == 400:
            print('bad req , code = 400 !')
            sock = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP
            sock.sendto(bytes('bad request !', 'utf_8'), (self.UDP_IP, udp_port))
            sock.close()

        elif int(response_type) == 301 or int(response_type) == 302:
            print('moved and redirect  , code = 301 or 302 !')
            # for i in splitedData:
            #     if 'Location:' in i:
            #         # print(splitedData[splitedData.index(i) + 1])
            #         new_location = splitedData[splitedData.index(i) + 1]
            #         new_location = new_location.split('//')
            #         new_location = new_location[1].split('\\')
            #         new_ip = new_location[0]

            BUFFER_SIZE = 10000
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # print((bytes(new_ip, 'utf-8')))
            # print(TCP_PORT)
            # s.connect((bytes(new_ip, 'utf-8'), self.TCP_PORT))
            s.send(bytes(self.realdata, 'utf-8'))
            data = s.recv(BUFFER_SIZE)
            s.close()

            self.response_to_client(data)

    def get_input(self):

        command = input('enter command : \n')
        command = "proxy -s tcp:192.168.1.33:5016 -d udp"
        # command = "proxy -s udp:192.168.1.33:5016 -d tcp"
        command = command.split(' ')

        if len(command) == 5:
            command2 = command[2].split(':')
            if command[0] == 'proxy' and command[1] == '-s' :
                if command2[0] == 'udp' and command[4] == 'tcp' :
                    self.udp_to_tcp = True
                elif command2[0] == 'tcp' and command[4] == 'udp' :
                    self.tcp_to_udp = True
                else :
                    print('wrong command')
                    return False

                self.UDP_IP =bytes (command2[1], 'utf-8')
                self.IP = bytes(command2[1], 'utf-8')
                self.UDP_PORT = int(command2[2])

            else :
                print('wrong command')
                return False
        return True

    def send_and_recieve_req(self):


        while True:

            correct_command = self.get_input()

            if self.udp_to_tcp and correct_command :

                while True:

                    print(' waiting for client request (http mode)... ')
                    #UDP_PORT = 5016
                    BUFFER_SIZE = 10000
                    sock = socket.socket(socket.AF_INET,  # Internet
                                         socket.SOCK_DGRAM)  # UDP
                    sock.bind((self.UDP_IP, self.UDP_PORT))
                    data, addr = sock.recvfrom(10000)  # buffer size is 10000 bytes
                    print('first data :', data)
                    sock.close()

                    if data:

                        data = str(data).split("!@#$%^&*()_+")
                        # TCP_IP = bytes(data[0][2:], 'utf-8')
                        TCP_IP = data[0][2:]
                        TCP_PORT = int(data[1])
                        NS = int(data[2])
                        MF = int(data[3])
                        MESSAGE = data[0][2:] + '!@#$%^&*()_+' + data[1] + '!@#$%^&*()_+' + data[2] + '!@#$%^&*()_+' + data[3] + '!@#$%^&*()_+' + data[4][:-8]
                        # cmsg = realdata1.split('\\')
                        # print(cmsg)
                        # cacheSaveMsg = realdata1.split('\\')[0]

                        print("received message:", MESSAGE)
                        print("tcpIP: ", TCP_IP)
                        print("tcpPORT", TCP_PORT)
                        print("N Next ", self.NR)
                        print(MESSAGE)
                        print('checksum', data[5][:-1], self.checksum(MESSAGE))
                        if NS == int(not bool(self.NR)) and (self.checksum(MESSAGE) == data[5][:-1]):
                            realdata1= ''
                            #print("heeeeeeeeeeeeereeeeeeeeeeeeee")
                            self.realdata = self.realdata + str(data[4][:-8])
                            realdata1 = realdata1 + str(data[0][2:]) + '!@#$%^&*()_+' + str(data[1]) + '!@#$%^&*()_+' + str(data[2]) + '!@#$%^&*()_+' + str(
                                data[3]) + '!@#$%^&*()_+' + str(data[4])

                            self.cacheSaveMsg = realdata1.split('\\')[0]

                            UDP_PORT = 5018

                            ack = bytes(str(self.NR), 'utf-8')
                            print("NR:", ack, self.NR, NS)

                            sock = socket.socket(socket.AF_INET,  # Internet
                                                 socket.SOCK_DGRAM)  # UDP

                            sock.sendto(ack, (self.UDP_IP, UDP_PORT))
                            sock.close()
                            self.NR = NS

                        if MF == 0:
                            break

                # realdata += '\r\n\r\n'
                # print("real data : ", realdata)


                for i in self.httpCache:
                    if self.cacheSaveMsg in i:
                        print('here  i use cache  :D', self.httpCache)
                        self.response_to_client(i[1])
                        self.inCache = 1


                if self.inCache == 0:  # if not in cache

                    print('it is not in cache  :( ', self.httpCache)
                    #----------------------------------------------------------------- socket
                    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # print(TCP_IP)
                    # s.connect((TCP_IP, TCP_PORT))
                    #
                    # # we just send " get request " :)
                    # s.send(bytes('GET / HTTP/1.0\r\n\r\n', 'utf-8'))
                    #
                    # data = s.recv(BUFFER_SIZE)
                    # s.close()

                    #------------------------------------------------------------------ requests
                    print(TCP_IP)
                    TCP_IP = 'http://' + TCP_IP
                    r = requests.get(TCP_IP)
                    print(r.text)


                    # save data in cache
                    if len(self.httpCache) < 10:
                        self.httpCache.append([self.cacheSaveMsg, data])
                    elif len(self.httpCache) == 10:
                        del self.httpCache[self.index]
                        self.httpCache.insert(self.index, [self.cacheSaveMsg, data])
                        self.index = self.index + 1
                        if self.index == 10:
                            self.index = 0

                    # print('index',index)
                    # print('new cache',httpCache)

                    self.response_to_client(r)
                    # self.response_to_client(data)

                inCache = 0


            elif self.tcp_to_udp and correct_command :

                print(' waiting for client request (DNS mode) ... ')

                # print(self.IP)
                TCP_IP = self.IP
                TCP_PORT = 5013
                BUFFER_SIZE = 10000  # Normally 10000, but we want fast response

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
                        data1 = str(data).split('!@#$%^&*()_+')
                        dns_type = str(data1[0][2:])
                        target = str(data1[1])
                        print('type: ', dns_type)
                        target = target.split('\\')[0]
                        print('target: ', target)
                        myResolver = dns.resolver.Resolver()  # create a new instance named 'myResolver'
                        myResolver.timeout = 0.01

                        for i in self.DNSCache:
                            if data in i:
                                print('here', self.DNSCache)
                                conn.send(bytes(i[1], 'utf-8'))
                                inDNSCache = 1

                        if self.inDNSCache == 0:   #if not in cache
                            while True:
                                try:
                                    myAnswers = myResolver.query(target, dns_type)  # Lookup the 'A' record(s) for google.com
                                    # print(myAnswers.flags , dns.flags.AA )
                                    break
                                except dns.exception.Timeout:
                                    print('time out')
                            result = ''
                            for rdata in myAnswers:  # for each response
                                result += str(rdata) + ' '
                                print(rdata)  # print the data

                            # save data in cache
                            if len(self.DNSCache) < 10:
                                self.DNSCache.append([data, result])
                            elif len(self.httpCache) == 10:
                                del self.httpCache[self.dnsindex]
                                self.DNSCache.insert(self.dnsindex, [data, result])
                                self.dnsindex = self.dnsindex + 1
                                if self.dnsindex == 10:
                                    self.dnsindex = 0

                            conn.send(bytes(result, 'utf-8'))  # echo
                            self.inDNSCache = 0
                conn.close()

if __name__ == "__main__":

    proxy = Proxy()
proxy.send_and_recieve_req()