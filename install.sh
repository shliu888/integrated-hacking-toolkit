#!/bin/bash

git clone https://github.com/Mebus/cupp.git
cd cupp
chmod +x cupp.py
sudo apt update
sudo apt install theharvester -y
sudo apt install recon-ng -y
sudo apt install whois -y
sudo apt install -y build-essential libssl-dev libpcap-dev pkg-config \
libnl-3-dev libnl-genl-3-dev checkinstall git
sudo apt install java-wrapper
chmod +x hackingtoolkit
sudo mv hackingtoolkit /usr/local/bin
echo "Installation complete."
