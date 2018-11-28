import AWSIoTPythonSDK
import getopt
import sys
import time
from classes import buildpoint

# Static Stuff
background_color_success = [ 255, 0, 0 ]    # RGB Green (Static)
background_color_failure = [ 0, 255, 0 ]    # RGB Red (Static)
background_color_build = [ 0, 0, 255 ]      # RGB Blue (Static)
foreground_color_point = [ 255, 255, 255 ]  # RGB White (Static)
foreground_color_red = [ 255, 0, 0 ]        # RGB Green (Static)
foreground_color_green = [ 0, 255, 0 ]      # RGB Red (Static)
max_leds = 100

# This changes during programming execution
background_color_active = background_color_build # This changes
builds = []
waiting = 1 # 0 = builds running, 1 + 2 = used to generate "waiting" pattern, 3 = don't show build points


"""
This generates one frame of waiting colours
returns { 1:[R,G,B], 2:[R,G,B], ..., max:[R,G,B] }
"""
def waiting_pattern():
    global waiting

    led_strip = {}
    start = waiting
    for i in range(0, max_leds):
        led_color = foreground_color_green if start == 1 else foreground_color_red
        led_strip[i] = led_color
        start = 2 if start == 1 else 1

    if waiting in (1,2):
        waiting = 2 if waiting == 1 else 1

    return led_strip

"""
This generates one frame of build pattern
returns { 1:[R,G,B], 2:[R,G,B], ..., max:[R,G,B] }
"""
def build_pattern():
    led_strip = {}
    for i in range(0, max_leds):
        led_strip[i] = background_color_active
    
    if waiting != 3:
        for build in builds:
            led_strip[build.getAndSetNextPoint(max_leds)] = foreground_color_point
    
    return led_strip

"""
This sets the LEDS on the strip
"""
def set_leds(toValues):
    #TODO: Import Raspberry Pi library and do stuff
    return

"""
This prints the commandline usage statement
"""
def print_usage():
    print("Usage: python3 main.py --clientid=<client id> --endpoint=<aws endpoint> --cacert=<path to ca cert> --privatekey=<path to private key> --cert=<path to cert>")
    print("       -i  --clientid     The ClientID of this node in AWS IoT")
    print("       -e  --endpoint     The AWS IoT endpoint url")
    print("       -a  --cacert       The path to the AWS IoT CA Cert")
    print("       -p  --privatekey   The path to the AWS IoT Private Key for this thing")
    print("       -c  --cert         The path to the AWS IoT Cert for this thing")

def main(clientid, endpoint, cacertpath, privatekeypath, certpath):
    # Create the AWS IoT Connection

    # Setup Listeners
    
    
    # Start wait screen
    while(True):
        if (waiting > 0):
            set_leds(waiting_pattern())
        else:
            set_leds(build_pattern())
        
        time.sleep(0.1)
    return

# Entry Point
if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:e:a:p:c:", [ "help", "clientid=", "endpoint=", "cacert=", "privatekey=", "cert=" ])
    except getopt.GetoptError as err:
        print(err)
        print_usage()
        sys.exit(2)

    clientid = None 
    endpoint = None
    cacertpath = None
    privatekeypath = None
    certpath = None

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
        else:
            assert False, "Unhandled Option"
    
    if None in (clientid, endpoint, cacertpath, privatekeypath, certpath):
        print("Error: Missing argument")
        print_usage()
        sys.exit(2)

    main(clientid, endpoint, cacertpath, privatekeypath, certpath)