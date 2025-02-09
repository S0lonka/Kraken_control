from PyQt5.QtWidgets import (QVBoxLayout, QPushButton, QTextEdit, QCheckBox, QDialog, QApplication)
import sys
# Импорт текста соглашения
from licenseTxt import license_agreement

#! Лицензионное соглашение
class LicenseAgreementDialog(QDialog):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.setWindowTitle('Лицензионное соглашение')
    self.setGeometry(100, 100, 600, 400)

    layout = QVBoxLayout()

    self.text_edit = QTextEdit(self)
    # Тест нашего соглашения
    self.text_edit.setPlainText(license_agreement)
    # Можно только читать
    self.text_edit.setReadOnly(True)
    layout.addWidget(self.text_edit)

    self.checkbox = QCheckBox("Я соглашаюсь с условиями лицензионного соглашения", self)
    self.checkbox.stateChanged.connect(self.on_checkbox_changed)
    layout.addWidget(self.checkbox)

    self.next_button = QPushButton("Далее", self)
    self.next_button.setEnabled(False)
    self.next_button.clicked.connect(self.accept)  # Закрываем диалог с результатом Accepted
    layout.addWidget(self.next_button)

    self.setLayout(layout)

  def on_checkbox_changed(self, state):
    if state == 2:  # 2 означает, что галочка поставлена
      self.next_button.setEnabled(True)
    else:
      self.next_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создаем экземпляр приложения
    license_window = LicenseAgreementDialog()  # Создаем экземпляр диалогового окна

    if license_window.exec_() == QDialog.Accepted:  # Показываем диалог и проверяем результат
        print("Пользователь согласился с условиями")
    else:
        print("Пользователь не согласился с условиями")
    sys.exit(app.exec_())  # Запускаем главный цикл приложения