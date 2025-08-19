import r2pipe
import re

dev = ' \033[1;32mBy Mohamed Abozaid\033[0m '

# Открываем файл с помощью r2pipe
r2 = r2pipe.open(filename='libdingtone.so', flags=['-w', '-e bin.relocs.apply=true'])

print('\n')
print('\033[93m#\033[0m' * 39)
print(dev.center(50, '#'))
print('\033[93m#\033[0m' * 39)

# Запрашиваем оригинальный SHA1
org_SHA1 = input('\nEnter The original SHA1-Digest (or hit enter for the default V2.4.7): ').strip()
if not org_SHA1:
    org_SHA1 = '118676ae1076dce81c4bfebbc63660ed3708e06b'

# Запрашиваем пользовательский SHA1
costum_SHA1 = input('Enter your Custom SHA1: ').strip()

# Поиск адреса по оригинальному SHA1
iz = r2.cmd(f'iz ~+{org_SHA1}')
srch_res = re.search(r'0x[0-9A-Fa-f]{1,10}', iz)  # Исправлено: {,10} на {1,10}
if srch_res:
    addr = srch_res.group()
    
    # Запись пользовательского SHA1 по найденному адресу
    r2.cmd(f'w {costum_SHA1} @ {addr}')
    print(f'\nWritten {costum_SHA1} at address {addr}\n')
else:
    print(f'Error: SHA1 {org_SHA1} not found.')

print('Add libdingtone.so back now\n')