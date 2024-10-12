import os
import glob

def embed_exe_in_jpeg(jpeg_path, exe_path, output_path):
    # Чтение JPEG файла
    try:
        with open(jpeg_path, 'rb') as jpeg_file:
            jpeg_data = jpeg_file.read()
        print(f"JPEG file read: {len(jpeg_data)} bytes")
    except FileNotFoundError:
        print(f"Error: JPEG file {jpeg_path} not found.")
        return
    except Exception as e:
        print(f"Error reading JPEG file: {e}")
        return

    # Поиск маркера окончания файла JPEG
    end_marker = b'\xff\xd9'
    try:
        jpeg_end = jpeg_data.index(end_marker) + len(end_marker)
        print(f"Found JPEG end marker at byte position: {jpeg_end}")
    except ValueError:
        print("Error: JPEG end marker not found")
        return

    # Чтение файла EXE
    try:
        with open(exe_path, 'rb') as exe_file:
            exe_data = exe_file.read()
        print(f"EXE file read: {len(exe_data)} bytes")
    except FileNotFoundError:
        print(f"Error: EXE file {exe_path} not found.")
        return
    except Exception as e:
        print(f"Error reading EXE file: {e}")
        return

    # Объединение данных JPEG и EXE
    combined_data = jpeg_data[:jpeg_end] + exe_data

    # Запись объединенных данных в выходной файл
    try:
        with open(output_path, 'wb') as output_file:
            output_file.write(combined_data)
        print(f"EXE has been successfully embedded in {output_path}")
    except Exception as e:
        print(f"Error writing to output file: {e}")

# Пример использования
script_dir = os.path.dirname(os.path.abspath(__file__))

# Поиск первого файла с расширением .jpg в директории скрипта
jpg_files = glob.glob(os.path.join(script_dir, "*.jpg"))

# Поиск первого файла с расширением .exe в директории скрипта
exe_files = glob.glob(os.path.join(script_dir, "*.exe"))

# Папка для вывода
output_dir = os.path.join(script_dir, "OutputDate")

# Проверка наличия папки OutputDate, создание если её нет
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Если найден и JPEG, и EXE файлы, то продолжаем
if jpg_files and exe_files:
    jpeg_path = jpg_files[0]
    exe_path = exe_files[0]
    
    # Получение имени файла без расширения и создание пути к выходному файлу
    jpeg_name = os.path.basename(jpeg_path)
    output_path = os.path.join(output_dir, jpeg_name)  # Выходной файл с тем же именем

    print(f"Found JPEG file: {jpeg_path}")
    print(f"Found EXE file: {exe_path}")
    embed_exe_in_jpeg(jpeg_path, exe_path, output_path)
else:
    print("No JPEG or EXE files found in the current directory.")
