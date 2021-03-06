#!/bin/sh

# Installer Md VPN 
# CopyRight 2021 
# Author Mahan Esnaasharan 2021 

sudo rm -Rv /opt/mdVpn

sudo mkdir /opt/mdVpn

sudo cp -rv mdFiles.zip /opt/mdVpn

cd /opt/mdVpn 

sudo unzip  mdFiles.zip

sudo cp mdVpn.desktop /usr/share/applications/






