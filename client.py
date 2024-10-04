
# Python program to implement client side of chat room.
import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 2:
    print("Correct usage: script, IP address")
    exit()

IP_address = str(sys.argv[1])
server.connect((IP_address, 8181))

while True:

    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server]

    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048).decode()
            if not message:
                print("Disconnected from server.")
                server.close()
                sys.exit(0)
            print(message)
        else:
            message = sys.stdin.readline()
            server.send(message.encode())
            sys.stdout.flush()
