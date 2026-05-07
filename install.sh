#!/bin/bash

# Clear screen
clear

# Red DARKX ASCII Art for authentication feel
echo -e "\e[1;31m
██████╗  █████╗ ██████╗ ██╗  ██╗██╗  ██╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝╚██╗██╔╝
██║  ██║███████║██████╔╝█████╔╝  ╚███╔╝ 
██║  ██║██╔══██║██╔══██╗██╔═██╗  ██╔██╗ 
██████╔╝██║  ██║██║  ██║██║  ██╗██╔╝ ██╗
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
             N E T W O R K
\e[0m"

echo -e "\e[1;36m[*] Installing Required Packages...\e[0m"
pkg update -y && pkg upgrade -y
pkg install python -y
pip install requests rich colorama urllib3

echo -e "\e[1;36m[*] Setting up the 'darkxnetwork' shortcut command...\e[0m"

# Creating a hidden directory for the tool
mkdir -p /data/data/com.termux/files/usr/share/darkxnetwork

# Copying the python script to the safe location
cp darkx.py /data/data/com.termux/files/usr/share/darkxnetwork/

# Creating the bash executable command
echo '#!/bin/bash' > /data/data/com.termux/files/usr/bin/darkxnetwork
echo 'python /data/data/com.termux/files/usr/share/darkxnetwork/darkx.py' >> /data/data/com.termux/files/usr/bin/darkxnetwork

# Giving execution permission
chmod +x /data/data/com.termux/files/usr/bin/darkxnetwork
chmod +x /data/data/com.termux/files/usr/share/darkxnetwork/darkx.py

echo -e "\e[1;32m[+] Installation Successful!\e[0m"
echo -e "\e[1;33m[!] Now you can open the tool anywhere in termux by typing:\e[0m"
echo -e "\e[1;31mdarkxnetwork\e[0m"
echo ""
