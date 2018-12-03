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
    def __init__(self, config: configparser.ConfigParser, args):
        """Initialize audio provider, engines and MQTT message handling.

        Keyword arguments:
        conf -- Configuration file parameters
        """
        self.config = config['DEFAULT']
        assert 0.0 <= float(args.sensitivity) <= 1.0, "Sensitivity must be between 0.0 and 1.0"
        self.engine = PreciseEngine(args.engine_path, args.model_path)
        self.runner = PreciseRunner(self.engine, on_activation=self._on_activation, on_prediction=self._on_first_prediction, sensitivity=float(args.sensitivity))

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
    
    def _on_first_prediction(self, prob):
        self.broker.publish('hotword/ready', '{}')
        self.runner.on_prediction=lambda x:None

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)8s %(asctime)s [Spotter] %(message)s ")
    
    # Read default config from file
    config = configparser.ConfigParser()
    config.read(FILE_PATH + "config.conf")

    parser = argparse.ArgumentParser(description='Hotword module for LinTo.')
    parser.add_argument('model_path', help='MQTT broker port')
    parser.add_argument('--engine_path', dest='engine_path', default=config['DEFAULT']['engine_path'], help='Precise engine path')
    parser.add_argument('--sensitivity', '-s', dest='sensitivity', default=config['DEFAULT']['sensitivity'], type=float, help="Hotwork sensitivity [0.0-1.0]")
    args = parser.parse_args()
    if not os.path.isfile(args.engine_path):
        logging.error("Could not find engine at {}".format(args.engine_path))
        exit()
    runner = HotwordSpotter(config, args)
    runner.run()

if __name__ == '__main__':
    main()
