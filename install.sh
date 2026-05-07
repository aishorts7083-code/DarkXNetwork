#!/bin/bash

clear

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
# Bas pkg update rakha hai taaki error na aaye
pkg update -y 
pkg install python git curl -y
pip install requests rich colorama urllib3

echo -e "\e[1;36m[*] Downloading and Setting up DarkXNetwork...\e[0m"
rm -rf /data/data/com.termux/files/usr/share/darkxnetwork
git clone https://github.com/aishorts7083-code/DarkXNetwork.git /data/data/com.termux/files/usr/share/darkxnetwork

echo -e "\e[1;36m[*] Setting up the 'darkxnetwork' shortcut command...\e[0m"
echo '#!/bin/bash' > /data/data/com.termux/files/usr/bin/darkxnetwork
echo 'python /data/data/com.termux/files/usr/share/darkxnetwork/darkx.py' >> /data/data/com.termux/files/usr/bin/darkxnetwork

chmod +x /data/data/com.termux/files/usr/bin/darkxnetwork
chmod +x /data/data/com.termux/files/usr/share/darkxnetwork/darkx.py

echo -e "\e[1;32m[+] Installation Successful!\e[0m"
echo -e "\e[1;33m[!] Now you can open the tool anywhere in termux by typing:\e[0m"
echo -e "\e[1;31mdarkxnetwork\e[0m"
echo ""
