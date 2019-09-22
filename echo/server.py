import socket
import random
import struct

sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '127.0.0.1'
port_recv = 5500
port_send = 5550
server = (server_address, port_recv)
sock_recv.bind(server)



print("Listening on " )


def get_pseudo_packet():
    F = random.randint(1,200)
    Pos = 10
    pack = struct.pack(">3c2f",b"H",b"2",b"C",F,Pos)
    return pack

while True:
    payload, client_address = sock_recv.recvfrom(1024)
    #print("Echoing data back to " + str(client_address))
    print(payload)
    data = get_pseudo_packet()
    sent = sock_send.sendto(data, (server_address,port_send))
