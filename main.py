import AWSIoTPythonSDK
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import board
import neopixel
import getopt
import json
import sys
import time

# Static Stuff
colors = {}
colors["succeed"] = (0,255,0) # RGB
colors["fail"] = (255,0,0) # RGB
colors["pattern_primary"] = (255,0,0) # RGB
colors["pattern_secondary"] = (0,255,0) # RGB
num_leds = 100
alternate_every = 4
frame_rate = 0.05 # seconds per frame
hold_time = 1 # seconds

# This changes during programming execution
internal_leds = []
builds = []
mqttClient=None
notification = {
    "count": 0,
    "color": (0,0,0)
}
pixels = None


"""
This sets the LEDS on the strip
"""
def set_leds(toValues):
    global pixels
    for led_number in range(0, len(internal_leds)):
        pixels[led_number] = internal_leds[led_number]
    pixels.show()

"""
This sets all the LEDs to a particular color
"""
def set_leds_notification(color):
    global pixels
    pixels.fill(color)
    pixels.show()

"""
This sets up the connection to AWS IoT
"""
def setup_iot_connection(clientid, endpoint, cacertpath, privatekeypath, certpath, topic):
    global mqttClient
    mqttClient = AWSIoTMQTTClient(clientid)
    mqttClient.configureEndpoint(endpoint, 8883)
    mqttClient.configureCredentials(cacertpath, privatekeypath, certpath)

    mqttClient.configureOfflinePublishQueueing(-1)
    mqttClient.configureDrainingFrequency(2)
    mqttClient.configureConnectDisconnectTimeout(10)
    mqttClient.configureMQTTOperationTimeout(5)

    mqttClient.connect()
    mqttClient.subscribe(topic, 1, mqtt_receive)

"""
Receives a packet from MQTT and processes it accordingly
"""
def mqtt_receive(client, userdata, message):
    print("Received Message")
    try:
        payload = json.loads(str(message.payload))
        build_id = payload["buildId"]
        status = payload["status"]
    except Exception as err:
        print("Error Receiving Message: {0} {1}".format(err, err.with_traceback))

    functions = {
        0: process_reset,
        1: process_create,
        2: process_succeed,
        3: process_fail
    }

    functions[status](str(build_id))

"""
Clears the Build List, Reset LED strip to waiting
"""
def process_reset(build_id):
    global builds, notification
    print("Processing Reset")
    builds.clear()
    notification["color"] = (0,0,0)
    notification["count"] = 0

"""
Adds a build to the LED strip
"""
def process_create(build_id):
    global builds
    print("Processing Create ({0})".format(build_id))
    builds.append(build_id)

"""
Removes a build from the list, sets success pattern
"""
def process_succeed(build_id):
    global builds, notification
    print("Processing Succeed ({0})".format(build_id))
    if build_id in builds:
        builds.remove(build_id)
    notification["color"] = colors["succeed"]
    notification["count"] = hold_time / frame_rate

"""
Removes a build from the list, sets the failure pattern
"""
def process_fail(build_id):
    global builds, notification
    print("Processing Fail ({0})".format(build_id))
    if build_id in builds:
        builds.remove()
    notification["color"] = colors["fail"]
    notification["count"] = hold_time / frame_rate

"""
This prints the commandline usage statement
"""
def print_usage():
    print("Usage: python3 main.py --clientid=<client id> --endpoint=<aws endpoint> --cacert=<path to ca cert> --privatekey=<path to private key> --cert=<path to cert> --topic=<mqtt topic>")
    print("       -i  --clientid     The ClientID of this node in AWS IoT")
    print("       -e  --endpoint     The AWS IoT endpoint url")
    print("       -a  --cacert       The path to the AWS IoT CA Cert")
    print("       -p  --privatekey   The path to the AWS IoT Private Key for this thing")
    print("       -c  --cert         The path to the AWS IoT Cert for this thing")
    print("       -t  --topic        The MQTT topic to listen for commands on")

def main(clientid, endpoint, cacertpath, privatekeypath, certpath, topic):
    global internal_leds, notification, pixels

    # Create the AWS IoT Connection
    print("Setting up IoT connection...")
    setup_iot_connection(clientid, endpoint, cacertpath, privatekeypath, certpath, topic)
    print("IoT Connection Setup Complete.")

    # Setup NeoPixels
    pixels = neopixel.NeoPixel(board.D18, num_leds, brightness=0.2, auto_write=False)

    # Create the LED pattern
    for led_block in range(0, int(num_leds/alternate_every)):
        for led in range(0, alternate_every):
            internal_leds.append( colors["pattern_primary"] if led_block % 2 == 0 else colors["pattern_secondary"] )

    # Start wait screen
    try:
        while(True):
            if notification["count"] > 0:
                print("notification {0} {1}".format(notification["color"], notification["count"]) )
                set_leds_notification(notification["color"])
                notification["count"] -= 1
            else:
                set_leds(internal_leds)
                if len(builds) > 0:
                    print("builds active: {0}".format(len(builds)))
                    start_led = internal_leds.pop(0)
                    internal_leds.append(start_led)

            time.sleep(frame_rate)
    except KeyboardInterrupt:
        mqttClient.disconnect()
    return

# Entry Point
if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:e:a:p:c:t:", [ "help", "clientid=", "endpoint=", "cacert=", "privatekey=", "cert=", "topic=" ])
    except getopt.GetoptError as err:
        print(err)
        print_usage()
        sys.exit(2)

    clientid = None 
    endpoint = None
    cacertpath = None
    privatekeypath = None
    certpath = None
    topic = None

    for key, value in opts:
        if key in ("-i", "--clientid"):
            clientid = value
        elif key in ("-e", "--endpoint"):
            endpoint = value
        elif key in ("-a", "--cacert"):
            cacertpath = value
        elif key in ("-p", "--privatekey"):
            privatekeypath = value
        elif key in ("-c", "--cert"):
            certpath = value
        elif key in ("-h", "--help"):
            print_usage()
            sys.exit(0)
        elif key in ("-t", "--topic"):
            topic = value
        else:
            assert False, "Unhandled Option"
    
    if None in (clientid, endpoint, cacertpath, privatekeypath, certpath):
        print("Error: Missing argument")
        print_usage()
        sys.exit(2)

    main(clientid, endpoint, cacertpath, privatekeypath, certpath, topic)