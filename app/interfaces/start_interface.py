import sys
import sqlite3
import asyncio
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QLineEdit, QMessageBox, QFileDialog, QDialog,
                            QMainWindow, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from qasync import asyncSlot, QEventLoop

#* Импорты моих библиотек
# Основное окно
from .main_interface import MainWindow
# Лицензия
from .license_interface import LicenseAgreementDialog
# Файл со стилями
from .utils.style.style_variables_editable import editable_colors


#! Класс Стартового окна

class StartWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    # Настройка основного окна
    self.setWindowTitle("KRAKEN - System control")

    # Иконка приложения
    self.setWindowIcon(QIcon("resources/img/imgReadme/kraken.jpg"))

    self.setGeometry(350, 100, 800, 600)  # x, y, width, height

    # Применяем стили
    self.setStyleSheet(f"""
      QWidget {{
        background-color: #{editable_colors["QWidget_bc"]};  /* Темно-серый фон */
        color: #{editable_colors["text_color"]};  /* Белый текст */
      }}
      QPushButton {{
        background-color: #{editable_colors["button_bc"]};  /* Серый фон кнопок */
        color: #{editable_colors["text_color"]};  /* Белый текст */
        border: 1px solid #{editable_colors["border_color"]};  /* Голубая рамка */
        padding: 5px;
        border-radius: 3px;
      }}
      QPushButton:hover {{
        background-color: #{editable_colors["border_color"]};  /* Голубой фон при наведении */
        color: #{editable_colors["button_color_hover"]};  /* Темный текст */
      }}
      QLineEdit, QTextEdit {{
        background-color: #{editable_colors["input_area"]};  /* Темно-серый фон полей ввода */
        color: #{editable_colors["text_color"]};  /* Белый текст */
        border: 1px solid #{editable_colors["border_color"]};  /* Голубая рамка */
        padding: 5px;
        border-radius: 3px;
      }}
      QTableWidget {{
        background-color: #{editable_colors["input_area"]};  /* Темно-серый фон таблицы */
        color: #{editable_colors["text_color"]};  /* Белый текст */
        gridline-color: #{editable_colors["border_color"]};  /* Голубые линии сетки */
      }}
      QHeaderView::section {{
        background-color: #{editable_colors["button_bc"]};  /* Серый фон заголовков таблицы */
        color: #{editable_colors["text_color"]};  /* Белый текст */
        padding: 5px;
        border: 1px solid #{editable_colors["border_color"]};  /* Голубая рамка */
      }}
      QScrollArea {{
        background-color: #{editable_colors["button_color_hover"]};  /* Темно-серый фон */
        border: none;
      }}
      QLabel {{
        color: #{editable_colors["text_color"]};  /* Белый текст */
      }}
    """)
    # Инициализация начального интерфейса
    self.init_ui()

  def init_ui(self):
    """
    Инициализация начального интерфейса с надписью, логотипом и кнопкой START.
    """
    # Создаем центральный виджет и основной layout
    self.central_widget = QWidget()
    self.setCentralWidget(self.central_widget)
    self.main_layout = QVBoxLayout(self.central_widget)
    self.main_layout.setAlignment(Qt.AlignCenter)  # Выравнивание по центру
    # Надпись "Hack with KRAKEN"
    self.title_label = QLabel("Hack with KRAKEN")
    self.title_label.setAlignment(Qt.AlignCenter)
    self.main_layout.addWidget(self.title_label)
    # Логотип
    self.logo_label = QLabel()
    self.logo_label.setPixmap(QPixmap("resources/img/imgReadme/kraken.jpg").scaled(200, 200, Qt.KeepAspectRatio))
    self.logo_label.setAlignment(Qt.AlignCenter)
    self.main_layout.addWidget(self.logo_label)
    # Кнопка START
    self.start_button = QPushButton("START")
    self.start_button.setFixedSize(150, 50)  # Фиксированный размер кнопки
    self.start_button.clicked.connect(self.change_interface)
    self.main_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

  @asyncSlot()
  async def change_interface(self):
    """
    Меняет интерфейс после нажатия кнопки START.
    """
    # Очищаем текущий интерфейс
    self.clear_interface()
    # Создаем две кнопки: "Создать" и "Подключиться"
    self.create_button = QPushButton("Создать")
    self.create_button.setFixedSize(150, 50)
    self.create_button.clicked.connect(self.create_interface)
    
    self.connect_button = QPushButton("Подключиться")
    self.connect_button.setFixedSize(150, 50)
    self.connect_button.clicked.connect(self.connect_to_db)
    # Добавляем кнопки в layout
    self.main_layout.addWidget(self.create_button)
    self.main_layout.addWidget(self.connect_button)

  #* Создаём клиент(ввод данных)
  @asyncSlot()
  async def create_interface(self):
    """
    Создает интерфейс для выбора пути и ввода данных.
    """
    self.clear_interface()
    
    # Поле для выбора пути
    self.path_layout = QHBoxLayout()
    self.path_input = QLineEdit()
    self.path_input.setPlaceholderText("Выберите путь для создания файла")
    self.path_button = QPushButton("Выбрать путь")
    self.path_button.clicked.connect(self.select_path)
    self.path_layout.addWidget(self.path_input)
    self.path_layout.addWidget(self.path_button)
    self.main_layout.addLayout(self.path_layout)

    # Поля ввода для Name, IP, Port
    self.name_input = QLineEdit()
    self.name_input.setPlaceholderText("Name")
    self.main_layout.addWidget(self.name_input)

    self.ip_input = QLineEdit()
    self.ip_input.setPlaceholderText("IP")
    self.main_layout.addWidget(self.ip_input)

    self.port_input = QLineEdit()
    self.port_input.setPlaceholderText("Port")
    self.main_layout.addWidget(self.port_input)

    # Кнопка "Создать"
    self.create_db_button = QPushButton("Создать")
    self.create_db_button.clicked.connect(self.create_database)
    self.main_layout.addWidget(self.create_db_button, alignment=Qt.AlignCenter)

  # Выбор пути для сохранения файла
  @asyncSlot()
  async def select_path(self):
    """
    Открывает проводник для выбора пути.
    """
    path = QFileDialog.getExistingDirectory(self, "Выберите путь")
    if path:
      self.path_input.setText(path)

  # Создание клиента
  @asyncSlot()
  async def create_database(self):
    """
    Создает SQLite таблицу, если IP корректен.
    """
    ip = self.ip_input.text().strip()
    if not self.validate_ip(ip):
      QMessageBox.warning(self, "Ошибка", "Некорректный IP")
      return

    # Получаем путь и имя базы данных
    path = self.path_input.text().strip()
    if not path:
      QMessageBox.warning(self, "Ошибка", "Выберите путь для создания файла")
      return


    # Показываем сообщение о начале загрузки
    QMessageBox.information(self, "Информация", "Загрузка .exe client начнётся после нажатия ОК, не закрывайте окно")
    
    '''ТУТ БУДЕТ ФУНКЦИЯ УПАКОВКИ СКРИПТА'''
    #todo Запуск Терминала
    await self.run_MainWindow()



  @asyncSlot()
  async def connect_to_db(self):
    """
    Проверяет наличие данных в БД и отображает их в таблице, если данные есть.
    """
    try:
      conn = sqlite3.connect("sqlite.db")
      cursor = conn.cursor()
      # Проверка наличия данных в таблице (предположим, что таблица называется 'connection_table')
      cursor.execute("SELECT name, ip, port FROM connection_table")
      result = cursor.fetchall()

      if result:
        # Если данные есть, отображаем их в таблице
        self.clear_interface()
        self.main_layout.addWidget(QLabel("Ваши поклонники", alignment=Qt.AlignCenter))

        # Создаем таблицу
        self.table = QTableWidget(len(result), 3)
        self.table.setHorizontalHeaderLabels(["Имя", "IP", "Port"])
        for row_idx, row_data in enumerate(result):
          for col_idx, col_data in enumerate(row_data):
            self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        self.main_layout.addWidget(self.table)

        # Добавляем кнопку "Продолжить"
        self.continue_button = QPushButton("Продолжить")
        self.continue_button.clicked.connect(self.run_MainWindow)
        self.main_layout.addWidget(self.continue_button, alignment=Qt.AlignCenter)
      else:
        # Если данных нет, выводим сообщение
        QMessageBox.information(self, "Нет данных", ":( У вас пока нету поклонников")
    except sqlite3.Error as e:
      QMessageBox.critical(self, "Ошибка", f"Ошибка при подключении к базе данных: {e}")
    finally:
      if conn:
        conn.close()

  # Очистка интерфейса
  def clear_interface(self):
    """
    Очищает текущий интерфейс, удаляя все виджеты.
    """
    for i in reversed(range(self.main_layout.count())):
      widget = self.main_layout.itemAt(i).widget()
      if widget:
        widget.setParent(None)


  # Проверка что ip введён правильно
  def validate_ip(self, ip):
    """
    Проверяет корректность IP-адреса.
    """
    parts = ip.split(".")
    if len(parts) != 4:
      return False
    for part in parts:
      try:
        num = int(part)
        if num < 0 or num > 255:
          return False
      except ValueError:
        return False
    return True

  #TODO: Функция Смены окон и открытия основного
  @asyncSlot()
  async def run_MainWindow(self):
    # Скрываем нынешнее окно
    self.hide()
    # Создаём и отображаем новое окно
    self.main_window = MainWindow()
    self.main_window.show()





# ЗАПУСК 
if __name__ == "__main__":
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