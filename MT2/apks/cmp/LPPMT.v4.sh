#!/bin/bash
#regular colors
black='\033[0;30m'
red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
blue='\033[0;34m'
purple='\033[0;35m'
cyan='\033[0;36m'
white='\033[0;37m'
#bold colors
bblack='\033[1;30m'
bred='\033[1;31m'
bgreen='\033[1;32m'
byellow='\033[1;33m'
bblue='\033[1;34m'
bpurple='\033[1;35m'
bcyan='\033[1;36m'
bwhite='\033[1;37m'
#end color
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
${bblue}Version: 4.0${end}"
    echo
    echo -e "${green}1. Add Package Name${end}"
    echo -e "${blue}a. Add [CLASSES]"
    echo -e "b. Add [FILE_IN_APK]"
    echo -e "c. Add [SHARED-PREFERENCES](delete doesn't support)"
    echo -e "d. Add [OTHER FILES]"
    echo -e "e. Add [COMPONENT]"
    echo -e "f. Add [BLOCK HOSTS]"
    echo -e "g. Add [LIB]${end}"
    echo -e "${purple}2. Add [END](add message if patching successful)${end}"
    echo -e "${yellow}3. Preview${end}"
    echo -e "${red}4. Exit${end}"
    echo -ne "Choose an option: "
}

blank=""

add_pkg() {
echo -en "Enter package name(ex: ${green}com.example.app${end}): "; read pkg_name
echo -en "Enter ${green}description${end} of patch: "; read description
blank+="[BEGIN]
${description}"
echo -en "Enable \"${green}Signature verification killer${end}\" option in patch[y/n]? : "; read ctf_kill
if [[ "$ctf_kill" == "y" ]]; then
blank+="
[use_signature_verification_killer]"
fi
echo -en "Enable \"${green}Removes integrity check and signature verification${end}\" option in patch[y/n]? : "; read ctf_dex_kill
if [[ "$ctf_dex_kill" == "y" ]]; then
blank+="
[use_dex_and_signature_verification_killer]"
fi
echo -en "Enable \"${green}Fake a modified APK archive from the original${end}\" option in patch[y/n]? : "; read fake_crc
if [[ "$fake_crc" == "y" ]]; then
blank+="
[use_fake_modified_apk_archive]"
fi

echo -en "Enable ${green}Free inapp emulation${end} and ${green}License validator${end} option in patch[y/n]? : "; read free_inapp
if [[ "$free_inapp" == "y" ]]; then
blank+="
[integrate_inapp_lvl_emulation]"
fi
}

