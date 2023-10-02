# server.py
import socket
import threading

# Configurações de rede
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

# Listas para armazenar informações dos clientes conectados
clients, names = [], []

# Configuração do servidor de socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def startChat():
    """
    Inicia o servidor de chat.

    Este método configura o servidor de socket, inicia a escuta de conexões
    e cria uma thread para lidar com cada cliente conectado.
    """
    print("O servidor está funcionando em " + SERVER)
    server.listen()

    while True:
        conn, addr = server.accept()

        # Solicita ao cliente que forneça um nome
        conn.send("NAME".encode(FORMAT))
        name = conn.recv(1024).decode(FORMAT)
        names.append(name)
        clients.append(conn)
        print(f"Nome: {name}")

        # Notifica a todos que um novo cliente entrou na sala
        broadcastMessage(f"{name} entrou na sala!".encode(FORMAT))

        # Envie uma mensagem de confirmação para o cliente recém-conectado
        conn.send('Conexão bem-sucedida!'.encode(FORMAT))

        # Inicia uma thread para lidar com o cliente
        thread = threading.Thread(target=handle, args=(conn, addr))
        thread.start()
        print(f"Conexões ativas: {threading.activeCount() - 1}")

def handle(conn, addr):
    """
    Lida com uma conexão de cliente individual.

    Este método recebe mensagens do cliente e as retransmite para todos os outros clientes.
    Quando a conexão com o cliente é encerrada, a função encerra.
    """
    print(f"Nova conexão: {addr}")
    connected = True

    while connected:
        message = conn.recv(1024)
        broadcastMessage(message)

    conn.close()

def broadcastMessage(message):
    """
    Envia uma mensagem para todos os clientes conectados.

    Este método itera sobre a lista de clientes e envia a mensagem especificada para cada um deles.
    """
    for client in clients:
        client.send(message)

# Inicia o servidor de chat
startChat()
