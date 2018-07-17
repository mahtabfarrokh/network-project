import socket
import time
import requests


# monireIP = '192.168.1.33'
# mahtabIP = '192.168.1.55'

class Client:

    def __init__(self):

        self.get_request = False
        self.DNS_request = False
        self.address = ''
        self.message = ''
        self.dns_type = ''
        self.dns_server = ''
        self.dns_target = ''
        self.IP = '127.0.0.1'
        self.turn = 0
        self.ignoreList = ['\\', '\\n', '\n', 'n', '\'', '\\t', '\t', 't', 'xa0', 'xc2']

        # IP = '192.168.1.55'
        # proxy -s udp:172.23.157.80:5016 -d tcp
        # GET / HTTP/1.1
        # www.google.com

        # 127.215.155.155
    def get_input(self):
        # self.turn += 1
        request = input('enter request : \n')
        host = input()
        # request = "type=CNAME server=8.8.4.4 target=aut.ac.ir"
        request = "GET / HTTP/1.1"
        host = "translate.google.com"
        get_req = request.split('/')
        dns_req = request.split(' ')
        if get_req[0] == 'GET ' and get_req[1] == ' HTTP' and (get_req[2] == '1.1' or get_req[2] == '1.0'):
            self.get_request = True
            self.address = host
            self.message = request
            return True
        # print(dns_req[0].split('=')[0], len(dns_req))
        if len(dns_req) == 3 and dns_req[0].split('=')[0] == 'type':
            self.DNS_request = True
            print(dns_req[0].split('=')[1])
            self.dns_type = dns_req[0].split('=')[1]
            print(dns_req[1].split('=')[1])
            self.dns_server = dns_req[1].split('=')[1]
            print(dns_req[2].split('=')[1])
            self.dns_target = dns_req[2].split('=')[1]
            return True
        return False

    def checksum1(self, message):
        c = 0
        print("staaaaaaaart")
        self.file.write('new\n')
        for x in message:
            if x not in self.ignoreList:
                # print(x + " - ", end='', flush=True)
                c = c + ord(x)
                self.file.write(x)
                # c = c + x
        csum = bin(c)
        csum = csum.split('b')

        return csum[1]


    def send_and_recieve_req(self):

        while True:
            correct_request = self.get_input()
            self.file = open("index.txt", "w")
            self.file2 = open("index.html", "w")
            if self.get_request and correct_request:

                UDP_IP = bytes(self.IP, 'utf-8')
                port = str(80)
                NS = 0
                MF = 0  # More fragment
                iteration = 2
                data = self.message
                realdata = ''

                segment_size = 5000

                if len(data) > segment_size:
                    iteration = int(len(data) / segment_size) + 2
                    MF = 1
                    print("fragment happened")
                else:
                    MF = 0
                for i in range(1, iteration):
                    UDP_PORT = 5016
                    UDP_PORT = 5001 + self.turn
                    if i == iteration - 1:
                        MF = 0
                    start = (i - 1) * segment_size
                    end = i * segment_size
                    if end > len(data):
                        end = len(data)
                    msg = self.address + '!@#$%^&*()_+' + port + '!@#$%^&*()_+' + str(NS) + '!@#$%^&*()_+' + str(MF) + '!@#$%^&*()_+' + data[start:end]
                    cmsg = msg.split('\\')
                    checksum = self.checksum1(msg)
                    msg = msg + '\r\n\r\n'
                    newmsg = msg + '!@#$%^&*()_+' + str(checksum)
                    MESSAGE = bytes(newmsg, 'utf-8')

                    sock = socket.socket(socket.AF_INET,  # Internet
                                         socket.SOCK_DGRAM)  # UDP
                    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                    sock.close()
                    counter = 0
                    while True:
                        counter += 1
                        print("counter :", counter)
                        UDP_PORT = 5018
                        UDP_PORT = 5010 + self.turn
                        print("port : ", UDP_PORT)
                        sock = socket.socket(socket.AF_INET,  # Internet
                                             socket.SOCK_DGRAM)  # UDP

                        sock.bind((UDP_IP, UDP_PORT))
                        sock.settimeout(1)
                        try:
                            data2, addr = sock.recvfrom(10000)
                            NR = str(data2)[2]
                            print('ack : ', NR, NS)
                            sock.close()
                            if int(NR) == int(not bool(NS)):
                                NS = int(NR)
                                print("aaaaaalaaaaaaaah ooo akkkbaaaarrrrrr")
                                break

                            print("received data:", NR)
                        except socket.timeout:
                            print('timeout')
                            print('retransmit: ', MESSAGE)
                            sock.close()
                            UDP_PORT = 5016
                            UDP_PORT = 5001 + self.turn
                            sock = socket.socket(socket.AF_INET,  # Internet
                                                 socket.SOCK_DGRAM)  # UDP
                            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                            sock.close()

                while True :
                    UDP_PORT = 5017
                    UDP_PORT = 5020 + self.turn
                    sock = socket.socket(socket.AF_INET,  # Internet
                                         socket.SOCK_DGRAM)  # UDP
                    sock.bind((UDP_IP, UDP_PORT))
                    data, addr = sock.recvfrom(10000)
                    sock.close()

                    if data:

                        data = str(data).split("!@#$%^&*()_+")
                        NS = int(data[0][2:])
                        MF = int(data[1])
                        MESSAGE = data[0][2:] + '!@#$%^&*()_+' + data[1] + '!@#$%^&*()_+' + data[2]
                        # MESSAGE = MESSAGE.replace('\\\\', '\\')

                        MESSAGE2 = MESSAGE.split('\\\\')
                        MESSAGE = ''
                        c = 0
                        for i in MESSAGE2:
                            if not c:
                                MESSAGE = i
                                c = 1
                            else:
                                MESSAGE += '\\' + i

                        MESSAGE = MESSAGE.replace('\\xa0', ' ')
                        MESSAGE = MESSAGE.replace('\\xc2', '')
                        MESSAGE = ''.join([i if ord(i) < 128 else ' ' for i in MESSAGE])
                        if NS == int(not bool(NR)) and (self.checksum1(MESSAGE) == data[3][:-9]):
                            print('wtffffffffff')
                            if MF == 1:
                                realdata = realdata + str(data[2][:-8])
                                self.file2.write(str(data[2][:-8]))
                            else:
                                realdata = realdata + str(data[2])
                                self.file2.write(str(data[2]))
                                self.file2.write('\r\n\r\n')

                            UDP_PORT = 5018
                            UDP_PORT = 5030 + self.turn
                            ack = bytes(str(NR), 'utf-8')
                            sock = socket.socket(socket.AF_INET,  # Internet
                                                 socket.SOCK_DGRAM)  # UDP

                            sock.sendto(ack, (UDP_IP, UDP_PORT))
                            sock.close()
                            NR = NS
                            if MF == 0:
                                break
                realdata += '\r\n\r\n'
                print("real data : ", realdata)



            elif self.DNS_request and correct_request:

                dnstype = self.dns_type
                target = self.dns_target
                server = self.dns_server
                print("hre : " + server)
                TCP_IP = bytes(self.IP, 'utf-8')
                TCP_PORT = 5016
                BUFFER_SIZE = 10000
                MESSAGE = bytes(dnstype + '!@#$%^&*()_+' + target + '!@#$%^&*()_+' + server + '!@#$%^&*()_+', 'utf-8')

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((TCP_IP, TCP_PORT))
                s.send(MESSAGE)
                data = s.recv(BUFFER_SIZE)
                s.close()
                data = str(data).split('@')
                print('received data: ', data[0])
                if len(data)==2:
                    print('authoritative flag : ', data[1])

            self.file.close()
            self.file2.close()


if __name__ == "__main__":

    client = Client()
    client.send_and_recieve_req()