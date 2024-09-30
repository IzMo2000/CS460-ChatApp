import socket 
import select 
import sys 
from _thread import *

chat_room_num = 1

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

def client_thread(conn, addr):
    conn.send("Welcome! If you would like to disconnect, press Enter (no input)")
    conn.send("Please enter your username: ".encode())
    username = conn.recv(2048).decode().strip()
    if username == "":
        print("Client closed connection")
        conn.close()
        return
    conn.send(f"Welcome to the chat app, {username}! Here are your options:\n".encode())
    
    while True:
        try:
            action = prompt_actions(conn)
            selected_room = 0
            if action == '1':
                selected_room = chat_room_num
                chatrooms[chat_room_num] = [conn]
                chat_room_num += 1
            else:
                selected_room = select_chat_room(conn)
                if selected_room is None:
                    continue
            join_chat_room(conn, addr, selected_room)
                
                
                    

                
def join_chat_room(conn, addr, room_num):
    return

def prompt_actions(conn, addr):
    user_input = ""
    while user_input not in ('1', '2'):
        conn.send("1. Create and Join a New Server\n".encode())
        conn.send("2. Join an Existing Server\n".encode())
        conn.send("Please choose 1 or 2: \n".encode())
        user_input = conn.recv(2048).decode()
        if user_input not in ('1', '2'):
            conn.send("ERROR: Input other than '1' or '2' received. Try again:".encode())
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