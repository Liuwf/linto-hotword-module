#!/bin/bash

ROOT=$PWD
ARCH=$(uname -m)
if [ $ARCH != "armv7l" ] && [ $ARCH != "x86_64" ]
    then
    echo "Invalid architecture $ARCH. Please contact maintener"
    exit
fi
echo "Setup for $ARCH"
echo "Move into hotword_spotter/"
cd hotword_spotter/
tar_name="precise-engine_0.2.0_$ARCH.tar.gz"
engine_link="https://github.com/MycroftAI/mycroft-precise/releases/download/v0.2.0/$tar_name"
echo "Downloading Mycroft precise-engine"
wget $engine_link
if [ -d 'precise-engine' ] 
    then
        echo "rmdir on placeholder folder precise-engine"
        rm -Rf precise-engine
    fi
echo "Extracting archive"
tar -zxvf $tar_name
echo "Removing archive"
rm $tar_name

echo "Downloading last model"
cd $ROOT/hotword_spotter/model/
wget "https://github.com/linto-ai/linto-models/raw/master/hotword-model/linto_64.zip"
unzip "linto_64.zip" -d .
rm "linto_64.zip"

echo "Installing dependencies"
sudo apt-get install python3 python3-pip 

echo "Running setup.py"
cd $ROOT
sudo pip3 install .