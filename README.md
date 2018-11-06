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

* numpy is a C-based mathematical library.
* paho-mqtt is a lightweigh MQTT client for python.
* tenacity the retrying library for python to never give up. 
* precise-runner is a python wrapper designed by mycroft to run the inference engine

```
sudo pip3 install numpy paho-mqtt tenacity precise-runner
```
### Dependencies
In order for the engine to run it needs two things:
- A inference engine as a compiled version of tensorflow matching the target architecture.
- A tensorflow frozen graph train to recognize the desired hotword

```
ARCH=armv7l or x86_64
rmdir precise-engine
wget $ARCH/precise-engine.tar
tar xvf precise-engine
rm precise-engine.tar
```

You can download our model for the HotWord LinTo or use your own. [Wiki](here)
```
cd model
wget model
```

## R
