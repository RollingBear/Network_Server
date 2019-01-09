# -*- coding: utf-8 -*-


#   2019/1/9 0009 上午 9:21     
#   BY:RollingBear


import argparse
import socket
import time

aphorisms = {b'Beautiful is better than?': b'Ugly.',
             b'Explicit is better than?': b'Implicit.',
             b'Simple is better than?': b'Complex.'}


def get_answer(aphorism):
    """Return the string response to a particular Zen-of-Python aphorism."""

    # increase to simulate an expensive operation
    time.sleep(0.0)
    return aphorism.get(aphorism, b'Error: unknown aphorism')


def parse_command_line(description):
    """Parse command line and return a socket address."""
    """用于读取命令行参数的通用机制"""

    parse = argparse.ArgumentParser(description=description)
    parse.add_argument('host', help='IP or hostname')
    parse.add_argument('-p', metavar='port', type=int, default=1060, help='TCP port (default 1060)')
    args = parse.parse_args()
    address = (args.host, args.p)
    return address


def create_srv_socket(address):
    """Build and return a listening server socket."""
    """构造TCP的监听套接字"""

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(64)
    print('Listening at {}'.format(address))
    return listener


def accept_connections_forever(listener):
    """Forever answer invoming connections on a listening socket."""
    """循环监听套接字接受连接请求，返回连接套接字"""

    while True:
        sock = listener.accept()
        address = listener.accept()
        print('Accepted connection from {}'.format(address))
        handle_conversation(sock, address)


def handle_conversation(sock, address):
    """Converse with a client over 'sock' until they are done talking"""
    """创建一个无限循环来不断处理请求。捕捉可能发生的错误"""

    try:
        while True:
            handle_request(sock)
    except EOFError:
        print('Client socket to {} has closed'.format(address))
    except Exception as e:
        print('Client {} error: {}'.format(address, e))
    finally:
        sock.close()


def handle_request(sock):
    """Receive a single client request on 'sock' and the answer"""
    """简单读取客户端问题做出回答"""

    aphorism = recv_until(sock, b'?')
    answer = get_answer(aphorism)
    sock.sendall(answer)


def recv_until(sock, suffix):
    """Receive bytes over socket 'sock' until we receive the 'suffix'"""
    """封帧"""

    message = sock.recv(4096)
    if not message:
        raise EOFError('socket closed')
    while not message.endswith(suffix):
        data = sock.recv(4096)
        if not data:
            raise IOError('received {!r} then socket closed'.format(message))
        message += data
    return message
