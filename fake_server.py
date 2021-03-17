import socket
import random
import struct
import math

sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '127.0.0.1'
port_recv = 5500
port_send = 5550
server = (server_address, port_recv)
sock_recv.bind(server)

print("Listening on ")

Pos = 0


def get_pseudo_packet(pos, F):
    pos += 1
    pack = struct.pack(">3c2f", b"H", b"2", b"C", F, pos, 0, 0, 0, 0, 0, 0, 0, 0)
    return pack


if __name__ == "__main__":
    while True:
        F = abs(math.sin(math.radians(Pos)) * 200) + random.randint(1, 20)
        Pos += 1
        try:
            payload, client_address = sock_recv.recvfrom(1024)
        except KeyboardInterrupt:
            sock_recv.close()
            print("Stop server")
            break
        # print("Echoing data back to " + str(client_address))
        print(payload)
        data = get_pseudo_packet(Pos, F)
        sent = sock_send.sendto(data, (server_address, port_send))
