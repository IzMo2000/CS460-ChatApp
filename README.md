How to run the code:
In the first terminal you want to run the command python3 server.py IP address 8181. The ip address will be your server id address and the port 8181. Once the server is listening. Open another terminal and use the command python3 client.py IP address 8181 . The id address and the port should be the same as the sever. You will be told to enter a name. Enter a name, then I would go and open another terminal. This terminal command should be python3 client.py IP. Then you will enter the name of the second person. You then will want to pick a chat room, have one of the clients pick chat room 1, and then the second client can pick 2 or 1. There you can talk back to each other. When you are done talking, you will hit enter and there you will be able to enter another chat room or leave the chat room as whole. When checking the demo.pcap, you should type in the tcp in the top of wireshark. 

Terminal One: python3 server.py 104.168.162.191 8181
Terminal Two: python3 client.py 104.168.162.191
Terminal Three: python3 client.py 104.168.162.191

104.168.162.191 -server
134.114.101.51 - client 
18.222.144.221 - client
