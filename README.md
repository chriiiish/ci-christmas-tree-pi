ci-christmas-tree-pi
====================
This project is designed to be run on a Raspberry Pi (Zero W) with a strip of NeoPixels attached.
This connects to AWS IoT to receive commands

---

Hardware
========

Minimum Hardware (based on what I'm using):
* Raspberry Pi (Zero W)
* Neopixel LED strip (5V)

If you've got a lot of LEDs ( < 8 LEDs ):
* a 5V 3A+ Power Supply

---

Installation
============
To install this on a raspberry pi, clone the repository into a folder of your choosing, here we're going to clone it into the documents:
```bash
cd /home/pi/Documents/
git clone https://github.com/chriiiish/ci-christmas-tree-pi
```

Then install the dependencies:

```bash
cd /home/pi/Documents/ci-christmas-tree-pi
sudo pip3 install -r requirements.txt
```

Then install the service:

```bash
cd /home/pi/Documents/ci-christmas-tree-pi

sudo chmod u+x install_service.sh
sudo cp run_example.sh run.sh
sudo chmod u+x run.sh

sudo ./install_service.sh
```

---

Configuration
=============
In order to run this you need to download the certificates and keys from AWS IoT. [See here](https://docs.aws.amazon.com/iot/latest/developerguide/iot-sdk-setup.html) for how to setup this as a device in AWS IoT.

In this example, we have downloaded all the certificates to `/home/pi/Documents/private/`. You'll need:

* Amazon IoT Root CA certificate (e.g. AmazonRootCA1.pem)
* Your Thing Certificate (e.g. 829a92e-certificate.pem.crt)
* Your Thing Private Key (e.g. 829a92e-private.pem.key)
* Your IoT Topic that you're listening on (e.g. mytree)
* Your AWS IoT endpoint (e.g. asdajsdlasoq-ats.iot.us-east-1.amazonaws.com)

Copy the run_example.sh file to run.sh and make it executable

```bash
cd /home/pi/Documents/ci-christmas-tree-pi
cp run_example.sh run.sh
sudo chmod u+x run.sh
```

Now go through the run.sh file and change the parameters to the ones you need. In the end you should have a file that looks like this:

```
# Wait for DNS to come up
sleep 30s

# Run the Christmas Tree
python3 /home/pi/Documents/ci-christmas-tree-pi/main.py --clientid=pi001 --endpoint=myendpoint-ats.iot.ap-southeast-2.amazonaws.com --cacert=/home/pi/Documents/private/AmazonRootCA1.pem --privatekey=/home/pi/Documents/private/deviceid-private.pem.key --cert=/home/pi/Documents/private/deviceid-certificate.pem.crt --topic=mytree
```

At this point we can go and install the service, which is what we will use to control the tree

```bash
cd /home/pi/Documents/ci-christmas-tree-pi
sudo chmod u+x install_service.sh
sudo ./install_service.sh /home/pi/Documents/ci-christmas-tree-pi
```

---

Run
===

To run the project, use the service:
```bash
sudo systemctl start ci-christmas-tree
sudo systemctl restart ci-christmas-tree
sudo systemctl stop ci-christmas-tree
```

**IMPORTANT**: when turning on the raspberry pi, make sure the LED strip is **disconnected** before powering on the board. As soon as the power's in, you can connect the strip.

---

Raspberry Pi Configuration
==========================

Connect the LED strip to GPIO18 as seen here: [(more info)](https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring)

![Raspberry Pi Wiring Diagram](https://cdn-learn.adafruit.com/assets/assets/000/063/928/original/led_strips_raspi_NeoPixel_powered_bb.jpg "Raspberry Pi Wiring Diagram")