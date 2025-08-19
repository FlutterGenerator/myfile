#!/bin/bash

# Проверка, установлен ли radare2
if ! command -v r2 &> /dev/null; then
    echo "Установка radare2"
    pkg install -y radare2 &> /dev/null
fi

echo
echo ' █████╗ ███╗   ██╗████████╗██╗██╗  ██╗'
echo '██╔══██╗████╗  ██║╚══██╔══╝██║██║ ██╔╝'
echo '███████║██╔██╗ ██║   ██║   ██║█████╔╝ '
echo '██╔══██║██║╚██╗██║   ██║   ██║██╔═██╗ '
echo '██║  ██║██║ ╚████║   ██║   ██║██║  ██╗'
echo '╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═╝'
echo ' Dont Remove Copyright ©Antik'
echo

# Ввод директории
read -p "〄 ВВЕДИТЕ ЦЕЛЕВУЮ ДИРЕКТОРИЮ --> " target_directory
echo "Введенная целевая директория: $target_directory"
echo

# Переход в целевую директорию
cd "$target_directory" || { echo "Не удалось изменить директорию"; exit 1; }

# Ввод имени библиотеки
read -p "〄 ВАШЕ ИМЯ БИБЛИОТЕКИ -->> " libname
echo "Введенное имя библиотеки: $libname"
echo

# Проверка существования библиотеки
if [[ ! -f "$libname" ]]; then
    echo "Ошибка: библиотека '$libname' не найдена в директории '$target_directory'."
    exit 1
fi

# Дамп
echo "Дампим..!!"
r2 -w "$libname" << EOF &> /dev/null
iE > Dump.cs
q
EOF

echo
echo "Дамп завершен 🤡👉👌"