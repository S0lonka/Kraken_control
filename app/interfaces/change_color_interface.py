import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from .utils.style.style_variables_base import base_colors  # Импортируем общий словарь
from .utils.style.style_variables_editable import editable_colors

class ColorChangerApp(QWidget):
  def __init__(self, parent=None):
    super().__init__()
    self.parent = parent
    self.initUI()

  def initUI(self):
    self.setWindowTitle('KRAKEN - Color Changer')
    self.setGeometry(100, 100, 400, 600)
    self.setWindowIcon(QIcon("app/interfaces/utils/resource/kraken.jpg"))

    self.setStyleSheet(f"""
      QWidget {{
        background-color: #{base_colors["QWidget_bc"]};  /* Темно-серый фон */
        color: #{base_colors["text_color"]};  /* Белый текст */
      }}
      QPushButton {{
        background-color: #{base_colors["button_bc"]};  /* Серый фон кнопок */
        color: #{base_colors["text_color"]};  /* Белый текст */
        border: 1px solid #{base_colors["border_color"]};  /* Голубая рамка */
        padding: 5px;
        border-radius: 3px;
      }}
      QPushButton:hover {{
        background-color: #{base_colors["border_color"]};  /* Голубой фон при наведении */
        color: #{base_colors["button_color_hover"]};  /* Темный текст */
      }}
      QLineEdit, QTextEdit {{
        background-color: #{base_colors["input_area"]};  /* Темно-серый фон полей ввода */
        color: #{base_colors["text_color"]};  /* Белый текст */
        border: 1px solid #{base_colors["border_color"]};  /* Голубая рамка */
        padding: 5px;
        border-radius: 3px;
      }}
      QTableWidget {{
        background-color: #{base_colors["input_area"]};  /* Темно-серый фон таблицы */
        color: #{base_colors["text_color"]};  /* Белый текст */
        gridline-color: #{base_colors["border_color"]};  /* Голубые линии сетки */
      }}
      QHeaderView::section {{
        background-color: #{base_colors["button_bc"]};  /* Серый фон заголовков таблицы */
        color: #{base_colors["text_color"]};  /* Белый текст */
        padding: 5px;
        border: 1px solid #{base_colors["border_color"]};  /* Голубая рамка */
      }}
      QScrollArea {{
        background-color: #{base_colors["button_color_hover"]};  /* Темно-серый фон */
        border: none;
      }}
      QLabel {{
        color: #{base_colors["text_color"]};  /* Белый текст */
      }}
    """)

    layout = QVBoxLayout()

    # Создаем ползунки, квадратики и поля ввода для каждой переменной
    for color_name, default_color in editable_colors.items():
      hbox = QHBoxLayout()

      # Название цвета (переводим в читаемый формат)
      readable_name = self.get_readable_name(color_name)
      label = QLabel(readable_name)
      hbox.addWidget(label)

      # Ползунок
      slider = QSlider(Qt.Horizontal)
      slider.setMinimum(0)
      slider.setMaximum(16777215)  # Диапазон HEX (000000 до FFFFFF)
      slider.setValue(int(default_color, 16))  # Начальное значение
      slider.valueChanged.connect(lambda value, name=color_name: self.update_color_input(name, value))
      hbox.addWidget(slider)

      # Квадратик для отображения цвета
      color_box = QLabel()
      color_box.setFixedSize(20, 20)
      color_box.setStyleSheet(f"background-color: #{default_color};")
      hbox.addWidget(color_box)

      # Поле ввода для HEX-кода
      input_field = QLineEdit(default_color)
      input_field.setMaxLength(6)
      input_field.textChanged.connect(lambda text, name=color_name: self.validate_color_input(name, text))
      hbox.addWidget(input_field)

      # Сохраняем ползунок, квадратик и поле ввода
      setattr(self, f"{color_name}_slider", slider)
      setattr(self, f"{color_name}_color_box", color_box)
      setattr(self, f"{color_name}_input", input_field)

      layout.addLayout(hbox)

    # Кнопки
    apply_button = QPushButton('Применить')
    apply_button.clicked.connect(self.apply_styles)
    layout.addWidget(apply_button)

    reset_button = QPushButton('Сбросить')
    reset_button.clicked.connect(self.reset_colors)
    layout.addWidget(reset_button)

    self.setLayout(layout)

  def get_readable_name(self, color_name):
    # Преобразуем имена переменных в читаемые названия
    name_map = {
      "QWidget_bc": "Фон окна",
      "text_color": "Цвет текста",
      "button_bc": "Фон кнопок",
      "border_color": "Цвет рамки",
      "button_color_hover": "Кнопка (наведение)",
      "input_area": "Поле ввода"
    }
    return name_map.get(color_name, color_name)

  def update_color_input(self, color_name, value):
    # Преобразуем значение ползунка в HEX-код
    hex_color = f"{value:06X}"
    getattr(self, f"{color_name}_input").setText(hex_color)
    self.update_color_box(color_name, hex_color)
    self.update_slider_style(color_name)

  def validate_color_input(self, color_name, text):
    if len(text) == 6 and all(c in "0123456789ABCDEFabcdef" for c in text):
      # Преобразуем HEX-код в значение ползунка
      value = int(text, 16)
      getattr(self, f"{color_name}_slider").setValue(value)
      self.update_color_box(color_name, text)
      self.update_slider_style(color_name)

  def update_color_box(self, color_name, hex_color):
    # Обновляем цвет квадратика
    color_box = getattr(self, f"{color_name}_color_box")
    color_box.setStyleSheet(f"background-color: #{hex_color};")

  def update_slider_style(self, color_name):
    # Обновляем цвет ручки ползунка
    hex_color = getattr(self, f"{color_name}_input").text()
    if len(hex_color) == 6 and all(c in "0123456789ABCDEFabcdef" for c in hex_color):
      slider = getattr(self, f"{color_name}_slider")
      slider.setStyleSheet(f"""
        QSlider::handle:horizontal {{
          background: #{hex_color};
          width: 20px;
          height: 20px;
          margin: -5px 0;
          border-radius: 10px;
        }}
      """)

  def apply_styles(self):
    # Обновляем значения в editable_colors
    for color_name in editable_colors.keys():
      hex_color = getattr(self, f"{color_name}_input").text()
      if len(hex_color) == 6 and all(c in "0123456789ABCDEFabcdef" for c in hex_color):
        editable_colors[color_name] = hex_color

    # Сохраняем изменения в файл style_variables.py
    self.save_editable_colors_to_file()

  def save_editable_colors_to_file(self):
    # Формируем содержимое для записи в файл
    file_content = f"""
# Изменяемые стили (изначально копия базовых)
editable_colors = {editable_colors}
"""

    # Записываем в файл
    with open("app/interfaces/utils/style/style_variables_editable.py", "w", encoding="utf-8") as file:
      file.write(file_content)
    
    # Обновляем стили в родительском окне
    if self.parent:  # Проверяем, есть ли родительское окно
      self.parent.update_styles()  # Вызываем метод обновления стилей

  def reset_colors(self):
    # Сбрасываем цвета на базовые значения
    for color_name, default_color in base_colors.items():
      # Обновляем ползунок, поле ввода и квадратик
      getattr(self, f"{color_name}_slider").setValue(int(default_color, 16))
      getattr(self, f"{color_name}_input").setText(default_color)
      self.update_color_box(color_name, default_color)
      self.update_slider_style(color_name)

      # Восстанавливаем базовые значения в editable_colors
      editable_colors[color_name] = default_color

    # Сохраняем изменения в файл style_variables.py
    self.save_editable_colors_to_file()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = ColorChangerApp()
  ex.show()
  sys.exit(app.exec_())