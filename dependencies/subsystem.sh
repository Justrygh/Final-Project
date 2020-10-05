#!/bin/bash
file1="dependencies.txt"
while read line;
do
sudo apt install $line -y
done < $file1