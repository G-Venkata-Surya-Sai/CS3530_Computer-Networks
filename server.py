import socket
import threading
import time
import os

# GV IP Address = "192.168.0.125"
IP_ADDR = socket.gethostbyname(socket.gethostname())
PORT = 1525
FORMAT = "utf-8"
SIZE = 1024
ADDRESS = (IP_ADDR, PORT)
PATH = "/home/g/sem5/computer_networks/socket_programming/server/"

print(f"[SERVER] Server IP Address is: {IP_ADDR}")

def list_to_string(s):
    str = "["
    for i in s:
        str += i + ","
    str += "]"
    return str


def client_request(client_socket,address):
    print("[SERVER] New client connected with address " + str(address))
    connected = True
    while connected:
        message = client_socket.recv(SIZE).decode(FORMAT)
        commandLine = message.partition(' ')

        if (commandLine[0] == "exit"):
            print("[SERVER] Client with address: " + str(address) + " is disconnected.")
            connected = False
        
        elif (commandLine[0] == "ls"):
            dir_list = os.listdir(PATH)
            client_socket.send(list_to_string(dir_list).encode(FORMAT))
            print("[SERVER] Displayed list of all the files to the client.")

        elif (commandLine[0] == "download"):
            print(f"[SERVER] Client with {address} is requesting for {commandLine[2]}.")
            file = open(PATH + commandLine[2], "rb")
            
            list = []
            data = file.read(SIZE)
            list.append(data)
            while data:
                data = file.read(SIZE)
                if data:
                    list.append(data)
                
            # length of the list
            length = len(list)
            send_length = str(length).encode(FORMAT)
            client_socket.send(send_length)
            
            # sleeping for a second 
            time.sleep(1)
            
            # sending one by one in the list
            for i in list:
                client_socket.send(i)

            print(f"[SERVER] {commandLine[2]} file sent to requested client.")
            
            time.sleep(1)

            # sending the file size
            file_size = os.path.getsize(PATH + commandLine[2])
            file_size = str(file_size)
            file_size = str(file_size).encode()
            client_socket.send(file_size)
            file.close()
        
        elif (commandLine[0] == "upload"):
            file = open(PATH + commandLine[2] ,"wb")

            # length of the list
            msg_length = client_socket.recv(SIZE)
            msg_length = msg_length.decode()
            msg_length = int(msg_length)
            
            for i in range(msg_length):
                file.write(client_socket.recv(SIZE))

            file_size = client_socket.recv(SIZE)
            file_size = file_size.decode(FORMAT)
            file_size = int(file_size)

            print(f"[SERVER]: {commandLine[2]} file of size {file_size} bytes received from a client.")
            file.close()
        
        elif (commandLine[0] == "feedback"):
            print(f"[SERVER] Client's Feedback: {commandLine[2]}")

    print("[SERVER] No of active threads running now: ", threading.active_count()-2)
    client_socket.close()

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(ADDRESS)

print("[SERVER] Server Waiting.....")
server_socket.listen(5)
while True:
    (client_socket,address) = server_socket.accept()

    # password
    password = "CS3530"   
    while True:
        user_pass = client_socket.recv(SIZE).decode()
        if(user_pass == password):
            client_socket.send("ACCEPTED".encode())
            print("[SERVER] A client accessed the server.")
            break
        else: 
            client_socket.send("REJECTED".encode())
    thread = threading.Thread(target = client_request, args = (client_socket,address))
    thread.start()
    print("[SERVER] No. of Active Threads: ", threading.active_count()-1) 