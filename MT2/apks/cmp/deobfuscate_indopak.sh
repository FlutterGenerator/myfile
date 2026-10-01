#!/data/data/com.termux/files/usr/bin/bash

INPUT="${1:-indopak}"
OUTPUT="$HOME/indopak_deobfuscated.sh"

if [ ! -f "$INPUT" ]; then
    echo "Ошибка: файл '$INPUT' не найден."
    echo "Использование:"
    echo "  bash $0 indopak"
    exit 1
fi

echo "[*] Входной файл: $INPUT"
echo "[*] Выходной файл: $OUTPUT"

TMP="$(mktemp)"

cleanup() {
    rm -f "$TMP"
}
trap cleanup EXIT

# Проверяем синтаксис исходника.
if ! bash -n "$INPUT" 2>/dev/null; then
    echo "[!] Предупреждение: исходный файл имеет необычный синтаксис."
fi

# Копируем только объявления переменных до eval.
# Финальный eval заменяем на printf, поэтому восстановленный
# код НЕ будет выполнен.
awk '
BEGIN { found=0 }

# Найден финальный eval
/^[[:space:]]*eval[[:space:]]+/ {
    found=1

    line=$0

    # Удаляем "eval " и печатаем раскрытую строку.
    sub(/^[[:space:]]*eval[[:space:]]+/, "", line)

    print "printf \"%s\\n\" " line

    next
}

# После eval ничего выполнять не нужно
found {
    next
}

{
    print
}
' "$INPUT" > "$TMP"

# Запускаем только часть с объявлениями переменных.
# eval в копии уже заменён на printf.
bash "$TMP" > "$OUTPUT" 2>/dev/null

if [ ! -s "$OUTPUT" ]; then
    echo "[!] Не удалось получить результат."
    echo "Проверь строку eval в файле."
    exit 1
fi

chmod 644 "$OUTPUT"

echo
echo "[+] Готово!"
echo "[+] Deobfuscated файл:"
echo "    $OUTPUT"
echo
echo "Проверить:"
echo "    less \"$OUTPUT\""
echo
echo "Первые строки:"
head -n 20 "$OUTPUT"