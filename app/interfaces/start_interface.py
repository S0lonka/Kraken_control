import asyncio
import sqlite3
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QLineEdit, QMessageBox, QFileDialog,
                            QMainWindow, QTableWidget, QTableWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
import logging
from qasync import asyncSlot

#* Импорты моих библиотек
# Основное окно
from .main_interface import MainWindow
# Файл со стилями
from .utils.style.style_variables_editable import editable_colors

import os
import sys

# Функция для получения иконки в exe
def resource_path(relative_path):
  """ Получить абсолютный путь к ресурсу. """
  if hasattr(sys, '_MEIPASS'):
    # Если приложение собрано в один файл (--onefile)
    base_path = sys._MEIPASS
  else:
    # Если приложение запущено из исходного кода
    base_path = os.path.abspath(".")

  return os.path.join(base_path, relative_path)

logging.basicConfig(
  level=logging.DEBUG,
  format="%(asctime)s [%(levelname)s] %(message)s",
  handlers=[
    logging.FileHandler("kraken.log"),
    logging.StreamHandler()
  ]
)

def handle_exception(exc_type, exc_value, exc_traceback):
  """Обработчик необработанных исключений."""
  logging.error("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))


# Перехват необработанных исключений
sys.excepthook = handle_exception

#! Класс Стартового окна
class StartWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    # Настройка основного окна
    self.setWindowTitle("KRAKEN - System control")

    # Иконка приложения
    self.icon_path = resource_path("resources/img/kraken.jpg")
    self.setWindowIcon(QIcon(self.icon_path))

    self.setGeometry(350, 100, 800, 600)  # x, y, width, height

    # Получаем путь к БД
    self.db_path = resource_path('app/sqlite.db')

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
    self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Выравнивание по центру
    # Надпись "Hack with KRAKEN"
    self.title_label = QLabel("Hack with KRAKEN")
    self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.main_layout.addWidget(self.title_label)
    # Логотип
    self.logo_label = QLabel()
    # icon_path = resource_path("resources/img/kraken.jpg")
    self.logo_label.setPixmap(QPixmap(self.icon_path).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
    self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.main_layout.addWidget(self.logo_label)
    # Кнопка START
    self.start_button = QPushButton("START")
    self.start_button.setFixedSize(150, 50)  # Фиксированный размер кнопки
    self.start_button.clicked.connect(self.change_interface)
    self.main_layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

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


  @asyncSlot()
  async def create_interface(self):
    """
    Создает интерфейс для выбора пути и ввода данных.
    """
    self.clear_interface()
    
    # Кнопка "Назад" в верхнем левом углу
    self.back_button = QPushButton("Назад")
    self.back_button.clicked.connect(self.change_interface)
    self.main_layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

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
    self.main_layout.addWidget(self.create_db_button, alignment=Qt.AlignmentFlag.AlignCenter)

  # Выбор пути для сохранения файла
  def select_path(self):
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
    Создает SQLite таблицу или добавляет туда данные
    """

    # передаём записанные данные в переменную
    name = self.name_input.text().strip()
    ip = self.ip_input.text().strip()
    port = self.port_input.text().strip()

    # Проверка что ip правилен
    if not self.validate_ip(ip):
      QMessageBox.warning(self, "Ошибка", "Некорректный IP")
      return

    # Проверяем, что все поля заполнены
    if not name or not ip or not port:
      QMessageBox.warning(self, "Ошибка", "Заполните все поля")
      return


    # Получаем путь и имя базы данных
    path = self.path_input.text().strip()
    if not path:
      QMessageBox.warning(self, "Ошибка", "Выберите путь для создания файла")
      return

    # Показываем сообщение о начале загрузки
    QMessageBox.information(self, "Информация", "Загрузка .exe client начнётся после нажатия ОК, не закрывайте окно")
    

    '''ТУТ БУДЕТ ФУНКЦИЯ УПАКОВКИ СКРИПТА'''

    self.run_MainWindow()
    # Заносим данные в БД (потом добавлять только если клиент успешно упакован)
    self.create_client_db()

    #todo Запуск Терминала
    


  # Создание Клиента в БД
  @asyncSlot()
  async def create_client_db(self):
    """
    Создает таблицу в базе данных SQLite (если её нет) и добавляет в неё данные, введенные пользователем.
    """

    # Получаем данные из полей ввода
    name = self.name_input.text()
    ip = self.ip_input.text()
    port = self.port_input.text()

    # Подключаемся к базе данных (файл sqlite.db)
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()

    try:
      # Создаем таблицу, если её нет
      cursor.execute('''
        CREATE TABLE IF NOT EXISTS connection_table (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          ip TEXT NOT NULL,
          port TEXT NOT NULL
        )
      ''')

      # Вставляем данные в таблицу
      cursor.execute('''
        INSERT INTO connection_table (name, ip, port)
        VALUES (?, ?, ?)
      ''', (name, ip, port))

      # Сохраняем изменения
      conn.commit()
      print("Данные успешно добавлены в таблицу!")

    except sqlite3.Error as e:
      print(f"Ошибка при работе с базой данных: {e}")

    finally:
      # Закрываем соединение с базой данных
      conn.close()



  # Отображает таблицу если она есть
  @asyncSlot()
  async def connect_to_db(self):
    """
    Проверяет наличие данных в БД и отображает их в таблице, если данные есть.
    """
    try:
      conn = sqlite3.connect(self.db_path)
      cursor = conn.cursor()
      # Проверка наличия данных в таблице (предположим, что таблица называется 'connection_table')
      cursor.execute("SELECT name, ip, port FROM connection_table")
      result = cursor.fetchall()

      if result:
        # Если данные есть, отображаем их в таблице
        self.clear_interface()

        # Создаем верхний макет для кнопки "Назад"
        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        self.top_layout.setSpacing(0)  # Убираем промежутки между элементами

        # Кнопка "Назад" в верхнем левом углу
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.change_interface)
        self.top_layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Добавляем верхний макет в основной макет
        self.main_layout.addLayout(self.top_layout)

        # Заголовок
        self.main_layout.addWidget(QLabel("Ваши поклонники", alignment=Qt.AlignmentFlag.AlignCenter))

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
        self.main_layout.addWidget(self.continue_button, alignment=Qt.AlignmentFlag.AlignCenter)
      else:
        # Если данных нет, выводим сообщение
        QMessageBox.information(self, "Нет данных", ":( У вас пока нету поклонников")
    except sqlite3.Error as e:
      QMessageBox.critical(self, "Ошибка", f"Возможно БД ещё не создана. Ошибка при подключении к базе данных: {e}")
    finally:
      if conn:
        conn.close()



  # Очистка интерфейса
  def clear_interface(self):
    """
    Очищает текущий интерфейс, удаляя все виджеты и макеты.
    """
    # Удаляем все виджеты и макеты из main_layout
    while self.main_layout.count():
      item = self.main_layout.takeAt(0)  # Берем первый элемент макета
      if item.widget():
        # Если элемент — виджет, удаляем его
        widget = item.widget()
        widget.setParent(None)
        widget.deleteLater()  # Освобождаем память
      elif item.layout():
        # Если элемент — макет, рекурсивно удаляем его содержимое
        self._clear_layout(item.layout())

  # Очистка layout для функции очистки интерфейсов
  def _clear_layout(self, layout):
    """
    Рекурсивно очищает макет и удаляет все его виджеты и вложенные макеты.
    """
    if layout is None:
      return

    while layout.count():
      item = layout.takeAt(0)
      if item.widget():
        widget = item.widget()
        widget.setParent(None)
        widget.deleteLater()
      elif item.layout():
        self._clear_layout(item.layout())
      elif item.spacerItem():
        layout.removeItem(item)


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
  def run_MainWindow(self):
    try:
      self.hide()
      # Создаём и отображаем новое окно
      self.main_window = MainWindow()
      self.main_window.show()
      asyncio.get_event_loop().run_forever()
    except Exception as e:
      logging.error("Ошибка при создании MainWindow", exc_info=True)
