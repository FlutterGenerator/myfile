import subprocess
import os
import time

print("👑 Mini Militia Dumper 👑 \n\n Dev : @tojik_proof_93\n Age : 18\n\n")

# Bash-скрипт для выполнения через radare2
bash_script = """
#!/bin/bash
if ! command -v r2 &> /dev/null; then
    echo "Installing radare2"
    pkg install -y radare2 &> /dev/null
fi
r2 -w libcocos2dcpp.so << EOF &> /dev/null
iE > jni.txt
q
EOF
"""

# Создаем временный Bash-скрипт
with open('jni.sh', 'w') as script_file:
    script_file.write(bash_script)

# Выполняем Bash-скрипт
subprocess.Popen(['sh', 'jni.sh'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Подождем 10 секунд для завершения работы скрипта
time.sleep(10)

# Ищем паттерны в файле jni.txt
target_patterns = {
    '_ZN22SoldierLocalController5getHPEv': 'HP offset'
}

with open('jni.txt', 'r') as file:
    lines = file.readlines()

found_lines = {}
for pattern, offset_name in target_patterns.items():
    for line in lines:
        if pattern in line:
            found_lines[pattern] = line
            break

global_offsets = {}
for pattern, line in found_lines.items():
    parts = line.split()
    for part in parts:
        if part.startswith('0x') and len(part) == 10:
            global_offsets[target_patterns[pattern]] = part
            break

# Запись offset'ов в dump.txt
with open('dump.txt', 'w') as dump_file:
    for name, offset in global_offsets.items():
        dump_file.write(f"{name} = {offset}\n")

print(f" HunMod \n\n Success dump.txt")

# Удаляем временный файл jni.txt
os.remove('jni.txt')

# Удаляем Bash-скрипт
os.remove('jni.sh')