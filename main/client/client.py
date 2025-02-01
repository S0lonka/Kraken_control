import socket
import os
import subprocess

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
      # ! КАКАЯ ЖЕ ЭТА ЕБАННАЯ ССАНИНА Я ЕГО МАТЬ ЕБАЛ
      try:
        # Выполнение команды и получение результата
        output = subprocess.run(command, capture_output=True, text=True, shell=True)
        response = output.stdout + output.stderr
        print(output.stdout)
        if response == "" or response == None:
          s.sendall("Команда выполнилась без вывода".encode())
      # ! РОССУМ КОНЧЕННЫЙ ХУЕСОС С ЕГО ЕБАНЫМ ЯЗЫКОМ Я НЕНАВИЖУ СВОЮ РАБОТУ
      except Exception as e:
        response = str(e)

      # Отправка результата обратно на сервер
      s.sendall(response.encode())


if __name__ == "__main__":
  start_client("127.0.0.1", 65432)
