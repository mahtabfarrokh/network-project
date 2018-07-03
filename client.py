import socket

UDP_IP = bytes("127.0.0.1", 'utf-8')
UDP_PORT = 5005
MESSAGE = bytes("Hello, World!", 'utf-8')

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

