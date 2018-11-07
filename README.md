# LinTo Hotword module
This project aims to provide a simple and efficient runner for hotword spotting.
It is designed to be part of the LinTo ecosystem.

## Getting Started
### Prerequisites
The module run on python3
```
sudo apt-get install python3 python3-pip
```

virtualenv ?
The module needs: 
* numpy is a C-based mathematical library.
* paho-mqtt is a lightweigh MQTT client for python.
* tenacity the retrying library for python to never give up. 
* precise-runner is a python wrapper designed by mycroft to run the inference engine

To build the module run the setup script
```

```
### Installation
To install the module go to the repository root and run 

```
sudo ./setup.sh
```
The script does several things:
* It downloads the inference engine from Mycroft project.
* It download our last hotword model
* It execute setup.py to install the module

## R
