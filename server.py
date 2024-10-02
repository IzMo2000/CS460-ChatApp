import socket
import select
import sys
from _thread import *

class ChatRoom:
    next_room_num = 0
    def __init__(self, conn):
        self.room_num = self.next_room_num
        self.next_room_num += 1
        self.clients = [conn]

    def add_client(self, conn):
        self.clients.append(conn)

    def remove_client(self, conn):
        self.clients.remove(conn)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print("Error: must give script, IP address, port number")
    exit()

IP_address = str(sys.argv[1])

Port = int(sys.argv[2])

server.bind((IP_address, Port))

server.listen(100)

chatrooms = []

def client_thread(conn, addr):
    conn.send("Welcome! If you would like to disconnect, press Enter (no input)\n".encode())
    conn.send("Please enter your username: ".encode())
    username = conn.recv(2048).decode().strip()
    if username == "":
        close_connection(conn, addr)
        return
    else:
        print(f"Client at {addr[0]} has entered as {username}")
    conn.send(f"Welcome to the chat app, {username}!\n".encode())
    while True:
        try:
            action = prompt_actions(conn)
            selected_room = 0
            if action == '1':
                selected_room = ChatRoom(conn)
                chatrooms.append(selected_room)

            elif action == '2':
                selected_room_num = select_chat_room(conn)
                if selected_room_num is None:
                    continue
                chatrooms[selected_room_num].add_client(conn)
                selected_room = chatrooms[selected_room_num]
            else:
                close_connection(conn, addr)
                return

            broadcast_message(selected_room, f"{username} has joined.")
            await_messages(selected_room, username, conn)
            print(f"{username} left chat room {selected_room.room_num}")
        except:
            # close_connection(conn, addr)
            continue

def close_connection(conn, addr):
    print(f"Client at {addr[0]} closed connection")
    conn.close()

def await_messages(room, username, conn):
    conn.send("To leave the chat room, press Enter (no input)\n".encode())

    while True:
       
        try:
            message = conn.recv(2048).decode().strip()
            if message and message != "":
                broadcast_message(room, f"{username}: {message}")
            else:
                chatrooms[room.room_num].remove_client(conn)
                print(chatrooms[room.room_num].__dict__)
                broadcast_message(room, f"{username} has left the chat.")
                break
        except:
            break

def broadcast_message(room, message):
    for conn in room.clients:
        try:
            conn.send(message.encode())
        except:
            room.remove_client(conn)

def prompt_actions(conn):
    user_input = " "
    while user_input not in ('1', '2', '3'):
        conn.send("1. Create and Join a New Server\n".encode())
        conn.send("2. Join an Existing Server\n".encode())
        conn.send("3. Disconnect\n".encode())
        conn.send("Please Choose 1, 2, or 3: ".encode())
        user_input = str(conn.recv(2048).decode().strip())
        if user_input not in ('1', '2', '3'):
            conn.send("ERROR: Input other than '1', '2', or '3' received. Try again:".encode())
    return user_input

def select_chat_room(conn):
    if len(chatrooms) == 0:
        conn.send("No chat rooms available!".encode())
        return None
    room_selection = -1
    while room_selection < 0 or room_selection > len(chatrooms) - 1:
        conn.send("Select a chatroom to join:\n".encode())
        for chatroom in chatrooms:
            conn.send(f"Chatroom {chatroom.room_num}\n".encode())
        conn.send("Join chat room #: ".encode())
        room_selection = conn.recv(2048).decode().strip()
        print(room_selection)
        try:
            room_selection = int(room_selection)
            print(room_selection)
        except ValueError:
            conn.send("ERROR: Non integer response detected.\n")
            room_selection = -1
        if room_selection < 0 or room_selection > len(chatrooms) - 1:
            conn.send("Try Again, please enter a valid room number\n")
    return room_selection

print("Chat app initialized. Listening...")
try:
    while True:
        conn, addr = server.accept()
        print(f"{addr[0]} connected")
        start_new_thread(client_thread, (conn, addr))

except KeyboardInterrupt:
    print("\nServer shutting down...")
    server.close()
    sys.exit(0)