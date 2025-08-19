#!/bin/bash
# regular colors
red='\033[0;31m'
green='\033[0;32m'
blue='\033[0;34m'
purple='\033[0;35m'
cyan='\033[0;36m'
white='\033[0;37m'
# bold
bred='\033[1;31m'
bgreen='\033[1;32m'
byellow='\033[1;33m'
end='\033[0m'

display_menu() {
echo -e "${cyan}
:::        :::::::::  :::::::::  ::::    :::: ::::::::::: 
:+:        :+:    :+: :+:    :+: +:+:+: :+:+:+    :+:     
+:+        +:+    +:+ +:+    +:+ +:+ +:+:+ +:+    +:+     
+#+        +#++:++#+  +#++:++#+  +#+  +:+  +#+    +#+     
+#+        +#+        +#+        +#+       +#+    +#+     
#+#        #+#        #+#        #+#       #+#    #+#     
########## ###        ###        ###       ###    ###     
${end}
${bgreen}Created by toyly_s${end}
${byellow}Version: 1.0${end}
"
    echo "1. Add Package Name"
    echo "2. Add [CLASSES]"
    echo "3. Add message if patch successfull"
    echo "4. Preview"
    echo "6. Exit"
    echo -n "Choose an option: "
}

blank=""

add_pkg() {
if [[ "$blank" =~ "[PACKAGE]" ]]; then
echo "You're already added package name"; sleep 3
else
echo -ne "Enter package name of apk: "; read pkg_name
blank+="[BEGIN]
#Description of patch
[PACKAGE]
${pkg_name}
"
fi
}

add_class() {
if ! [[ "$blank" =~ "[PACKAGE]" ]]; then
echo "First add package name"; sleep 3
else
blank+="
[CLASSES]"
echo -en " Enter class name(eg: Lcom/main/ui/shop;)(press enter to skip): "; read cls_name
if [[ -z "$cls_name" ]]; then
class_name=""
else
class_name="{\"class name\":\"${cls_name}\"}"
fi
echo -en " Enter method name(eg: isPro): "; read mtd_name
if [[ -z "$mtd_name" ]]; then
exit 1
fi
echo -en " Enter parameter(s)(eg: Ljava/lang/String;), if empty press enter: "; read prmtr_name
if [[ -z $prmtr_name ]]; then
prmtr_name=""
else
prmtr_name="{\"parameter types\":\"${prmtr_name}\"}"
fi
echo -en " Enter return type(eg: Z): "; read rt_name
if [[ -z "$rt_name" ]]; then
exit 1
fi
echo -en " Enter original bytes(press enter to skip): "; read org_bytess
if [[ -z "$org_bytess" ]]; then
org_bytes=""
else
org_bytes="{\"original\":\"${org_bytess}\"}"
fi
if [[ "$rt_name" == 'Z' ]]; then
echo -e "Example:\n12 10 0F 00 - true\n12 00 0F 00 - false"
fi
if [[ "$rt_name" == 'V' ]]; then
echo -e "Example:\n00 00 0E 00 - empty void"
fi
echo -en " Enter bytes to modify: "; read mod_bytes
if [[ -z "$mod_bytes" ]]; then
exit 1
fi

blank+="
${class_name}
{\"method name\":\"${mtd_name}\"}
${prmtr_name}
{\"return type\":\"${rt_name}\"}
${org_bytes}
{\"replaced\":\"${mod_bytes}\"}
"
fi
}

add_end() {
if ! [[ "$blank" =~ "[PACKAGE]" ]]; then
echo "First add package name"; sleep 3
elif ! [[ "$blank" =~ "[CLASSES]" ]]; then
echo "Add [CLASSES]"; sleep 3
else
echo -n "Enter message: "; read end_msg
blank+="
[END]
${end_msg}"
fi
}

# preview, save patch and exit
save() {
echo "
${blank}
"
echo -en "Save to text[y/s]? "; read yesno
if [[ "$yesno" == 'y' ]]; then
local p_path="/sdcard/${pkg_name}.txt"
cat > ${p_path} << EOF
${blank}
EOF
sed -i '/^$/d' ${p_path}
exit 1
fi
}

while true; do
clear
    display_menu
    read choice
    case $choice in
        1) add_pkg;;
        2) add_class;;
        3) add_end;;
        4) save;;
        6) exit 0;;
        *) echo "Invalid choice";;
    esac
done