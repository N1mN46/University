import socket
import os

HOST = '127.0.0.1'
PORT = 12345
FILENAME = 'send.txt'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Відправка файлу {FILENAME}...")

        with open(FILENAME, 'rb') as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break 
                s.sendall(chunk)
        
        s.shutdown(socket.SHUT_WR)

        response = s.recv(1024)
        print(f"Відповідь сервера: {response.decode()}")