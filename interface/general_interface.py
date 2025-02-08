import sys
import sqlite3
import asyncio
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QLabel, QScrollArea, QTableWidget, 
                             QTableWidgetItem, QLineEdit, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from qasync import asyncSlot, QEventLoop
import discordrp
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("kraken.log"),
        logging.StreamHandler()
    ]
)


#! Класс Основного окна
class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    #! Основные настройки
    # Настройка основного окна
    self.setWindowTitle("KRAKEN - System control")

    # Иконка приложения
    icon_path = "img/imgReadme/kraken.jpg" 
    self.setWindowIcon(QIcon(icon_path))

    # x, y, width, height
    self.setGeometry(200, 100, 1200, 700)

    # Применяем стили
    self.setStyleSheet("""
      QWidget {
        background-color: #2E3440;  /* Темно-серый фон */
        color: #ECEFF4;  /* Белый текст */
      }
      QPushButton {
        background-color: #4C566A;  /* Серый фон кнопок */
        color: #ECEFF4;  /* Белый текст */
        border: 1px solid #81A1C1;  /* Голубая рамка */
        padding: 5px;
        border-radius: 3px;
      }
      QPushButton:hover {
        background-color: #81A1C1;  /* Голубой фон при наведении */
        color: #2E3440;  /* Темный текст */
      }
      QLineEdit, QTextEdit {
        background-color: #3B4252;  /* Темно-серый фон полей ввода */
        color: #ECEFF4;  /* Белый текст */
        border: 1px solid #81A1C1;  /* Голубая рамка */
        padding: 5px;
        border-radius: 3px;
      }
      QTableWidget {
        background-color: #3B4252;  /* Темно-серый фон таблицы */
        color: #ECEFF4;  /* Белый текст */
        gridline-color: #81A1C1;  /* Голубые линии сетки */
      }
      QHeaderView::section {
        background-color: #4C566A;  /* Серый фон заголовков таблицы */
        color: #ECEFF4;  /* Белый текст */
        padding: 5px;
        border: 1px solid #81A1C1;  /* Голубая рамка */
      }
      QScrollArea {
        background-color: #2E3440;  /* Темно-серый фон */
        border: none;
      }
      QLabel {
        color: #ECEFF4;  /* Белый текст */
      }
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
    self.db_connection = sqlite3.connect("sqlite.db")  # Укажите путь к вашей базе данных
    self.cursor = self.db_connection.cursor()

    # Создаем тестовую таблицу, если её нет
    self.create_connection_table()

    # Переменная для хранения состояния сервера
    self.server_running = False
    self.clientid = "1337766338621607997"



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

    # Вывод предупреждения
    warning_message = """<font color='red'>Внимание!</font>\n
Данное программное обеспечение разработано исключительно в образовательных целях и для тестирования системной безопасности с разрешения владельца системы.
Незаконное или несанкционированное использование может нарушать законы и привести к уголовной или административной ответственности.
Разработчики не несут ответственности за любые последствия использования данного ПО.
Помните: безопасность начинается с ответственности!
бог любит вас."""
    self.terminal_output.append(warning_message)
    logging.info("Предупреждение отображено в терминале")

  async def handle_client(self, reader, writer):
    logging.debug("сопряжение с клиентом удачна")
    self.reader = reader
    self.writer = writer
    self.terminal_output.append(f'{self.writer.get_extra_info("peername")} подключился к серверу\n')
    try:
      while True:
        logging.debug("обрабатываем запросы клиента")
        self.data = await self.reader.read(100)
        if not self.data:
          logging.info("данные пустые, клиент возможно отключился")
          self.terminal_output.append('Клиент отключился, rest and peace')
          break
        self.message = self.data.decode().strip()
        logging.info(f"получено сообщение: {self.message}")
        print(f"{self.message}")
        await writer.drain()
    except Exception as e:
      self.terminal_output.append(f"если ты это видишь, видимо ты где-то облажался, rest and peace")
      self.terminal_output.insertHtml(f"<font color='red'>{e}</font><br>")
  
  #* Обработка команд
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
    self.terminal_output.append(f"<font color='lightBlue'>[username@kraken ~] $</font> {command}\n")

    # Обработка ОСОБЫХ команд
    if command == "/help":
        logging.info("Обработка команды /help")
        self.terminal_output.append('''
        /con_info                  Информация о подключении
        /connect                  Подключиться к клиенту
        /disconnect                  Отключиться от клиента
        ''')

    elif command == "/con_info":
        logging.info("Обработка команды /con_info")
        logging.debug("Проверяем статус подключения")
        logging.debug(f"Текущий статус подключения: {self.server_running}")
        if self.server_running:
            self.terminal_output.append("Статус подключения: <font color='green'>ПОДКЛЮЧЕН</font>")
        else:
            self.terminal_output.append("Статус подключения: <font color='red'>ОТКЛЮЧЕН</font>")

    elif command == "/connect":
        logging.info("Обработка команды /connect")
        logging.debug("Проверяем статус подключения")
        logging.debug(f"Текущий статус подключения: {self.server_running}")
        if not self.server_running:
            self.server_running = True
            self.terminal_output.append("<font color='green'>Сервер запущен на 127.0.0.1:65432</font>\n")
            logging.debug("Запускаем сервер")
            self.server = await asyncio.start_server(self.handle_client, '127.0.0.1', 65432)
        else:
            self.terminal_output.append("\n<font color='lightblue'>Сервер уже был запущен</font>\n")

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

    # Обработка НЕ ОСОБЫХ команд
    else:
        logging.info("Обработка обычной команды")
        if self.server_running:
            logging.debug("Сервер подключен, передаем команду клиенту")
            self.terminal_output.append(f"Введена команда: {command}\n")
            try:
                self.writer.write(command.encode())
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
    self.video_label.setAlignment(Qt.AlignCenter)

    logging.debug("Добавление метки в макет")
    self.content_layout.addWidget(self.video_label)

  #! Key Logger
  @asyncSlot()
  async def show_keylogger(self):
    """
    Отображает интерфейс для key logger-а.
    """
    logging.info("Отображение интерфейса для key logger-а")
    self.clear_content()

    logging.debug("Создание текстового поля для вывода данных key logger-а")
    self.text_display = QTextEdit()
    self.text_display.setReadOnly(True)

    logging.debug("Добавление текстового поля в макет")
    self.content_layout.addWidget(self.text_display)

  #! Информация
  @asyncSlot()
  async def show_info(self):
    """
    Отображает интерфейс для информации.
    """
    logging.info("Отображение интерфейса для информации")
    self.clear_content()

    logging.debug("Создание метки для отображения информации")
    self.info_label = QLabel()
    self.info_label.setAlignment(Qt.AlignLeft)

    info_text = f"""
    Вывод1 - [Переменная1]
    Вывод2 - [Переменная2]
    Вывод3 - [Переменная3]
    Вывод4 - [Переменная4]
    Вывод5 - [Переменная5]
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

  #* Отображение
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

    # Создаем контейнер для удаления строк
    self.delete_container = QWidget()
    self.delete_layout = QHBoxLayout(self.delete_container)

    # Создаем поле ввода для номера строки
    self.delete_input = QLineEdit()
    self.delete_input.setPlaceholderText("Номер строки")
    self.delete_input.setFixedWidth(100)  # Ограничиваем ширину поля ввода

    # Создаем кнопку "Удалить"
    self.delete_button = QPushButton("Удалить")
    self.delete_button.clicked.connect(self.delete_from_database)

    # Добавляем поле ввода и кнопку в layout
    self.delete_layout.addWidget(self.delete_input)
    self.delete_layout.addWidget(self.delete_button)
    self.delete_layout.addStretch()  # Добавляем растяжку, чтобы кнопка была слева

    # Создаем прокручиваемую область и таблицу
    self.scroll_area = QScrollArea()
    self.scroll_area.setWidgetResizable(True)

    self.table_widget = QTableWidget()
    self.scroll_area.setWidget(self.table_widget)

    # Добавляем контейнеры с полями ввода и таблицу в layout
    self.content_layout.addWidget(self.input_container)
    self.content_layout.addWidget(self.delete_container)
    self.content_layout.addWidget(self.scroll_area)

    # Обновляем таблицу данными из базы данных
    await self.update_table()

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

    # Проверяем, что все поля заполнены
    if not name or not ip or not port:
      print("Все поля должны быть заполнены")
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

  #* Удаление строки из базы данных
  @asyncSlot()
  async def delete_from_database(self):
    """
    Удаляет строку из базы данных по указанному номеру.
    """
    # Получаем номер строки из поля ввода
    row_number_text = self.delete_input.text().strip()
    if not row_number_text:
      print("Введите номер строки")
      return

    try:
      row_number = int(row_number_text)  # Преобразуем в число
      if row_number < 1:
        print("Номер строки должен быть больше 0")
        return

      # Получаем список ID из базы данных
      self.cursor.execute("SELECT id FROM connection_table")
      ids = [row[0] for row in self.cursor.fetchall()]

      # Проверяем, что номер строки корректен
      if 1 <= row_number <= len(ids):
        # Удаляем строку из базы данных
        self.cursor.execute("DELETE FROM connection_table WHERE id = ?", (ids[row_number - 1],))
        self.db_connection.commit()
        await self.update_table()  # Обновляем таблицу
        self.delete_input.clear()  # Очищаем поле ввода
      else:
        print("Номер строки вне диапазона")
    except ValueError:
      print("Ошибка: введите корректный номер строки")

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

  #! Очистка интерфейса
  def clear_content(self):
    """
    Очищает содержимое основного окна, удаляя все виджеты из content_layout.
    """
    for i in reversed(range(self.content_layout.count())):
      self.content_layout.itemAt(i).widget().setParent(None)


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





#! Класс Стартового окна
class StartWindow(MainWindow):
  def __init__(self):
    super().__init__()
    # Настройка основного окна
    self.setWindowTitle("KRAKEN - System control")
    # Иконка приложения
    icon_path = "img/imgReadme/kraken.jpg" 
    self.setWindowIcon(QIcon(icon_path))
    self.setGeometry(350, 100, 800, 600)  # x, y, width, height
    # Применяем стили
    self.setStyleSheet("""
      QWidget {
        background-color: #2E3440;  /* Темно-серый фон */
        color: #ECEFF4;  /* Белый текст */
      }
      QPushButton {
        background-color: #4C566A;  /* Серый фон кнопок */
        color: #ECEFF4;  /* Белый текст */
        border: 1px solid #81A1C1;  /* Голубая рамка */
        padding: 10px;
        border-radius: 5px;
        font-size: 16px;
      }
      QPushButton:hover {
        background-color: #81A1C1;  /* Голубой фон при наведении */
        color: #2E3440;  /* Темный текст */
      }
      QLabel {
        color: #ECEFF4;  /* Белый текст */
        font-size: 24px;
        font-weight: bold;
      }
      QLineEdit {
        background-color: #3B4252;  /* Темно-серый фон полей ввода */
        color: #ECEFF4;  /* Белый текст */
        border: 1px solid #81A1C1;  /* Голубая рамка */
        padding: 5px;
        border-radius: 3px;
      }
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
    # Логотип (замените путь на ваш логотип)
    self.logo_label = QLabel()
    self.logo_label.setPixmap(QPixmap("img/imgReadme/kraken.jpg").scaled(200, 200, Qt.KeepAspectRatio))
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

  @asyncSlot()
  async def select_path(self):
    """
    Открывает проводник для выбора пути.
    """
    path = QFileDialog.getExistingDirectory(self, "Выберите путь")
    if path:
      self.path_input.setText(path)


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


  #TODO: Функция Смены окон и открытия основного
  @asyncSlot()
  async def run_MainWindow(self):
    # Скрываем нынешнее окно
    self.hide()
    # Создаём и отображаем новое окно
    self.main_window = MainWindow()
    self.main_window.show()


  @asyncSlot()
  async def connect_to_db(self):
    """
    Проверяет наличие данных в БД и разрешает подключение, если данные есть.
    """
    # Подключение к базе данных SQLite
    try:
      conn = sqlite3.connect("sqlite.db")
      cursor = conn.cursor()
      # Проверка наличия данных в таблице (предположим, что таблица называется 'users')
      cursor.execute("SELECT COUNT(*) FROM connection_table")
      result = cursor.fetchone()
      if result and result[0] > 0:
        # Если данные есть, разрешаем подключение
        QMessageBox.information(self, "Успех", "Подключение успешно!")
        self.clear_interface()
        self.new_label = QLabel("Подключение успешно! Данные найдены.")
        self.new_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.new_label)
      else:
        # Если данных нет, выводим сообщение
        QMessageBox.information(self, "Нет данных", ":( У вас пока нету поклонников")
    except sqlite3.Error as e:
      QMessageBox.critical(self, "Ошибка", f"Ошибка при подключении к базе данных: {e}")
    finally:
      if conn:
        conn.close()

  def clear_interface(self):
    """
    Очищает текущий интерфейс, удаляя все виджеты.
    """
    for i in reversed(range(self.main_layout.count())):
      widget = self.main_layout.itemAt(i).widget()
      if widget:
        widget.setParent(None)


if __name__ == "__main__":
  #! просто для быстрых тестов( для разрабов) выбор нужного интерфейса
  cmd_quest = input("main or start\n> ")

  # Основной интерфейс
  if cmd_quest == "main":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_window = MainWindow()
    main_window.show()

    with loop:
      loop.run_forever()

  # Начальный интерфейс
  elif cmd_quest == "start":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    start_window = StartWindow()
    start_window.show()

    with loop:
      loop.run_forever()