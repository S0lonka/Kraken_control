import os
import shutil

# Пути к файлам
config_file = 'app/interfaces/utils/style/style_variables_editable.py'
template_file = 'app/interfaces/utils/style/style_variables_editable.template.py'

# Проверяем, существует ли config.py
if not os.path.exists(config_file):
  shutil.copy(template_file, config_file)
  print("Файл создан")