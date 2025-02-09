import asyncio
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QTextCursor, QFont
from qasync import asyncSlot

#! Терминал внутри ОКНА С ТЕРМИНАЛОМ
class Terminal(QTextEdit):
  def __init__(self):
    super().__init__()
    self.setFont(QFont("Courier", 10))
    self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.setLineWrapMode(QTextEdit.NoWrap)
    self.setReadOnly(False)
    self.setText("> ")
    self.cursor = self.textCursor()
    self.cursor.movePosition(QTextCursor.End)
    self.setTextCursor(self.cursor)

  def keyPressEvent(self, event):
    if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
      self.process_command()
    else:
      super().keyPressEvent(event)

  @asyncSlot()
  async def process_command(self):
    cursor = self.textCursor()
    cursor.movePosition(QTextCursor.End)
    cursor.select(QTextCursor.LineUnderCursor)
    command = cursor.selectedText()[2:]  # Убираем "> " из команды
    cursor.movePosition(QTextCursor.End)
    cursor.insertText("\n")

    if command == "/help":
      self.append("Available commands:\n/help - Show this help message")
    else:
      # Пример асинхронной операции
      await asyncio.sleep(1)  # Имитация долгой операции
      self.append(f"Unknown command: {command}")

    self.append("> ")
    cursor.movePosition(QTextCursor.End)
    self.setTextCursor(cursor)







#! ОКНО С АДМИН ТЕРМИНАЛОМ
class TerminalWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.setWindowIcon(QIcon("resources/img/imgReadme/kraken.jpg"))
    self.setWindowTitle("KRAKEN - ADMIN TERMINAL")
    self.setGeometry(100, 100, 800, 600)

    # Устанавливаем стили для всего окна и его элементов
    self.setStyleSheet("""
      QWidget {
        background-color: #2E3440;  /* Темно-серый фон */
        color: #ECEFF4;  /* Белый текст */
      }
      QTextEdit {
        background-color: #3B4252;  /* Более светлый фон для текстового поля */
        color: #ECEFF4;  /* Белый текст */
        border: 1px solid #4C566A;  /* Граница */
        padding: 5px;
      }
      QScrollBar:vertical {
        background-color: #3B4252;  /* Фон скроллбара */
        width: 12px;
        margin: 0px;
      }
      QScrollBar::handle:vertical {
        background-color: #4C566A;  /* Цвет ползунка */
        min-height: 20px;
        border-radius: 6px;
      }
      QScrollBar::add-line:vertical,
      QScrollBar::sub-line:vertical {
        background: none;
      }
      QScrollBar::add-page:vertical,
      QScrollBar::sub-page:vertical {
        background: none;
      }
    """)

    layout = QVBoxLayout()
    self.terminal = Terminal()
    layout.addWidget(self.terminal)
    self.setLayout(layout)