import socket

def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Сервер запущен на {host}:{port}. Ожидание подключения клиента...")

        conn, addr = s.accept()
        with conn:
            print('Подключен к', addr)
            while True:
                command = input("Введите команду для выполнения на клиенте (или 'exit' для выхода): ")
                if command.lower() == 'exit':
                    break
                conn.sendall(command.encode())
                response = conn.recv(1024).decode()
                print(f"Ответ клиента: {response}")

if __name__ == "__main__":
    q = input("Укажите в формате айпи:порт сервера (по умолчанию 127.0.0.1:65432)")
    start_server(q.split(":")[0], int(q.split(":")[1]))
