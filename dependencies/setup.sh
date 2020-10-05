#!/bin/bash
sudo apt update -y && sudo apt upgrade -y
echo "Installing Dependencies - Please wait..." 

file2="prerequisites.txt"
while read line; do
# read each line - file2
sudo apt install $line
done < $file2

file1="dependencies.txt"
while read line; do
# read each line - file1
sudo apt install $line -y
done < $file1

dpkg -i ../src/code/dns-timing/debs/*

file3="requirements.txt"
while read line; do
# read each line - file3
sudo pip3 install $line
done < $file3