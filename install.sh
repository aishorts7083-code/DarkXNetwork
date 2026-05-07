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
pkg update -y 
pkg install python git curl -y
pip install requests rich colorama urllib3

echo -e "\e[1;36m[*] Downloading DarkXNetwork...\e[0m"
# Purana folder delete karke naya download karega
rm -rf /data/data/com.termux/files/usr/share/darkxnetwork
git clone https://github.com/aishorts7083-code/DarkXNetwork.git /data/data/com.termux/files/usr/share/darkxnetwork

echo -e "\e[1;36m[*] Setting up the shortcut command...\e[0m"

# SMART DETECT: Ye line aapki 'Darkxnetwork.py' ko khud dhoondh legi
PY_FILE=$(ls /data/data/com.termux/files/usr/share/darkxnetwork/*.py 2>/dev/null | head -n 1)

if [ -z "$PY_FILE" ]; then
    echo -e "\e[1;31m[!] Error: GitHub repo mein .py file nahi mili!\e[0m"
    exit 1
fi

echo '#!/bin/bash' > /data/data/com.termux/files/usr/bin/darkxnetwork
echo "python $PY_FILE" >> /data/data/com.termux/files/usr/bin/darkxnetwork

chmod +x /data/data/com.termux/files/usr/bin/darkxnetwork
chmod +x "$PY_FILE"

echo -e "\e[1;32m[+] Installation Successful!\e[0m"
echo -e "\e[1;33m[!] Type 'darkxnetwork' to start.\e[0m"
