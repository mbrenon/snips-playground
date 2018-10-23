#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser

import subprocess
import time

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes

CONFIG_INI = "config.ini"
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


def acer_power():
    subprocess.call(["irsend", "send_once", "AcerBS312", "power"])


class IRController(object):
    """IR Controller."""

    def __init__(self):
        # get the configuration.
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except (IOError, ConfigParser.Error) as e:
            print e.message
            raise

        # start listening to MQTT.
        self.start_blocking()

    def turnOnTV_callback(self, hermes, intent_message):
        # Close session.
        hermes.publish_end_session(intent_message.session_id, "")

        # Send IR command.
        print "<turnOnTV>"
        acer_power()
        print "<turnOnTV/>"

    def turnOffTV_callback(self, hermes, intent_message):
        # Close session.
        hermes.publish_end_session(intent_message.session_id, "")

        # Send IR command.
        print "<turnOffTV>"
        acer_power()
        time.sleep(3)
        acer_power()
        print "<turnOffTV/>"

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self, hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == "mbrenon:turnOnTV":
            self.turnOnTV_callback(hermes, intent_message)
        elif coming_intent == "mbrenon:turnOffTV":
            self.turnOffTV_callback(hermes, intent_message)
        else:
            print "Unrecognized intent: " + coming_intent

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()


if __name__ == "__main__":
    IRController()
