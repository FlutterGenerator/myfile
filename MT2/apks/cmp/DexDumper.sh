#!/data/data/com.termux/files/usr/bin/bash

trap ctrl_c INT

apk="Anticrack.login.rudra"
data="/data/data"
folder="/sdcard/DexDumper"

echo "
──╔╗─────╔╗───╔══╗──────╔╗
──║║─────║║───║╔╗║──────║║
──║╠══╦══╣║╔══╣╚╝╚╦══╦══╣╚═╦═══╗
╔╗║║║═╣║═╣║║══╣╔═╗║╔╗║╔╗║╔╗╠══║║
║╚╝║║═╣║═╣╚╬══║╚═╝║╚╝║╚╝║╚╝║║══╣
╚══╩══╩══╩═╩══╩═══╩══╩══╩══╩═══╝
"

if ! [ $(id -u) = 0 ]; then
	echo "Please run as root"
	exit
fi

if [[ -z $apk ]]; then
	echo "Usage: sudo $0 [packagename]"
	exit
fi

function ctrl_c() {
	find $folder -type d -empty -delete 2>/dev/null
	find $folder -type d \( -name "files" -o -name "lib" \) -delete 2>/dev/null
	rm -Rf $folder/oat $folder/$apk/oat
	echo -ne "\rSTOPED"
	exit
}

if [ ! -d $data/$apk ]; then
	echo -ne "\rPackagename $apk isn't installed...\n"
	exit
fi

echo "Press CTRL+C to STOP"

while true; do
 	cp -rf $data/$apk/ $folder 2>/dev/null
	echo -ne "\rRunning..."
done
