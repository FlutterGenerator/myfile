import zipfile
import re
import os
import sys
import tempfile

# Определение цветовых кодов для консольного вывода
bred = '\033[1;31m'
bgreen = '\033[1;32m'
byellow = '\033[1;33m'
bblue = '\033[1;34m'
bpurple = '\033[1;35m'
bcyan = '\033[1;36m'
bwhite = '\033[1;37m'
end = '\033[0m'

# Создание баннера с информацией о версии
banner = f"""{byellow}
   _____          _   _       _____ _   _ _____ 
  / ____|   /\   | \ | |     / ____| \ | |  __ \
 | |  __   /  \  |  \| |    | |  __|  \| | |  | |
 | | |_ | / /\ \ | . ` |    | | |_ | . ` | |  | |
 | |__| |/ ____ \| |\  |    | |__| | |\  | |__| |
  \____/_/    \_\_| \_|     \_____|_| \_|_____/
{end}
"""

# Функция для печати баннера
def print_banner():
    os.system('clear')
    print(banner)
    print(f"{bwhite}Version: 6.0{end}")
    print(f"{bwhite}Created by {bred}@toyly_s {bwhite}& {bred}@RK_TECHNO_INDIA{end}")
    print(f"{bblue}Telegram Channel: https://t.me/apkinsight{end}\n")

# Функция для создания файла Utils.smali
def create_Utils(extract_folder):
    sf_path = os.path.join(extract_folder, 'Utils.smali')
    with open(sf_path, 'w') as special_file:
        special_file.write(
            ".class public LdexGun/Utils;\n"
            ".super Ljava/lang/Object;\n\n"
            ".method public static getV()I\n"
            "    .locals 1\n"
            "    const/4 v0, 0x1\n"  # Возвращает 1 (или любое другое значение)
            "    return v0\n"
            ".end method\n"
        )
    return sf_path

# Функция для модификации содержимого файлов Smali
def modify_file_content(file_path, rel_path):
    with open(file_path, 'r') as f:
        original_content = f.read()

    modified_content = original_content
    created_Utils = False

    # Примеры модификации, добавьте свои регулярные выражения здесь
    # Замена методов, чтобы обойти проверки
    modified_content = re.sub(r'(\.method (.+?)\s*{)', r'\1\n    invoke-static {p0}, LdexGun/Utils;->getV()I\n', modified_content)
    
    # Создание Utils.smali, если он ещё не создан
    if not created_Utils:
        create_Utils(os.path.dirname(file_path))
        created_Utils = True

    # Запись модифицированного содержимого обратно в файл
    with open(file_path, 'w') as f:
        f.write(modified_content)

# Основная функция
def main(apk_path):
    # Создание временной папки для извлечения APK
    with tempfile.TemporaryDirectory() as extract_folder:
        # Извлечение APK
        with zipfile.ZipFile(apk_path, 'r') as apk:
            apk.extractall(extract_folder)

        # Обход всех файлов в извлеченной папке
        for root, dirs, files in os.walk(extract_folder):
            for file in files:
                if file.endswith('.smali'):
                    file_path = os.path.join(root, file)
                    modify_file_content(file_path, file)

        # Создание нового APK из модифицированных файлов
        modified_apk_path = os.path.splitext(apk_path)[0] + '_modified.apk'
        with zipfile.ZipFile(modified_apk_path, 'w') as modified_apk:
            for root, dirs, files in os.walk(extract_folder):
                for file in files:
                    modified_apk.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), extract_folder))
    
    print(f"Modified APK created: {modified_apk_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{bred}Usage: python script.py <path_to_apk>{end}")
        sys.exit(1)

    print_banner()
    main(sys.argv[1])