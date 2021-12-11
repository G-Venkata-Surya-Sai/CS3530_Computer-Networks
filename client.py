import socket
import time
import os

# GV IP Address = "192.168.0.125"
IP_ADDR = socket.gethostbyname(socket.gethostname())
PORT = 1525
FORMAT = "utf-8"
SIZE = 1024
ADDRESS = (IP_ADDR, PORT)
PATH = "/home/g/sem5/computer_networks/socket_programming/client/"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client_socket.connect(ADDRESS)

# password encryption
password = input("[CLIENT] Enter the password to access the server: ")
tries = 1

while True:
    client_socket.send(password.encode())
    output = client_socket.recv(SIZE).decode()
    if(output == "ACCEPTED"):
        print("[CLIENT] ACCESS GRANTED!")
        break
    if(tries == 5):
        print("[CLIENT] Too many tries. Exited.")
        quit()
    password = input("[CLIENT] Sorry! Try again: ")
    tries += 1

# password

read = input("[CLIENT] Enter a command to run:\n> ")
while True:
    client_socket.send(read.encode(FORMAT))
    commandLine = read.partition(' ')    
    
    if (commandLine[0] == "exit"):
        print("[CLIENT] Successfully disconnected from the server.")
        break

    elif (commandLine[0] == "ls"):
        print("[CLIENT] List of all the files in the directory: ")
        print(client_socket.recv(SIZE).decode(FORMAT))

    elif (commandLine[0] == "download"):
        file = open(PATH + commandLine[2], "wb")
        
        # length of the list
        msg_length = client_socket.recv(SIZE)
        msg_length = msg_length.decode()
        msg_length = int(msg_length)

        for i in range(msg_length):
            file.write(client_socket.recv(SIZE))
        
        file_size = client_socket.recv(SIZE)
        file_size = file_size.decode(FORMAT)
        file_size = int(file_size)
        print(f"[CLIENT] {commandLine[2]} file of size {file_size} bytes downloaded from server upon request.")
        file.close()
    
    elif (commandLine[0] == "upload"):
        file = open(PATH + commandLine[2],"rb")
        
        list = []
        data = file.read(SIZE)
        list.append(data)
        while data:
            data = file.read(SIZE)
            if data:
                list.append(data) 

        # length of the list
        length = len(list)
        send_length = str(length).encode()
        client_socket.send(send_length)
        
        time.sleep(1)
        # sending one by one in the list
        for i in list:
            client_socket.send(i)

        print(f"[CLIENT] {commandLine[2]} uploaded to the server.")

        time.sleep(1)

        file_size = os.path.getsize(PATH + commandLine[2])
        file_size = str(file_size)
        file_size = str(file_size).encode()
        client_socket.send(file_size)

        file.close() 

    elif (commandLine[0] == "feedback"):
        print(f"[CLIENT] message sent to the server.")

    read = input("[CLIENT] Enter another command to run:\n> ")