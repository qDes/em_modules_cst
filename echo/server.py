import socket
import random
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '127.0.0.1'
server_port = 5500

server = (server_address, server_port)
sock.bind(server)
print("Listening on " + server_address + ":" + str(server_port))


def get_pseudo_packet():
    F = random.randint(1,200)
    Pos = 10
    pack = struct.pack(">3c2f",b"H",b"2",b"C",F,Pos)
    return pack

while True:
    payload, client_address = sock.recvfrom(1024)
    print("Echoing data back to " + str(client_address))
    data = get_pseudo_packet()
    sent = sock.sendto(data, client_address)
