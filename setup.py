#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="linto_hotword",
    version="0.2.0",
    include_package_data=True,
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['linto_hotword=hotword_spotter.hotword_spotter:main'],
    },
    install_requires=[
        'precise-runner',
        'tenacity',
        'pyalsaaudio',
        'paho-mqtt'
    ],
    author="Rudy Baraglia",
    author_email="baraglia.rudy@gmail.com",
    description="linto_hotword is the hotword spotter for the LinTo device",
    license="AGPL V3",
    keywords="wakeword hotword",
    url="",
    project_urls={
        "github" : ""
    },
    long_description="Refer to README"

)