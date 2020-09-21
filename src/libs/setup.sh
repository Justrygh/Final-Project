#!/bin/bash
echo "Installing Dependencies - Please wait..." 
file1="dependencies.txt"
while read line; do
# read each line - file1
sudo apt install $line
done < $file1

file2="requirments.txt"
while read line; do
# read each line - file2
sudo pip3 install $line
done < $file2
