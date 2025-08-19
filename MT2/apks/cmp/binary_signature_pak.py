import sys
import os

def check_binary_signature(file_path):
    try:
        if not os.path.isfile(file_path):
            print(f"Указанный путь '{file_path}' не является файлом.")
            return

        with open(file_path, 'rb') as f:
            signature = f.read(4)  # Читаем первые 4 байта файла
            if len(signature) < 4:
                print("Файл слишком мал для получения сигнатуры.")
                return
            
            # Преобразуем байты в формат \\xXX
            hex_signature = ''.join(f'\\x{byte:02x}' for byte in signature)
            print("Бинарная сигнатура файла:", hex_signature)  # Выводим сигнатуру

            # Выводим дополнительные данные
            file_size = os.path.getsize(file_path)
            print(f"Размер файла: {file_size} байт")

    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден. Проверьте правильность пути.")
    except IsADirectoryError:
        print(f"Указанный путь '{file_path}' является директорией, а не файлом.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    # Проверяем, передан ли аргумент командной строки
    if len(sys.argv) < 2:
        print("Пожалуйста, укажите путь к файлу .pak")
        sys.exit(1)

    # Получаем путь к файлу из аргументов командной строки
    file_path = sys.argv[1]
    check_binary_signature(file_path)