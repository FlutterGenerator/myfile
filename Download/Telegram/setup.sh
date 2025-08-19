#!/bin/bash
termux-setup-storage
# Update and upgrade packages
pkg update -y && pkg upgrade -y

# Install necessary packages
pkg install git -y && \
pkg install curl -y && \
pkg install clang -y && \
pkg install rust -y

# Clear the screen
clear

# Install the cargo package
if cargo install --git https://github.com/trumank/uesave-rs.git; then
    # If the cargo install command succeeds, add the PATH export to bash.bashrc
    echo 'export PATH="$PATH:/data/data/com.termux/files/home/.cargo/bin"' >> /data/data/com.termux/files/usr/etc/bash.bashrc
    echo "Installation successful and PATH updated."
else
    echo "Installation failed."
fi
clear
echo "Now Termux is closing After 4 second..."
echo "Please Run Termux Again and Type 'uesave' "
sleep 5
pkill termux