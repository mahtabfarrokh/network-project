import socket


UDP_IP = bytes("172.23.157.80", 'utf-8')
UDP_PORT = 5006
BUFFER_SIZE = 1024
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)# buffer size is 1024 bytes
    if data:

        data = str(data).split("@")
        TCP_IP = bytes(data[0][3:], 'utf-8')
        TCP_PORT = int(data[1])
        MESSAGE = bytes(data[2], 'utf-8')
        print("received message:", MESSAGE)
        print(TCP_IP)
        print(TCP_PORT)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        data = s.recv(BUFFER_SIZE)
        s.close()
        print("received data:", data)
