import os
import re

wlc_msg = "\033[33m" + r"""
 _____                       _____  __  __          _
|  __ \                     |  _  |/ _|/ _|        | |
| |  \/ __ _ _ __ ___   ___ | | | | |_| |_ ___  ___| |_
| | __ / _` | '_ ` _ \ / _ \| | | |  _|  _/ __|/ _ \ __|
| |_\ \ (_| | | | | | |  __/\ \_/ / | | | \__ \  __/ |_
 \____/\__,_|_| |_| |_|\___| \___/|_| |_| |___/\___|\__|


""" + "\033[0m"

print(wlc_msg)

# Code by GhostKiller - GocMod.com with Love ❤️
directory = input("Input Path file .cs: ").strip()

keywords = [
    "getcoins", "getgems", "getdiamond", "getmoney", "getcash", "getgold", "getdollar",
    "get_coins", "get_gems", "get_diamond", "get_money", "get_cash", "get_gold", "get_dollar",
    "isVIP", "isPurchased", "RemoveAds", "NoADS", "getoil", "isPro", "isVIP", "isPremium", 
    "Donated", "Unlocked", "Full", "Paid", "onetime", "isFull", "isUnlocked", "ispaid", 
    "isnoads", "isremoveads", "hasPro", "hasVIP", "hasPaid", "hasPremium", "hasNoAds", 
    "hasFull", "hasRemoveAds", "VIP", "premium", "getLV", "getPower", "get_Power", 
    "get_Purchased", "getPurchased", "getUnlock", "getUnlocked", "hasUnlocked", "isUnlocked", 
    "get_IsVIP", "getArenaUnlock", "getCoinNum", "getDiamondNum", "getSkinUnlock", 
    "IsHeroUnlocked", "get_goldCoins", "GearsUnlocked", "HeroesUnlocked", "get_Power", 
    "get_NoAdsPurchased", "get_NoAds", "get_IsPremiumPurchaser", "get_Energy", "getcoin", "get_coin"
]

keywords = [keyword.lower() for keyword in keywords]

# Code by GhostKiller - GocMod.com with Love ❤️
pattern_offset = re.compile(r"// RVA:\s+(0x[0-9A-Fa-f]+)\s+Offset:\s+(0x[0-9A-Fa-f]+)")
pattern_method = re.compile(r"public\s+(?:static\s+)?(\w+)\s+(\w+)\s*\([^)]*\)")
# Code by GhostKiller - GocMod.com with Love ❤️
def search_in_file(file_path):
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
            
            current_offset = None
            
            for line in content:
                offset_match = pattern_offset.search(line)
                if offset_match:
                    current_offset = offset_match.group(2)
                
                method_match = pattern_method.search(line)
                if method_match:
                    return_type, name = method_match.groups()
                    if name.lower() in keywords and current_offset:
                        results.append((name, return_type, current_offset))
                        current_offset = None
                        
    except Exception as e:
        print(f"Error when reading file {file_path}: {e}")
    return results

if not os.path.isdir(directory):
    print(f"The path {directory} does not exist or is not a directory.")
else:
    found_any = False
    results_to_write = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.cs'):
                file_path = os.path.join(root, file)
                results = search_in_file(file_path)
                if results:
                    found_any = True
                    for name, return_type, offset in results:
                        result_line = f"{name} ({return_type}) Offset: {offset}"
                        print(result_line)
                        results_to_write.append(result_line)
    if not found_any:
        print("No result is found.")
    else:
        output_file_path = os.path.join(directory, "result.txt")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write("\n".join(results_to_write))
        print(f"Results have been saved to {output_file_path}")
# Code by GhostKiller - GocMod.com with Love ❤️