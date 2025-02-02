import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, 
                             QPushButton, QHBoxLayout, QMessageBox, QLineEdit, QFileDialog)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
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

  def change_interface(self):
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


  def create_interface(self):
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

  def select_path(self):
    """
    Открывает проводник для выбора пути.
    """
    path = QFileDialog.getExistingDirectory(self, "Выберите путь")
    if path:
      self.path_input.setText(path)

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

  def create_database(self):
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

    try:
      conn = sqlite3.connect("sqlite.db")
      cursor = conn.cursor()
      # Создаем таблицу connection_table
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS connection_table (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT,
          ip TEXT,
          port TEXT
        )
      """)
      conn.commit()
      QMessageBox.information(self, "Успех", "Таблица успешно создана!")
    except sqlite3.Error as e:
      QMessageBox.critical(self, "Ошибка", f"Ошибка при создании таблицы: {e}")
    finally:
      if conn:
        conn.close()

  def connect_to_db(self):
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

  def clear_layout(self):
    """
    Очищает текущий layout, удаляя все виджеты.
    """
    for i in reversed(range(self.main_layout.count())):
      widget = self.main_layout.itemAt(i).widget()
      if widget:
        widget.setParent(None)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())