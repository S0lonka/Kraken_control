import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QLabel, QScrollArea, QTableWidget, 
                             QTableWidgetItem, QLineEdit)
from PyQt5.QtCore import Qt

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
    result = f"Выполнена команда: {command}"  # Заглушка для результата
    self.terminal_output.append(result)
    self.terminal_input.clear()

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

  #* Отображение
  def show_database(self):
    """
    Отображает интерфейс для базы данных.
    Заполняет таблицу данными из SQLite.
    """
    self.clear_content()

    # Создаем строку ввода для добавления данных
    self.db_input = QLineEdit()
    self.db_input.setPlaceholderText('Введите данные в формате: name="John" ip="245.35.0.8" port="44267" или delete="1"')
    self.db_input.returnPressed.connect(self.process_db_input)

    # Создаем прокручиваемую область и таблицу
    self.scroll_area = QScrollArea()
    self.scroll_area.setWidgetResizable(True)

    self.table_widget = QTableWidget()
    self.scroll_area.setWidget(self.table_widget)

    # Добавляем строку ввода и таблицу в layout
    self.content_layout.addWidget(self.db_input)
    self.content_layout.addWidget(self.scroll_area)

    # Обновляем таблицу данными из базы данных
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

  #* Обработка ввода
  def process_db_input(self):
    """
    Обрабатывает ввод в строке базы данных.
    """
    input_text = self.db_input.text()
    self.db_input.clear()

    # Разбираем введенные данные
    data = {}
    for part in input_text.split():
      if "=" in part:
        key, value = part.split("=")
        key = key.strip()
        value = value.strip('"')
        data[key] = value

    # Если введена команда на удаление
    if "delete" in data:
      try:
        row_number = int(data["delete"])  # Номер строки, введенный пользователем
        if row_number < 1:
          print("Номер строки должен быть больше 0")
          return

        # Получаем данные из таблицы
        self.cursor.execute("SELECT id FROM connection_table")
        ids = [row[0] for row in self.cursor.fetchall()]

        # Проверяем, что номер строки корректен
        if 1 <= row_number <= len(ids):
          # Удаляем строку из базы данных
          self.cursor.execute("DELETE FROM connection_table WHERE id = ?", (ids[row_number - 1],))
          self.db_connection.commit()
          self.update_table()
        else:
          print("Номер строки вне диапазона")
      except ValueError:
        print("Ошибка в удалении: некорректный ввод")

    # Если введены данные для добавления
    elif all(key in data for key in ["name", "ip", "port"]):
      self.cursor.execute("""
        INSERT INTO connection_table (name, ip, port)
        VALUES (:name, :ip, :port)
      """, data)
      self.db_connection.commit()
      self.update_table()

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