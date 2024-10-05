# How to run the code

## Running the server

On the server host, enter the following command:

`python3 server.py ip_address`

where `ip_address` is the ip address associated with the host running the server

## Connecting to the server

To connect to the server, enter the following command:

`python3 client.py ip_address`

where `ip_address` is the same ip used for the last command - we are trying to connect to the server at this address

## Chatroom operations

When the server is accessed, the client will be told to enter a name. After entering the name (or disconnecting using Enter), the client can select from the following options:

```
1. Create and Join a New Server
2. Join an Existing Server
3. Disconnect
```

Assuming the user has then joined a chat room from this point, they will be able to send messages to other users in this room by submitting a message. They can see the messages in the chat room using `/read` while in the chat room. They can then leave and disconnect from the server using `/exit` while in the chat room.

# Interpretting demo.pcap

When checking the demo.pcap, you should apply the filter `tcp` in the top of wireshark.

The following commands were ran, with Terminal 1 being the server and Terminals 2 & 3 being the clients:

Terminal One, 104.168.162.191: `python3 server.py 104.168.162.191`

Terminal Two, 134.114.101.51: `python3 client.py 104.168.162.191`

Terminal Three, 18.222.144.221: `python3 client.py 104.168.162.191`

The clients then both joined the same chat room, exchanged a message each, and closed out their connections.
