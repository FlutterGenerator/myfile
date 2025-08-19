######
Start () {
echo -e '\e[36m [0] Gihub repository
 [1] Compile
 [2] Decompile
 [3] Recourse Anti-Confusion
 [4] Recourse Confusion
 [5] Antisplit
 [6] Information \e[0m' 
read -p ' Choose option: ' option;
#####
if [ "$option" = "0" ]; then
echo -e "\e[32m [=] Opening browser...\n\e[0m"
termux-open-url https://github.com/REAndroid/APKEditor
elif [ "$option" = "1" ]; then
read -p ' Full path to directory(input): ' folder;
java -jar APKEditor*.jar b -i "$folder"
elif [ "$option" = "2" ]; then
read -p ' Full path to apk(input): ' file;
java -jar APKEditor*.jar d -i "$file"
elif [ "$option" = "3" ]; then
read -p ' Full path to apk(input): ' file;
java -jar APKEditor*.jar x -i "$file"
elif [ "$option" = "4" ]; then
read -p ' Full path to apk(input): ' file;
java -jar APKEditor*.jar p -i "$file"
elif [ "$option" = "5" ]; then
read -p ' Full path to apks, apkm or xapk(input): ' file;
java -jar APKEditor*.jar m -i "$file"
elif [ "$option" = "6" ]; then
read -p ' Full path to apk(input): ' file;
echo -e "\e[32m [=] Info:\e[0m"
java -jar APKEditor*.jar info -i "$file"
elif [ -z "$option" ]; then
echo -e "\e[31m [!] Empty option\e[0m";
else
echo -e "\e[31m [!] Unknown option ($option)\e[0m";
fi }
######
echo -e '
    █████╗ ██████╗ ██╗  ██╗███████╗██████╗ ██╗████████╗ ██████╗ ██████╗ 
   ██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██╔══██╗██║╚══██╔══╝██╔═══██╗██╔══██╗
   ███████║██████╔╝█████╔╝ █████╗  ██║  ██║██║   ██║   ██║   ██║██████╔╝
   ██╔══██║██╔═══╝ ██╔═██╗ ██╔══╝  ██║  ██║██║   ██║   ██║   ██║██╔══██╗
   ██║  ██║██║     ██║  ██╗███████╗██████╔╝██║   ██║   ╚██████╔╝██║  ██║
   ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝' | lolcat
echo -e "                                             \e[32mScript created by @toyly_s\e[0m\n"
APKEditor="/storage/emulated/0/Download" # default directory
echo -e "\n Default directory: \e[32m$APKEditor\e[0m \e[33m\n If you skip this(press enter), path will be default(You can change default directory at 50 line)\e[0m"
read -p ' Path to APKEditor: ' editor;
if [ -z "$editor" ]; then
cd $APKEditor
echo -e "\e[32m Using directory: $APKEditor\e[0m"
Start
exit
fi
cd "$editor"
echo -e "\e[32m Using directory: $editor\e[0m"
Start
exit
it

exit
