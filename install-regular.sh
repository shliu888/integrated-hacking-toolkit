#!/bin/bash

sudo apt update
sudo apt install -y build-essential libssl-dev libpcap-dev pkg-config \
  libnl-3-dev libnl-genl-3-dev checkinstall git
sudo apt install -y aircrack-ng
sudo apt install -y crunch
sudo apt install -y dsniff
git clone https://github.com/Mebus/cupp.git
cd cupp
chmod +x cupp.py
sudo apt install java-wrapper
sudo apt install maltego
sudo apt install theharvester -y
sudo apt install recon-ng
sudo apt install whois
echo "Completed installing tools."

