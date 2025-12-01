import socket

HOST = '127.0.0.1'  
PORT = 12345        

print(f"Запуск Echo-сервера на {HOST}:{PORT}...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Очікування з'єднання...")
    
    conn, addr = s.accept() 
    with conn:
        print(f"З'єднано: {addr}")
        while True:
            data = conn.recv(1024) 
            if not data:
                break 
            print(f"Отримано: {data.decode()}")
            conn.sendall(data) 