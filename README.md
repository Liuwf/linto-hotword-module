# LinTo Hotword module
This project aims to provide a simple and efficient runner for hotword spotting.
It is designed to be part of the LinTo ecosystem.

## Getting Started

### Installation
To install the module go to the repository root and run 
```
sudo ./setup.sh
```
It should work on both x86_64 and armv7l

The script does several things:
* It looks for python3 and python3-pip.
* It downloads the inference engine from Mycroft project.
* It download our last hotword model.
* It execute pip install using setup.py to install the module.

## Usage
To launch the module simply use the bin created during the setup:
```shell
linto_hotword model_path.pb
```
The spotter will send a message on the local MQTT broker each time the hotword is spotted.
Topics and MQTT parameter cannot be changed after instalation for now (On it !)

## References
TODO
