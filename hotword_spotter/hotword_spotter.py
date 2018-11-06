#!/usr/bin/env python3
import time

from precise_runner import PreciseEngine, PreciseRunner

import os
import sys
import time
import datetime

import argparse
import json
import configparser
import logging
import paho.mqtt.client as mqtt
import tenacity


FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
class HotwordSpotter:
    def __init__(self, config: configparser.ConfigParser):
        """Initialize audio provider, engines and MQTT message handling.

        Keyword arguments:
        conf -- Configuration file parameters
        """
        self.config = config['PARAMS']
        self.engine = PreciseEngine(FILE_PATH + 'precise-engine/precise-engine', FILE_PATH + self.config['model_path'])
        self.runner = PreciseRunner(self.engine, on_activation=self._on_activation)

        #MQTT broker client
        self.broker = self._broker_connect()
            
    def run(self):
        """Run the wuw spotter and its threads until broker is disconnected."""
        self.engine.start()
        self.runner.start()
        try:
            self.broker.loop_forever()
        except KeyboardInterrupt:
            logging.info("Process interrupted by user")

        logging.info("WuW spotter is off.")

    @tenacity.retry(wait=tenacity.wait_random(min=1, max=10),
                retry=tenacity.retry_if_result(lambda s: s is None),
                retry_error_callback=(lambda s: s.result())
                )
    def _broker_connect(self):
        """Tries to connect to MQTT broker until it succeeds"""
        logging.info("Attempting connexion to broker at {}:{}".format(self.config['broker_ip'], self.config['broker_port']))
        try:
            broker = mqtt.Client()
            broker.on_connect = self._on_broker_connect
            broker.connect(self.config['broker_ip'], int(self.config['broker_port']), 0)
            return broker
        except:
            logging.warning("Failed to connect to broker (Auto-retry)")
            return None

    def _on_broker_connect(self, client, userdata, flags, rc):
        logging.info("Succefully connected to broker")

    def _on_activation(self):
        msg = dict()
        msg['on'] =  datetime.datetime.now().isoformat()
        msg['value'] = self.config['wuw_pub_value']
        payload = json.dumps(msg)
        self.broker.publish(self.config['wuw_pub_topic'], payload)
        logging.debug("Published message '{}' on topic {}".format(msg, payload))

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)8s %(asctime)s [Spotter] %(message)s ")

    # Read default config from file
    config = configparser.ConfigParser()
    print(FILE_PATH + "config.conf")
    config.read(FILE_PATH + "config.conf")
    runner = HotwordSpotter(config)
    runner.run()

if __name__ == '__main__':
    main()
