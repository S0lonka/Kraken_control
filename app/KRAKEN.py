# Запуск приложения
import sys
import asyncio
from PyQt6.QtWidgets import (QApplication,QDialog)
from qasync import QEventLoop

# Импорты моих модулей
from interfaces.license_interface import LicenseAgreementDialog
from interfaces.main_interface import MainWindow


def main():
  app = QApplication(sys.argv)
  loop = QEventLoop(app)
  asyncio.set_event_loop(loop)

  if LicenseAgreementDialog().exec() == QDialog.DialogCode.Accepted:
    main_window = MainWindow()
    main_window.show()

    with loop:
      loop.run_forever()
  else:
    sys.exit()  # Завершаем программу, если лицензия не принята

# Функция очистки логгера
def log_clear():
  # Открываем файл в режиме записи, что очищает его содержимое
  with open("kraken.log", 'w') as file:
    pass  # Ничего не записываем, просто очищаем файл


if __name__ == "__main__":
  # Очищаем логгер
  log_clear()
  # Запускаем основной скрипт
  main()
