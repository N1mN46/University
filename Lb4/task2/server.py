import socket

HOST = '127.0.0.1'
PORT = 12345

print(f"Запуск постійного сервера на {HOST}:{PORT}...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()

    while True:
        print("Очікування клієнта...")
        conn, addr = s.accept()
        
        with conn: 
            print(f"З'єднано: {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"Клієнт {addr} відключився.")
                    break
                conn.sendall(data)