#!/data/data/com.termux/files/usr/bin/bash
set -e

pkg update -y
pkg install -y git

cd ~
rm -rf rootfaker-termux
git clone https://github.com/Rick000000007/rootfaker-termux
cd rootfaker-termux
bash install.sh
