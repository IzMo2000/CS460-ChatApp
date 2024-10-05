import socket
import select
import sys
from _thread import *

class ChatRoom:
    next_room_num = 0
    def __init__(self, conn):
        self.room_num = ChatRoom.next_room_num
        ChatRoom.next_room_num += 1
        self.messages = []
        self.clients = [conn]

    def add_client(self, conn):
        self.clients.append(conn)

    def remove_client(self, conn):
        self.clients.remove(conn)
    
    def add_message(self, message):
        self.messages.append(message)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP_address = str(sys.argv[1])
server.bind((IP_address, 8181))

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
    action = prompt_actions(conn)
    if action == '1':
        selected_room = ChatRoom(conn)
        chatrooms.append(selected_room)
    elif action == '2':
        selected_room_num = select_chat_room(conn)
        if selected_room_num is None:
            selected_room = ChatRoom(conn)
            chatrooms.append(selected_room)
        chatrooms[selected_room_num].add_client(conn)
        selected_room = chatrooms[selected_room_num]
    else:
        close_connection(conn, addr)
        return

    selected_room.add_message(f"{username} has joined.\n")
    await_messages(selected_room, username, conn)
    print(f"{username} left chat room {selected_room.room_num}")
    close_connection(conn, addr)

def close_connection(conn, addr):
    print(f"Client at {addr[0]} closed connection")
    conn.close()

def await_messages(room, username, conn):
    conn.send("Input will now be sent to chatoom. To see chat room messages, type '/read'. To leave, type '/exit'\n".encode())
    while True:
        try:
            message = conn.recv(2048).decode().strip()
            if message == "/exit":
                chatrooms[room.room_num].remove_client(conn)
                room.add_message(f"{username} has left the chat.\n")
                break
            if message == "/read":
                print(room.messages)
                for message in room.messages:
                    try:
                        conn.send(message.encode())
                    except:
                        room.remove_client(conn)
            else:
                room.add_message(f"{username}: {message}\n")
                conn.send("Message sent.".encode())
        except:
            break

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
        conn.send("No chat rooms available! Creating room...\n".encode())
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
            conn.send("ERROR: Non integer response detected.\n".encode())
            room_selection = -1
        if room_selection < 0 or room_selection > len(chatrooms) - 1:
            conn.send("Try Again, please enter a valid room number\n".encode())
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
