# -*- coding: utf-8 -*-


#   2019/1/9 0009 上午 10:07     
#   BY:RollingBear

import argparse
import random
import socket
import Server_Basic_Package_Def1


def client(address, cause_error=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)

    aphorisms = list(Server_Basic_Package_Def1.aphorisms)

    if cause_error:
        sock.sendall(aphorisms[0][:-1])
        return
    for aphorism in random.sample(aphorisms, 3):
        sock.sendall(aphorism)
        print(aphorism, Server_Basic_Package_Def1.recv_until(sock, b'.'))

    sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example client')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-e', action='store_true', help='cause an error')
    parser.add_argument('-p', metavar='port', type=int, default=1060, help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    client(address, args.e)