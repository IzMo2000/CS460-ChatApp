import socket 
import select 
import sys 
from _thread import *


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

if len(sys.argv) != 3: 
    print("Error: must give script, IP address, port number")
    exit()
    
IP_address = str(sys.argv[1])

Port = int(sys.argv[2])

server.bind((IP_address, Port)) 

server.listen(100) 
 
chatrooms = {}
chat_room_num = 1

def client_thread(conn, addr):
    global chat_room_num
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
                selected_room = chat_room_num

                chatrooms[selected_room] = [conn]
                chat_room_num += 1

            elif action == '2':
                selected_room = select_chat_room(conn)
                if selected_room is None:
                    continue
                chatrooms[selected_room].append(conn)
            else:
                close_connection(conn, addr)
                return

            broadcast_message(selected_room, f"{username} has joined.")
            await_messages(selected_room, username, conn)
            print(f"{username} left chat room {selected_room}")
        except:
            continue
            
def close_connection(conn, addr):
    print(f"Client at {addr[0]} closed connection")
    conn.close()

def await_messages(room_num, username, conn):
    conn.send("To leave the chat room, press Enter (no input)\n".encode())
    while True:
        try:
            message = conn.recv(2048).decode().strip()
            if message and message != "":
                broadcast_message(room_num, f"{username}: {message}")
            else:
                chatrooms[room_num].remove(conn)
                broadcast_message(room_num, f"{username} has left the chat.")
                break
        except:
            break

def broadcast_message(room_num, message):
    for conn in chatrooms[room_num]:
        try:
            conn.send(message.encode())
        except: 
            close_connection(conn)
            chatrooms[room_num].remove(conn) 

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
    if chat_room_num == 1:
        conn.send("No chat rooms available!".encode())
        return None
    room_selection = 0
    while room_selection < 1 or room_selection > chat_room_num - 1:
        conn.send("Select a chatroom to join:\n".encode())
        for num in range(1, chat_room_num):
            conn.send(f"Chatroom {num}\n".encode())
        conn.send("Join chat room #: ".encode())
        room_selection = conn.recv(2048).decode()
        try:
            room_selection = int(room_selection)
        except ValueError:
            conn.send("ERROR: Non integer response detected.\n")
            room_selection = 0
        if room_selection < 1 or room_selection > chat_room_num - 1:
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