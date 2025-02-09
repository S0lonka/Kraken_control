# Запуск приложения
import sys
import asyncio
from PyQt5.QtWidgets import (QApplication,QDialog)
from qasync import QEventLoop


# Импорты моих модулей
from interfaces.license_interface import LicenseAgreementDialog
from interfaces.start_interface import StartWindow

def main():
  app = QApplication(sys.argv)
  loop = QEventLoop(app)
  asyncio.set_event_loop(loop)

  if LicenseAgreementDialog().exec_() == QDialog.Accepted:
    start_window = StartWindow()
    start_window.show()

    with loop:
      loop.run_forever()
  else:
    sys.exit()  # Завершаем программу, если лицензия не принята

if __name__ == "__main__":
  main()