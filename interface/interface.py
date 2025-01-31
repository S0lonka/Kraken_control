import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QLabel, QScrollArea, QTableWidget, 
                             QTableWidgetItem, QLineEdit)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    # Настройка основного окна
    self.setWindowTitle("PyQt5 Multi-Interface App")
    self.setGeometry(100, 100, 800, 600)

    # Создаем контейнер для кнопок и основного окна
    self.main_widget = QWidget()
    self.setCentralWidget(self.main_widget)

    # Основной layout
    self.main_layout = QVBoxLayout(self.main_widget)

    # Создаем верхнюю панель с кнопками
    self.top_buttons_layout = QHBoxLayout()
    self.main_layout.addLayout(self.top_buttons_layout)

    # Создаем кнопки
    self.button1 = QPushButton("Терминал")
    self.button2 = QPushButton("Видео")
    self.button3 = QPushButton("Текст")
    self.button4 = QPushButton("Информация")
    self.button5 = QPushButton("База данных")

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
    self.button3.clicked.connect(self.show_text)
    self.button4.clicked.connect(self.show_info)
    self.button5.clicked.connect(self.show_database)

    # Инициализируем начальный интерфейс
    self.show_terminal()

    # Подключение к базе данных SQLite
    self.db_connection = sqlite3.connect("example.db")  # Укажите путь к вашей базе данных
    self.cursor = self.db_connection.cursor()

    # Создаем тестовую таблицу, если её нет
    self.create_test_table()

  def create_test_table(self):
    """
    Создает тестовую таблицу в базе данных, если она не существует.
    """
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS test_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        ip TEXT,
        port TEXT
      )
    """)
    self.db_connection.commit()

  def clear_content(self):
    """
    Очищает содержимое основного окна, удаляя все виджеты из content_layout.
    """
    for i in reversed(range(self.content_layout.count())):
      self.content_layout.itemAt(i).widget().setParent(None)

  def show_terminal(self):
    """
    Отображает интерфейс терминала.
    """
    self.clear_content()

    self.terminal_input = QLineEdit()
    self.terminal_output = QTextEdit()
    self.terminal_output.setReadOnly(True)

    self.content_layout.addWidget(self.terminal_input)
    self.content_layout.addWidget(self.terminal_output)

    self.terminal_input.returnPressed.connect(self.execute_command)

  def execute_command(self):
    """
    Обрабатывает ввод команды в терминале.
    """
    command = self.terminal_input.text()
    result = f"Выполнена команда: {command}"  # Заглушка для результата
    self.terminal_output.append(result)
    self.terminal_input.clear()

  def show_video(self):
    """
    Отображает интерфейс для видео.
    """
    self.clear_content()

    self.video_label = QLabel("Здесь будет видео")
    self.video_label.setAlignment(Qt.AlignCenter)

    self.content_layout.addWidget(self.video_label)

  def show_text(self):
    """
    Отображает интерфейс для текста.
    """
    self.clear_content()

    self.text_display = QTextEdit()
    self.text_display.setReadOnly(True)

    self.content_layout.addWidget(self.text_display)

  def show_info(self):
    """
    Отображает интерфейс для информации.
    """
    self.clear_content()

    self.info_label = QLabel()
    self.info_label.setAlignment(Qt.AlignLeft)

    info_text = """
    Вывод1 - [Переменная1]
    Вывод2 - [Переменная2]
    Вывод3 - [Переменная3]
    Вывод4 - [Переменная4]
    Вывод5 - [Переменная5]
    """
    self.info_label.setText(info_text)

    self.content_layout.addWidget(self.info_label)

  def show_database(self):
    """
    Отображает интерфейс для базы данных.
    Заполняет таблицу данными из SQLite.
    """
    self.clear_content()

    # Создаем строку ввода для добавления данных
    self.db_input = QLineEdit()
    self.db_input.setPlaceholderText('Введите данные в формате: name="Maks" ip="245.35.0.8" port="44267"')
    self.db_input.returnPressed.connect(self.add_to_database)

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

  def update_table(self):
    """
    Обновляет таблицу данными из базы данных.
    """
    # Получаем данные из базы данных
    self.cursor.execute("SELECT * FROM test_table")
    data = self.cursor.fetchall()

    # Устанавливаем количество строк и столбцов в таблице
    self.table_widget.setRowCount(len(data))
    self.table_widget.setColumnCount(4)
    self.table_widget.setHorizontalHeaderLabels(["ID", "Name", "IP", "Port"])

    # Заполняем таблицу данными
    for row_index, row_data in enumerate(data):
      for col_index, col_data in enumerate(row_data):
        self.table_widget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

  def add_to_database(self):
    """
    Добавляет данные в базу данных на основе введенной строки.
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

    # Вставляем данные в базу данных
    if data:
      self.cursor.execute("""
        INSERT INTO test_table (name, ip, port)
        VALUES (:name, :ip, :port)
      """, data)
      self.db_connection.commit()

      # Обновляем таблицу
      self.update_table()

  def closeEvent(self, event):
    """
    Закрывает соединение с базой данных при закрытии приложения.
    """
    self.db_connection.close()
    event.accept()

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())