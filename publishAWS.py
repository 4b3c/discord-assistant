# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a1uog9q54dyrxe-ats.iot.us-west-2.amazonaws.com"
CLIENT_ID = "discord_bot"
PATH_TO_CERTIFICATE = "Python_AWS_Keys/DeviceCertificatePython.crt"
PATH_TO_PRIVATE_KEY = "Python_AWS_Keys/PrivatePemKeyPython.key"
PATH_TO_AMAZON_ROOT_CA_1 = "Python_AWS_Keys/AmazonRootCA1Python.pem"
MESSAGE = "Itzza me, apizza"
TOPIC = "esp32/sub"
RANGE = 1


def send_esp_message(data):
    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
                endpoint=ENDPOINT,
                cert_filepath=PATH_TO_CERTIFICATE,
                pri_key_filepath=PATH_TO_PRIVATE_KEY,
                client_bootstrap=client_bootstrap,
                ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
                client_id=CLIENT_ID,
                clean_session=False,
                keep_alive_secs=6
                )

    # Make the connect() call
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    # Publish message to server desired number of times.
    print('Begin Publish')
    message = {"message" : data}
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    t.sleep(0.1)
    print('Publish End')

    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()