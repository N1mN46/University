import socket

HOST = '127.0.0.1'  
PORT = 12345        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    message = "куку!"
    print(f"Відправка: {message}")
    s.sendall(message.encode('utf-8')) 
    data = s.recv(1024) 

print(f"Отримано від сервера: {data.decode('utf-8')}")