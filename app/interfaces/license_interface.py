from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QTextEdit, QCheckBox, QDialog, QLabel
# Импорт текста соглашения
from interfaces.utils import license_agreement

#! Лицензионное соглашение
class LicenseAgreementDialog(QDialog):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.setWindowTitle('Лицензионное соглашение')
    self.setGeometry(100, 100, 450, 250)

    layout = QVBoxLayout()

    # Добавляем текст сверху
    self.label = QLabel(
      "Пожалуйста, ознакомьтесь с лицензионным соглашением перед продолжением:\n"
      "Это важно для понимания ваших прав и обязанностей.\n"
      "Лицензионное соглашение регулирует использование данного программного обеспечения.\n"
      "Перед установкой или использованием программы убедитесь, что вы согласны с условиями.\n"
      "Если вы не согласны с условиями, пожалуйста, закройте это окно и не используйте программу.\n"
      "Спасибо за ваше внимание и понимание.", self)
    layout.addWidget(self.label)

    self.text_edit = QTextEdit(self)
    # Тест нашего соглашения
    self.text_edit.setHtml(license_agreement)
    # Можно только читать
    self.text_edit.setReadOnly(True)
    self.text_edit.setMaximumHeight(200)  # Уменьшаем высоту окна с соглашением
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
