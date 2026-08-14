#!/usr/bin/env bash

python3 -m pip install -r requirements.txt
sudo apt install jcal

file='./timeir.py'
name="$(basename "${file%.py}")"

cp -r $file ~/.local/bin/$name

clear
echo "installtion is done"