import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, 
                             QPushButton, QHBoxLayout, QMessageBox)
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
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.create_button)
        self.button_layout.addWidget(self.connect_button)
        self.main_layout.addLayout(self.button_layout)

    def create_interface(self):
        """
        Создает пустой интерфейс после нажатия кнопки "Создать".
        """
        self.clear_interface()
        self.new_label = QLabel("Пустой интерфейс")
        self.new_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.new_label)

    def connect_to_db(self):
        """
        Проверяет наличие данных в БД и выводит сообщение.
        """
        # Симуляция проверки данных в БД
        data_exists = self.check_db_data()

        if data_exists:
            self.clear_interface()
            self.new_label = QLabel("Данные найдены, интерфейс будет обновлен")
            self.new_label.setAlignment(Qt.AlignCenter)
            self.main_layout.addWidget(self.new_label)
        else:
            QMessageBox.information(self, "Нет данных", ":( У вас пока нету поклонников")

    def check_db_data(self):
        """
        Симуляция проверки данных в БД.
        В реальном приложении здесь будет запрос к БД.
        """
        # Возвращаем False для симуляции отсутствия данных
        return False

    def clear_interface(self):
        """
        Очищает текущий интерфейс, удаляя все виджеты.
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