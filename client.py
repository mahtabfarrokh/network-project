import socket
import time
import requests


# monireIP = '192.168.1.33'
# mahtabIP = '192.168.1.55'

class Client :

    def __init__(self):

        self.get_request = False
        self.DNS_request = False
        self.address = ''
        self.message = ''
        self.dns_type =''
        self.dns_server = ''
        self.dns_target = ''
        self.IP = '172.23.157.80'
        # IP = '192.168.1.55'
        # proxy -s udp:172.23.157.80:5016 -d tcp
        # GET / HTTP/1.1
        # www.google.com
    def get_input(self) :

        request = input('enter request : \n')
        host = input()
        request = "GET / HTTP/1.1"
        host = "python.org"
        get_req = request.split('/')
        dns_req = request.split(' ')
        if get_req[0] == 'GET ' and get_req[1] == ' HTTP' and (get_req[2] == '1.1' or get_req[2] == '1.0'):
            self.get_request = True
            self.address = host
            self.message = request
            return True
        elif len(dns_req) == 3 and dns_req[0].split('=')[0] == 'type':
            self.DNS_request = True
            self.dns_type = dns_req[0].split('=')[1]
            self.dns_server = dns_req[1].split('=')[1]
            self.dns_target = dns_req[2].split('=')[1]
            return True
        return False

    def checksum1(self,message):
        c = 0
        print("staaaaaaaart")
        for x in message:
            if not (x == '\\' or x == '\\n' or x == '\n' or x == 'n' or x == '\''):
                print(x + " - ", end='', flush=True)
                c = c + ord(x)
        csum = bin(c)
        csum = csum.split('b')

        return csum[1]
#1110110011011011
    def send_and_recieve_req(self):
        while True :

            correct_request = self.get_input()

            if self.get_request and correct_request:

                UDP_IP = bytes(self.IP, 'utf-8')
                timeout = 50
                address = self.address
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
                    if i == iteration - 1:
                        MF = 0
                    start = (i - 1) * segment_size
                    end = i * segment_size
                    if end > len(data):
                        end = len(data)
                    msg = self.address + '!@#$%^&*()_+' + port + '!@#$%^&*()_+' + str(NS) + '!@#$%^&*()_+' + str(MF) + '!@#$%^&*()_+' + data[start:end]
                    cmsg = msg.split('\\')
                    # checksum = checksum1(cmsg[0])
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
                        UDP_PORT = 5008
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
                            UDP_PORT = 5016
                            sock = socket.socket(socket.AF_INET,  # Internet
                                                 socket.SOCK_DGRAM)  # UDP
                            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                            sock.close()

                while True :
                    UDP_PORT = 5017
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
                        MESSAGE = MESSAGE.replace('\\\\', '\\')
                        MESSAGE2 = MESSAGE.split('\\\\')
                        MESSAGE = ''
                        c = 0
                        for i in MESSAGE2:
                            if not c:
                                MESSAGE = i
                                c = 1
                            else:
                                MESSAGE += '\\' + i
                        print('here: ')
                        # print(len(data))
                        # for i in range(0, len(data)):
                        #     print(data[i])
                        #     print("********************")
                        print(data[3][:-9])
                        print(self.checksum1(MESSAGE))

                        if NS == int(not bool(NR)) and (self.checksum1(MESSAGE) == data[3][:-9]):
                            print('wtffffffffff')
                            if MF == 1:
                                realdata = realdata + str(data[2][:-8])
                            else:
                                realdata = realdata + str(data[2])

                            UDP_PORT = 5008
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



            elif self.DNS_request and correct_request :

                dnstype = self.dns_type
                target = self.dns_target

                TCP_IP = bytes(self.IP, 'utf-8')
                TCP_PORT = 5013
                BUFFER_SIZE = 10000
                MESSAGE = bytes(dnstype + '!@#$%^&*()_+' + target + '!@#$%^&*()_+', 'utf-8')

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((TCP_IP, TCP_PORT))
                s.send(MESSAGE)
                data = s.recv(BUFFER_SIZE)
                s.close()
                print('received data:', data)

if __name__ == "__main__":

    client = Client()
    client.send_and_recieve_req()