add_class() {
if ! [[ "$blank" =~ "[BEGIN]" ]]; then
echo -en "First add ${red}package name${end}"; sleep 3
else
blank+="
[CLASSES]"

while true; do
echo -en " Enter ${green}class name${end}(ex: ${yellow}Lcom/main/ui/shop;${end})(press enter to skip): "; read cls_name
if [[ -z "$cls_name" ]]; then
class_name=""
else
class_name="{\"class name\":\"${cls_name}\"}"
fi
echo -en " Enter ${green}method name${end}(ex: ${yellow}isPro${end})(press enter to skip): "; read mtd_name
if [[ -z "$mtd_name" ]]; then
mtd_name=""
else
mtd_name="{\"method name\":\"${mtd_name}\"}"
fi
echo -en " Enter ${green}parameter(s)${end}(ex: ${yellow}Ljava/lang/String;${end}), if empty press enter: "; read prmtr_name
if [[ -z $prmtr_name ]]; then
prmtr_name=""
else
prmtr_name="{\"parameter types\":\"${prmtr_name}\"}"
fi
echo -en " Enter ${green}return type${end}(ex: ${yellow}Z${end})(press enter to skip): "; read rt_name
if [[ -z $rt_name ]]; then
rt_name=""
else
rt_name="{\"return type\":\"${rt_name}\"}"
fi
echo -en " Enter ${green}original bytes${end}: "; read org_bytess
org_bytess=$(echo $org_bytess | tr '[:lower:]' '[:upper:]')
if [[ -z "$org_bytess" ]]; then
org_bytes=""
else
org_bytes="{\"original\":\"${org_bytess}\"}"
fi
if [[ "$rt_name" == 'Z' ]]; then
echo -e "Example:\n ${green}12 10 0F 00${end} - true(means ${yellow}const/4 v0, 0x1${end} and ${yellow}return v0${end})\n ${green}12 00 0F 00${end} - false(means ${yellow}const/4 v0, 0x0${end} and ${yellow}return v0${end})"
fi
if [[ "$rt_name" == 'V' ]]; then
echo -e "Example:\n ${green}00 00 0E 00${end} - empty void(means ${yellow}nop${end} and ${yellow}return-void${end})"
fi
echo -en " Enter ${green}bytes to modify${end}: "; read mod_bytes
mod_bytes=$(echo $mod_bytes | tr '[:lower:]' '[:upper:]')
if [[ -z "$mod_bytes" ]]; then
echo -e "${red}Don't skip!, it's important${end}"; sleep 3
fi

blank+="
${class_name}
${mtd_name}
${prmtr_name}
${rt_name}
${org_bytes}
{\"replaced\":\"${mod_bytes}\"}"
echo -en "Press \"${red}s${end}\" to ${red}stop conversation${end} for [CLASSES],(write any letter for continue): "; read c_f
if [[ "$c_f" == "s" ]]; then
break
fi
done
fi
}

add_file_in_apk() {
if ! [[ "$blank" =~ "[BEGIN]" ]]; then
echo "First add ${red}package name${end}"; sleep 3
else
blank+="
[FILE_IN_APK]"
while true; do
echo -en "Enter ${green}path${end} to file in apk: "; read f_file_path
if [[ -z "$f_file_path" ]]; then
echo -e "${red}Don't skip!, it's important${end}"; sleep 3
fi
echo -en "Enter ${green}offset${end}(press enter to skip): "; read f_offset
f_offset=$(echo $f_offset | tr '[:lower:]' '[:upper:]')

if [[ -z "$f_offset" ]]; then
f_offset=""
else
f_offset="{\"offset\":\"${f_offset}\"}"
fi
echo -en "Enter ${green}original bytes${end}(it's not necessary if you wrote offset): "; read f_org_bytes
f_org_bytes=$(echo $f_org_bytes | tr '[:lower:]' '[:upper:]')
if [[ -z "$f_org_bytes" ]]; then
f_org_bytes=""
else
f_org_bytes="{\"original\":\"${f_org_bytes}\"}"
fi
echo -en "Enter ${green}bytes to modify${end}: "; read f_mod_bytes
f_mod_bytes=$(echo $f_mod_bytes | tr '[:lower:]' '[:upper:]')
if [[ -z "$f_mod_bytes" ]]; then
echo -e "${red}Don't skip!, it's important${end}"; sleep 3
fi
blank+="{\"name\":\"${f_file_path}\"}
${f_offset}
${f_org_bytes}
{\"replaced\":\"${f_mod_bytes}\"}"
echo -en "Press \"${red}s${end}\" to ${red}stop conversation${end} for [FILE_IN_APK],(write any letter for continue): "; read c_f
if [[ "$c_f" == "s" ]]; then
break
fi
done
fi
}

add_SP() {
if ! [[ "$blank" =~ "[BEGIN]" ]]; then
echo -e "First add ${red}package name${end}"; sleep 3
else

blank+="
[SHARED-PREFERENCES]"

while true; do
echo -en " Enter ${green}shared_preference.xml${end} file name(current file: ${sp_f_name}): "; read sp_f_name
if [[ -z "$sp_f_name" ]]; then
sp_f_name=""
else
sp_f_name="{\"file_name\":\"${sp_f_name}\"}"
fi
echo -en " Enter ${green}value name${end}(ex: ${yellow}is_purchased${end}): "; read sp_p_name
echo -en " Enter ${green}value type${end}(${green}int${end}, ${green}string${end}, ${green}long${end}, ${green}float${end} or ${green}boolean${end}): "; read sp_v_type
echo -en " Enter ${sp_p_name}(${sp_v_type}) value: "; read sp_p_value
sp_v_type="{\"insert\":\"${sp_v_type}\"}"
sp_p_name="{\"pref_name\":\"${sp_p_name}\"}"
sp_p_value="{\"value\":\"${sp_p_value}\"}"

blank+="
${sp_f_name}
${sp_v_type}
${sp_p_name}
${sp_p_value}"
echo -en "Press \"${red}s${end}\" to stop conversation for [SHARED-PREFERENCES],(write any letter for continue): "; read c_f
if [[ "$c_f" == "s" ]]; then
break
fi
done
fi
}

add_other_files() {
if ! [[ "$blank" =~ "[BEGIN]" ]]; then
echo -e "First add ${red}package name${end}"; sleep 3
else
while true; do
echo -en " 1. Byte replacement\n 2. Insert bytes\n 3. Stop conversation\n Choose(1/2/3): "; read choose
if [[ $choose -eq 3 ]]; then
break
elif [[ $choose -eq 1 ]]; then
blank+="
[OTHER FILES]"
echo -en " Enter ${green}file name${end}: "; read o_f_name
if [[ -z "$o_f_name" ]]; then
o_f_name=""
else
o_f_name="{\"name\":\"${o_f_name}\"}"
fi
echo -en " Enter ${green}offset${end}(press enter to skip): "; read o_offset
o_offset=$(echo $o_offset | tr '[:lower:]' '[:upper:]')

if [[ -z "$o_offset" ]]; then
o_offset=""
else
o_offset="{\"offset\":\"${o_offset}\"}"
fi

echo -en " Enter ${green}original bytes${end}(it's not necessary if you wrote offset): "; read o_org_bytes
o_org_bytes=$(echo $o_org_bytes | tr '[:lower:]' '[:upper:]')

if [[ -z "$o_org_bytes" ]]; then
o_org_bytes=""
else
o_org_bytes="{\"original\":\"${o_org_bytes}\"}"
fi
echo -en " Enter ${green}bytes to modify${end}: "; read o_mod_bytes
o_mod_bytes=$(echo $o_mod_bytes | tr '[:lower:]' '[:upper:]')

if [[ -z "$o_mod_bytes" ]]; then
echo -e "${red}Don't skip!  It's important${end}"; sleep 3
else
o_mod_bytes="{\"replaced\":\"${o_mod_bytes}\"}"
fi
blank+="
${o_f_name}
${o_offset}
${o_org_bytes}
${o_mod_bytes}"
else
blank+="
[OTHER FILES]"
echo -en " Enter ${green}file name${end}: "; read o_f_name
if [[ -z "$o_f_name" ]]; then
echo -e "${red}Don't skip!  It's important${end}"; sleep 3
else
o_f_name="{\"name\":\"${o_f_name}\"}"
fi

echo -en " Enter ${green}original bytes${end}: "; read o_org_bytes
o_org_bytes=$(echo $o_org_bytes | tr '[:lower:]' '[:upper:]')

if [[ -z "$o_org_bytes" ]]; then
echo -e "${red}Don't skip!  It's important${end}"; sleep 3
else
o_org_bytes="{\"original\":\"${o_org_bytes}\"}"
fi

echo -en " Enter ${green}bytes to insert${end}: "; read o_insert
o_insert=$(echo $o_insert | tr '[:lower:]' '[:upper:]')

if [[ -z "$o_insert" ]]; then
echo -e "${red}Don't skip! It's important${end}"; sleep 3
else
o_insert="{\"insert\":\"${o_insert}\"}"
fi
blank+="
${o_f_name}
${o_org_bytes}
${o_insert}"
fi
done
fi
}

add_compnt() {
if ! [[ "$blank" =~ "[BEGIN]" ]]; then
echo -e "First add ${red}package name${end}"; sleep 3
else

blank+="
[COMPONENT]"
while true; do
echo -en "Enter ${green}component${end}(ex: ${yellow}com.android.ad.AdActivity${end})(\"${red}s${end}\" for ${red}stop${end}): "; read component

if [[ "$component" == "s" ]]; then
break
fi
echo -en "[${green}enable${end}/${red}disable${end}] component? "; read eord
blank+="
{\"${eord}\":\"${component}\"}"
done
fi
}

add_blc_hst() {
if ! [[ "$blank" =~ "[BEGIN]" ]]; then
echo -e "First add ${red}package name${end}"; sleep 3
else

blank+="
[BLOCK HOSTS]"
while true; do
echo -en "Enter ${green}host${end}(ex: ${yellow}google.com${end})(\"${red}s${end}\" for ${red}stop${end}): "; read host
if [[ "$host" == "s" ]]; then
break
fi
blank+="
{\"host\":\"$host\"}"
done
fi
}

add_lib() {
if ! [[ "$blank" =~ "[BEGIN]" ]]; then
echo -e "First add ${red}package name${end}"; sleep 3
else
blank+="
[LIB]"
while true; do
echo -en "\n${green}[LIB-ARMEABI]\n[LIB-ARMEABI-V7A]\n[LIB-ARM64-V8A]\n[LIB-MIPS]\n[LIB-X86]\n[LIB-X86_64]${end}\nChoose one of ${green}these${end}(press enter to skip, \"${red}s${end}\" to ${red}stop${end}): "; read arch
if [[ "$arch" == "s" ]]; then
break
fi
echo -en "Enter ${green}native library name${end}"; read lib_name
if [[ -z "$lib_name" ]]; then
lib_name=""
else
lib_name="{\"name\":\"${lib_name}\"}"
fi

echo -en "Enter ${green}offset${end}"; read lib_offset
if [[ -z "$lib_offset" ]]; then
lib_offset=""
else
lib_offset="{\"offset\":\"${lib_offset}\"}"
fi

echo -en "Enter ${green}original bytes${end}"; read lib_org_bytes
if [[ -z "$lib_org_bytes" ]]; then
lib_org_bytes=""
else
lib_org_bytes="{\"original\":\"${lib_org_bytes}\"}"
fi

echo -en "Enter ${green}bytes to modify${end}"; read lib_mod_bytes


blank+="
${arch}
${lib_name}
${lib_offset}
${lib_org_bytes}
{\"replaced\":\"${lib_mod_bytes}\"}"
done
fi
}

add_end() {
echo -en "Enter ${green}success message${end}: "; read end_msg
blank+="
[END]
${end_msg}"
}

save() {
echo
echo -e "\n${blank}\n" | sed '/^$/d'
echo
echo -en "Save to text[y/n]? "; read yesno
if [[ "$yesno" == 'y' ]]; then
local p_path="/sdcard/${pkg_name}.txt"
cat > ${p_path} << EOF
${blank}
EOF
sed -i '/^$/d' ${p_path}
echo -e "Patch saved: ${green}/sdcard/${pkg_name}.txt${end}"
exit 1
fi
}

while true; do
clear
    display_menu
    read choice
    case $choice in
        1) add_pkg;;
       "a") add_class;;
       "b") add_file_in_apk;;
       "c") add_SP;;
       "d") add_other_files;;
       "e") add_compnt;;
       "f") add_blc_hst;;
       "g") add_lib;;
        2) add_end;;
        3) save;;
        4) exit 0;;
        *) echo -e "${red}Invalid choice${end}"; sleep 3;;
    esac
done