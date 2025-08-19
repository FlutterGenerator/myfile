from decimal import Decimal

def decimal_to_hex(decimal_number, bit_length, add_prefix):
    """
    將十進制數字轉換為十六進制表示，支持 32 位和 64 位。

    參數:
        decimal_number (Decimal): 要轉換的十進制數字
        bit_length (int): 指定轉換的位數，應為 32 或 64
        add_prefix (bool): 是否在十六進制表示前加上"0x"前綴

    返回:
        str: 對應的十六進制字符串
    """
    if not isinstance(decimal_number, Decimal):
        raise ValueError("輸入必須是一個 Decimal 類型")
    
    if decimal_number < 0:
        raise ValueError("輸入必須是一個非負數")
    
    hex_string = hex(int(decimal_number))[2:].upper()
    
    if bit_length == 32:
        hex_string = hex_string.zfill(8)
    elif bit_length == 64:
        hex_string = hex_string.zfill(16)
    else:
        raise ValueError("位長度必須是32或64")
    
    return "0x" + hex_string if add_prefix else hex_string

def validate_input(user_input):
    """
    驗證用戶輸入是否為有效的整數。

    參數:
        user_input (str): 用戶輸入的字符串

    返回:
        Decimal: 如果輸入有效，返回轉換後的 Decimal 數字
    """
    try:
        value = Decimal(user_input)
        if value < 0:
            raise ValueError("輸入必須是一個非負數")
        return value
    except Exception:
        raise ValueError("輸入無效，請輸入一個有效的非負十進制整數")

def choose_bit_length(prompts):
    """
    提示用戶選擇位長度

    參數:
        prompts (dict): 提示信息字典

    返回:
        int: 用戶選擇的位長度
    """
    while True:
        bit_length = input(prompts['choose_bits']).strip().lower()
        if bit_length == 'exit':
            print(prompts['exit'])
            return None
        elif bit_length in ['32', '64']:
            return int(bit_length)
        else:
            print(prompts['invalid_choice'])

def get_decimal_number(prompts):
    """
    提示用戶輸入十進制數字

    參數:
        prompts (dict): 提示信息字典

    返回:
        Decimal: 用戶輸入的十進制數字
    """
    while True:
        user_input = input(prompts['enter_number'])
        if user_input.lower() == 'exit':
            print(prompts['exit'])
            return None
        else:
            try:
                return validate_input(user_input)
            except ValueError as e:
                print(f"{prompts['error']} {e}")

def ask_add_prefix(prompts):
    """
    提問用戶是否添加 '0x' 前綴

    參數:
        prompts (dict): 提示信息字典

    返回:
        bool: 用戶選擇是否添加 '0x' 前綴
    """
    while True:
        add_prefix = input(prompts['add_prefix']).strip().lower()
        if add_prefix in ['y', 'n']:
            return add_prefix == 'y'
        else:
            print(prompts['invalid_prefix_choice'])

def select_language(languages, prompts):
    """
    選擇語言

    參數:
        languages (dict): 可用語言字典
        prompts (dict): 提示信息字典

    返回:
        str: 選擇的語言
    """
    print(prompts['language_selection'])
    for key, value in languages.items():
        print(f"{key}: {value}")
    
    while True:
        choice = input(prompts['language_prompt']).strip().lower()
        if choice in languages:
            return languages[choice]
        elif choice in languages.values():
            return choice
        else:
            print(prompts['invalid_language'])

def convert_number(decimal_number, base):
    """
    將十進制數字轉換為指定基數的字符串表示。

    參數:
        decimal_number (Decimal): 要轉換的十進制數字
        base (int): 目標進制，支持 2（二進制）、8（八進制）、16（十六進制）

    返回:
        str: 對應的進制字符串
    """
    if base == 2:
        return bin(int(decimal_number))[2:]
    elif base == 8:
        return oct(int(decimal_number))[2:]
    elif base == 16:
        return hex(int(decimal_number))[2:].upper()
    else:
        raise ValueError("不支持的進制")

def main():
    languages = {
        'zh': '中文',
        'en': 'English'
    }
    
    language_prompts = {
        '中文': {
            'welcome': "歡迎使用進制轉換器！",
            'options': "您可以進行以下操作：\n1. 輸入一個十進制數字來查看其進制表示\n2. 輸入 'exit' 退出程序",
            'choose_base': "請選擇轉換的目標進制（2, 8, 16，輸入 'exit' 退出）：",
            'invalid_choice_base': "無效的選擇，請輸入 2, 8 或 16。",
            'choose_bits': "請選擇轉換的位數（32 或 64，輸入 'exit' 退出）：",
            'invalid_choice': "無效的選擇，請輸入 32 或 64。",
            'enter_number': "請輸入一個十進制數字來轉換（輸入 'exit' 退出）：",
            'add_prefix': "是否在十六進制表示前加上'0x'前綴？（y/n）：",
            'invalid_prefix_choice': "無效的選擇，請輸入 'y' 或 'n'。",
            'exit': "退出程序。",
            'error': "錯誤：",
            'result': "{decimal_number} 的 {base} 進制表示為: {result}",
            'language_selection': "可用語言",
            'language_prompt': "請輸入語言名稱或代碼：",
            'invalid_language': "無效選擇，請重試。"
        },
        'English': {
            'welcome': "Welcome to the Base Converter!",
            'options': "You can perform the following actions:\n1. Enter a decimal number to see its base representation\n2. Enter 'exit' to quit the program",
            'choose_base': "Please choose the target base for conversion (2, 8, 16, enter 'exit' to quit):",
            'invalid_choice_base': "Invalid choice, please enter 2, 8, or 16.",
            'choose_bits': "Please choose the bit length for conversion (32 or 64, enter 'exit' to quit):",
            'invalid_choice': "Invalid choice, please enter 32 or 64.",
            'enter_number': "Please enter a decimal number to convert (enter 'exit' to quit):",
            'add_prefix': "Do you want to add '0x' prefix to the hexadecimal representation? (y/n):",
            'invalid_prefix_choice': "Invalid choice, please enter 'y' or 'n'.",
            'exit': "Exiting the program.",
            'error': "Error:",
            'result': "The {base} base representation of {decimal_number} is: {result}",
            'language_selection': "Available Languages",
            'language_prompt': "Please enter the language name or code:",
            'invalid_language': "Invalid choice, please try again."
        }
    }

    language = select_language(languages, language_prompts['English'])
    prompts = language_prompts[language]
    
    print(prompts['welcome'])
    print(prompts['options'])
    
    while True:
        base_choice = input(prompts['choose_base']).strip().lower()
        if base_choice == 'exit':
            print(prompts['exit'])
            break
        elif base_choice in ['2', '8', '16']:
            base = int(base_choice)
        else:
            print(prompts['invalid_choice_base'])
            continue

        decimal_number = get_decimal_number(prompts)
        if not decimal_number:
            break

        if base == 16:
            bit_length = choose_bit_length(prompts)
            if not bit_length:
                break

            add_prefix = ask_add_prefix(prompts)
            try:
                result = decimal_to_hex(decimal_number, bit_length, add_prefix)
            except ValueError as e:
                print(f"{prompts['error']} {e}")
                continue
        else:
            try:
                result = convert_number(decimal_number, base)
            except ValueError as e:
                print(f"{prompts['error']} {e}")
                continue

        print(prompts['result'].format(decimal_number=decimal_number, base=base, result=result))

if __name__ == "__main__":
    main()