import platform
import subprocess
import psutil
import socket

def os_info():
  # Информация об ОС
  print(f"Операционная система: {platform.system()} {platform.version()}")
  print(f"Имя компьютера: {socket.gethostname()}")

  # Имя Wi-Fi сети
  if platform.system() == "Windows":
      command = "netsh wlan show interfaces"
      result = subprocess.run(command, capture_output=True, text=True, encoding='cp866', shell=True)
      
      # Проверяем, что команда выполнена успешно и stdout не равен None
      if result.returncode == 0 and result.stdout:
          for line in result.stdout.splitlines():
              if "SSID" in line and "BSSID" not in line:
                  ssid = line.split(":")[1].strip()
                  print(f"Имя Wi-Fi сети: {ssid}")
                  break
      else:
          print("Не удалось получить имя Wi-Fi сети.")
          if result.stderr:
              print(f"Ошибка: {result.stderr}")

  # Linux
  elif platform.system() in ["Linux", "Darwin"]:
      command = "iwgetid -r"
      result = subprocess.run(command, capture_output=True, text=True, encoding='cp866', shell=True)
      if result.returncode == 0 and result.stdout:
          print(f"Имя Wi-Fi сети: {result.stdout.strip()}")
      else:
          print("Не удалось получить имя Wi-Fi сети.")
          if result.stderr:
              print(f"Ошибка: {result.stderr}")

  # Информация о системе
  print(f"Количество ядер CPU: {psutil.cpu_count(logical=True)}")
  print(f"Загрузка CPU: {psutil.cpu_percent(interval=1)}%")
  print(f"Всего памяти: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB")
