import os
from colorama import init, Fore, Style

init(autoreset=True)

def loading_animation(percent):
    black_squares = "⬛"
    white_squares = "⬜"
    num_black = int(percent / 5)
    num_white = 20 - num_black
    progress_bar = f"{Fore.GREEN}[{black_squares * num_black}{white_squares * num_white}] {percent}%{Style.RESET_ALL}"
    print(progress_bar, end='\r')

def search_word_in_files(directory, search_word):
    matching_lines = {}
    total_files = sum([len(files) for _, _, files in os.walk(directory)])
    processed_files = 0

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            with open(file_path, 'r', encoding='utf-8') as f:
                for line_number, line in enumerate(f, 1):
                    if search_word.lower() in line.lower() and any(f"r{i}" in line for i in range(-25, 26)):
                        line += '\n\n' if line.strip() else '\n'

                        if file not in matching_lines:
                            matching_lines[file] = []
                        matching_lines[file].append((line_number, line))

            processed_files += 1
            loading_progress = int((processed_files / total_files) * 100)
            loading_animation(loading_progress)

    total_words_found = sum(len(lines) for lines in matching_lines.values())

    if total_words_found > 0:
        output_file_path = f'/storage/emulated/0/MT2/apks/1{search_word}.txt'
        with open(output_file_path, 'a', encoding='utf-8') as output_file:
            output_file.write(f"{Fore.YELLOW}============================= {search_word.upper()} ============================={Fore.YELLOW}\n")
            for file, lines in matching_lines.items():
                output_file.write("\n\n\n")
                output_file.write(f"{Fore.CYAN}============================= {os.path.basename(file)} ============================={Fore.CYAN}\n")
                for line_number, line in lines:
                    output_file.write(f"Line {line_number}: {line}")

        print(f"\nWords have been added to {os.path.basename(output_file_path)}")

def get_search_keyword():
    while True:
        print(f"{Fore.GREEN}Enter the keyword to search (to exit: 'q'):")
        search_word = input(">>> ").strip()
        if search_word.lower() == 'q':
            return 'q'
        elif search_word.lower() == 'dl':
            delete_output_files()
        else:
            return search_word

def search_and_add_lines_with_keywords(directory, search_word):
    keywords = ['vipuser', 'ispro', 'isprouser', 'ispremium', 'ispremiumuser', 'alreadyvip', 'ispurchased', 'unlocked', 'adremoved', 'gopremium', 'removed_ads', 'is_subscribed', 'subscribe_pro', 'ispurchase', 'purchase', 'ispremium', 'getpremium', 'mispremium', '"pro"ispro', 'subscribe', 'vip', 'isuservip', 'vipaccess', 'proaccess', 'premiumaccess', 'subscribeduser', 'prosubscription', 'premiumsubscription', 'purchasedsubscription', 'vipsubscription', 'is_vip_subscribed', 'is_pro_subscribed', 'is_premium_subscribed', 'pro_member', 'premium_member', 'subscribed_member', 'pro_membership', 'premium_membership', 'purchased_membership', 'vip_membership', 'is_vip_member', 'is_pro_member', 'is_premium_member', 'vip_status', 'pro_status', 'premium_status', 'vip_plan', 'pro_plan', 'premium_plan', 'vip_upgrade', 'pro_upgrade', 'premium_upgrade', 'vip_feature', 'pro_feature', 'premium_feature', 'vip_content', 'pro_content', 'premium_content', 'accountType', 'pro_offer', 'premium_offer', 'vip_offer', 'donate', 'isdonate', 'is_vip_purchased', 'donate_and_remove_ads', 'donate_remove_ads', 'ad_free', 'no_ads', 'remove_ads', 'ad_removal', 'vip_purchase', 'pro_purchase', 'premium_purchase', 'subscription_plan', 'subscribed_plan', 'vip_plan_purchase', 'pro_plan_purchase', 'premium_plan_purchase', 'upgrade_to_vip', 'upgrade_to_pro', 'upgrade_to_premium', 'buy_premium', 'buy_pro', 'buy_vip', 'purchased_vip', 'purchased_pro', 'purchased_premium', 'membership_plan', 'vip_membership_plan', 'pro_membership_plan', 'premium_membership_plan', 'get_member_features', 'user_features', 'avail_vip_features', 'avail_pro_features', 'avail_premium_features', 'membership_status', 'vip_membership_status', 'pro_membership_status', 'premium_membership_status', 'show_vip_content', 'show_pro_content', 'show_premium_content', 'unlock_member_benefits', 'member_discounts', 'special_offers', 'exclusive_access', 'get_all_features', 'complete_feature_set']

    total_words_found = 0
    new_file_path = f"/storage/emulated/0/MT2/apks/2{search_word}.txt"

    with open(new_file_path, "w") as new_file:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".txt"):
                    with open(os.path.join(root, file), "r") as f:
                        lines = f.readlines()
                        for line in lines:
                            if any(f"r{i}" in line for i in range(-25, 26)):
                                for keyword in keywords:
                                    if keyword in line.lower():
                                        new_file.write(line.strip() + '\n\n')
                                        total_words_found += 1
                    print(Fore.GREEN + "Loading..." + Style.RESET_ALL, end='\r')

    if total_words_found > 0:
        print(f"Total words found: {total_words_found}\n")
        remove_duplicate_keywords(new_file_path)

    if total_words_found == 0:
        os.remove(new_file_path)

def delete_output_files():
    output_directory = "/storage/emulated/0/MT2/apks/"
    for file in os.listdir(output_directory):
        if file.endswith(".txt"):
            os.remove(os.path.join(output_directory, file))
    print("All output .txt files have been deleted.")

def remove_duplicate_keywords(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    lines = list(dict.fromkeys(lines))

    with open(file_path, 'w') as file:
        file.writelines(lines)

def main():
    while True:
        search_word = get_search_keyword()
        if search_word.lower() == 'q':
            break
        search_word_in_files('/storage/emulated/0/MT2/apks/out_dir/asm/', search_word)
        search_and_add_lines_with_keywords('/storage/emulated/0/MT2/apks/', search_word)

if __name__ == "__main__":
    main()
