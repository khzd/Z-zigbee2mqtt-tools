#!/usr/bin/env python3
"""a simple device data generator that sends to an MQTT broker via paho"""
import sys
import yaml
from yaml import load, dump
import paho.mqtt.client as mqtt

def zgene(host, port, username, password, topic, devices, verbose):
    """generate data and send it to an MQTT broker"""
    topic = topic + "/bridge/config/ban"
    mqttc = mqtt.Client()

    if username:
        mqttc.username_pw_set(username, password)

    mqttc.connect(host, port)
    devices = list(devices.keys())
    i = 0
    while i < len(devices):
        data = { devices[i] }
        payload = devices[i]
        if verbose:
            print("%s , %s" % (topic, payload))
        mqttc.publish(topic, payload)
        i += 1

def main(config_path, topic):
    """main entry point, load and validate config and call generate"""
    try:
        with open(config_path) as handle:
            config = yaml.load(handle)
            mqtt_config = config.get("mqtt", {})
            devices = config.get("devices")
            if not devices:
                print("no devices specified in config, nothing to do")
                return

            host = mqtt_config.get("host", "localhost")
            port = mqtt_config.get("port", 1883)
            username = mqtt_config.get("username")
            password = mqtt_config.get("password")

            data = yaml.dump( config )
            """print ("config file %s " % yaml.dump(data))"""
            zgene(host, port, username, password, topic, devices,  True)
    except IOError as error:
        print("Error opening config file '%s'" % config_path, error)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("usage %s config.yaml 'topic of the network to ban in'" % sys.argv[0])
