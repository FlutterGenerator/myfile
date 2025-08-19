import r2pipe
import re
import binascii

dev = ' \033[1;32mBy Mohamed Abozaid\033[0m '

# Список файлов для обработки
files = ['libSignature.so', 'libwxcipher.so']

# Запрашиваем оригинальные SHA1 и MD5
org_SHA1 = input('\nEnter the original SHA1-Digest (or hit enter for the default V2.4.7): ').strip()
if not org_SHA1:
    org_SHA1 = '95797cb839a75de0362c2e3e3d9c0b93815a050b'

org_MD5 = input('Enter the original MD5-Digest (or hit enter for the default V2.4.7): ').strip()
if not org_MD5:
    org_MD5 = '82a45919ce5501ac2bf4aee3679d793e'

# Запрашиваем пользовательские значения для SHA1 и MD5
custom_SHA1 = input('Enter your Custom SHA1: ').strip()
custom_MD5 = input('Enter your Custom MD5: ').strip()

# Функция для поиска и замены бинарных данных
def search_and_replace_binary(r2, digest, custom_digest, hash_type):
    digest_bin = binascii.unhexlify(digest)  # Преобразуем хеш в бинарный формат
    custom_bin = binascii.unhexlify(custom_digest)
    
    # Поиск бинарных данных в файле
    px = r2.cmdj(f"pxj ~[{', '.join(map(str, digest_bin))}]")  # Ищем SHA1 в бинарном формате
    print(f'Searching for {hash_type} as binary: {digest}')
    
    if px and len(px) > 0 and px[0] != 0:
        addr = hex(px[0])  # Берем первый адрес из списка найденных
        r2.cmd(f'w {binascii.hexlify(custom_bin).decode()} @ {addr}')  # Записываем новые данные
        print(f'Written {custom_digest} at address {addr}\n')
        return True
    else:
        print(f'Error: {hash_type} {digest} not found or invalid address.\n')
        return False

# Проходим по каждому файлу
for file in files:
    r2 = r2pipe.open(filename=file, flags=['-w', '-e bin.relocs.apply=true'])

    print('\n')
    print('\033[93m#\033[0m' * 39)
    print(dev.center(50, '#'))
    
    # Обработка SHA1 в libSignature.so
    if file == 'libSignature.so':
        print(f"Processing SHA1 in {file}".center(50, '#'))
        print(f'\nProcessing SHA1 in {file}...')
        if not search_and_replace_binary(r2, org_SHA1, custom_SHA1, 'SHA1'):
            print(f'Error: SHA1 {org_SHA1} not found in {file}.')

    # Обработка MD5 в libwxcipher.so
    elif file == 'libwxcipher.so':
        print(f"Processing MD5 in {file}".center(50, '#'))
        print(f'Processing MD5 in {file}...')
        if not search_and_replace_binary(r2, org_MD5, custom_MD5, 'MD5'):
            print(f'Error: MD5 {org_MD5} not found in {file}.')

    r2.quit()

print('Add the modified .so files back now\n')