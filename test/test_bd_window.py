from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QMenu, QMessageBox
)
from PyQt6.QtCore import Qt

class MyTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def contextMenuEvent(self, event):
        # Получаем позицию клика
        row = self.rowAt(event.pos().y())
        col = self.columnAt(event.pos().x())

        # Показываем меню только для первого столбца
        if col == 0 and row >= 0:
            # Создаем контекстное меню
            menu = QMenu(self)

            # Добавляем действие "Сказать привет"
            say_hello_action = menu.addAction("Сказать привет")
            say_hello_action.triggered.connect(lambda: self.say_hello(row))

            # Показываем меню
            menu.exec(event.globalPos())

    def say_hello(self, row):
        # Получаем имя из первой колонки
        name = self.item(row, 0).text()
        QMessageBox.information(self, "Привет", f"Привет, {name}!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создаем таблицу
        self.table = MyTableWidget(self)
        self.table.setRowCount(2)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "IP", "Port"])

        # Заполняем таблицу данными
        self.table.setItem(0, 0, QTableWidgetItem("Алиса"))
        self.table.setItem(0, 1, QTableWidgetItem("192.168.1.1"))
        self.table.setItem(0, 2, QTableWidgetItem("8080"))

        self.table.setItem(1, 0, QTableWidgetItem("Макс"))
        self.table.setItem(1, 1, QTableWidgetItem("192.168.1.2"))
        self.table.setItem(1, 2, QTableWidgetItem("8081"))

        # Устанавливаем таблицу как центральный виджет
        self.setCentralWidget(self.table)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()