import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QLabel, QScrollArea, QTableWidget, 
                             QTableWidgetItem, QLineEdit)
from PyQt5.QtCore import Qt
import main.server as server

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    #! Основные настройки
    # Настройка основного окна
    self.setWindowTitle("KRAKEN - System control")
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

  #! Терминал
  def show_terminal(self):
    """
    Отображает интерфейс терминала.
    """
    self.clear_content()

    self.terminal_input = QLineEdit()
    self.terminal_input.setPlaceholderText('Введите команду для терминала')
    self.terminal_output = QTextEdit()
    self.terminal_output.setReadOnly(True)

    self.content_layout.addWidget(self.terminal_input)
    self.content_layout.addWidget(self.terminal_output)

    self.terminal_input.returnPressed.connect(self.execute_command)

  #* Обработка команд
  def execute_command(self):
    """
    Обрабатывает ввод команды в терминале.
    """
    command = self.terminal_input.text()
    self.terminal_input.clear()

    if command == "connect":
      if not self.server_running:
        self.server_running = True
        self.terminal_output.append("Сервер запущен на 127.0.0.1:65432\n")

    elif command == "disconnect":
      if self.server_running:
        self.server_running = False
        self.terminal_output.append("Сервер остановлен\n")
        # Здесь можно добавить код для остановки сервера
      else:
        self.terminal_output.append("Сервер не был запущен\n")

    else:
      if self.server_running:
        # Отправляем команду на сервер и получаем ответ
        response = server.start_server("127.0.0.1", 65432, command)
        self.terminal_output.append(f"Команда: {command}\nОтвет: {response}\n")
      else:
        self.terminal_output.append("Сервер не запущен. Введите 'connect' для запуска.\n")




  #! Видео
  def show_video(self):
    """
    Отображает интерфейс для видео.
    """
    self.clear_content()

    self.video_label = QLabel("Здесь будет видео")
    self.video_label.setAlignment(Qt.AlignCenter)

    self.content_layout.addWidget(self.video_label)

  #! Key Logger
  def show_keylogger(self):
    """
    Отображает интерфейс для key logger-а.
    """
    self.clear_content()

    self.text_display = QTextEdit()
    self.text_display.setReadOnly(True)

    self.content_layout.addWidget(self.text_display)

  #! Информация
  def show_info(self):
    """
    Отображает интерфейс для информации.
    """
    self.clear_content()

    self.info_label = QLabel()
    self.info_label.setAlignment(Qt.AlignLeft)

    info_text = f"""
    Вывод1 - [Переменная1]
    Вывод2 - [Переменная2]
    Вывод3 - [Переменная3]
    Вывод4 - [Переменная4]
    Вывод5 - [Переменная5]
    """
    self.info_label.setText(info_text)

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

  def show_database(self):
    """
    Отображает интерфейс для базы данных.
    Заполняет таблицу данными из SQLite.
    """
    self.clear_content()

    # Создаем контейнер для полей ввода и кнопки
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
    self.scroll_area.setWidget(self.table_widget)

    # Добавляем контейнер с полями ввода и таблицу в layout
    self.content_layout.addWidget(self.input_container)
    self.content_layout.addWidget(self.scroll_area)

    # Обновляем таблицу данными из базы данных
    self.update_table()

  #* Добавление данных в базу данных
  def add_to_database(self):
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
    self.update_table()

  #* Обновление таблицы
  def update_table(self):
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

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())