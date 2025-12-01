import socket

HOST = '127.0.0.1'
PORT = 12345

print(f"Сервер слухає на {HOST}:{PORT}...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Прийом файлу від {addr}...")
            
            with open('file.txt', 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
            
            print("Файл  отримано та збережено як 'file.txt'")
            conn.sendall(b"File received successfully")