# server.py
import socket
import threading

PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

clients, names = [], []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def startChat():
    print("O servidor está funcionando em " + SERVER)
    server.listen()

    while True:
        conn, addr = server.accept()
        conn.send("NAME".encode(FORMAT))
        name = conn.recv(1024).decode(FORMAT)
        names.append(name)
        clients.append(conn)
        print(f"Nome: {name}")
        broadcastMessage(f"{name} entrou na sala!".encode(FORMAT))
        conn.send('Conexão bem-sucedida!'.encode(FORMAT))
        thread = threading.Thread(target=handle, args=(conn, addr))
        thread.start()
        print(f"Conexões ativas: {threading.activeCount() - 1}")

def handle(conn, addr):
    print(f"Nova conexão: {addr}")
    connected = True

    while connected:
        message = conn.recv(1024)
        broadcastMessage(message)

    conn.close()

def broadcastMessage(message):
    for client in clients:
        client.send(message)

startChat()