# Webcambilight

This ambilight clone is meant to work with any TV source, since the screen data is gathered using a Logitech C920 webcam.

The software runs on Raspberry Pi. Tested on Raspberry Pi 3 Model B, Rasbian Stretch Lite.

Features:

* Detect your television from image (HDMI cable between TV and RasPi is required during the calibration phase)
* Save calibration data into file. Re-calibration is only needed if webcam or TV has been moved.
* Isolate TV from webcam stream (using the calibration data, which includes xy-coordinatess of corners.)
* Transfer the edge pixels' RGB data to WS2801 RGB LED strip.
* Optionally: Blur image
* Optionally: Blend frames over time. (_n_ frames before current frame)

Usage:

* Plug in the power cord. The service starts automatically after the os loads.
* Pressing blue button (GPIO BMC 5) will launch calibration.
* Pressing red button (GPIO BMC 6) will save calibration data and shutdown os.
* After waiting for os to shutdown, you can pull the plug.

For further information, check this document: https://sway.office.com/tqb611MrFPdCkPQu

The link has pretty pictures too.

_Note: sudo rights required (reason: PyGame)_

## Installation

For installing the WS2801 LED strip, check the Sway document above.

### OpenCV

For installing OpenCV on Raspberry, check this guide by Adrian Rosebrock: https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/

I was running OpenCV 4.1.0 while writing the code. Python version 3.5.

### 

### Python Libraries

After you have Git Cloned this project, run:

```
pip install -r requirements.txt
```

If PyGame gives you any errors, you might have to install some missing dependencies. I needed these:

```
sudo apt-get install libsdl1.2-dev libportmidi-dev \
libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev \
libsmpeg-dev 
```

### SPI

In order to use the hardware SPI controller, you must enable it. Type:

```
sudo raspi-config
```

...and find the setting from Interfacing Options. Enable it. After a reboot, /dev/spidev0.0/ will exist on your system.


### HDMI settings

If you boot RasPi without HDMI being plugged in, you might run into problems with HDMI resolution. Thus, it is a good idea to edit /boot/config.txt (with sudo):


The config below will force 1080p60 mode without overscan. If your TV doesn't support this, or you are unsure about it, check the EDID data using this guide before proceeding: https://www.opentechguides.com/how-to/article/raspberry-pi/28/raspi-display-setting.html

Find these lines, uncomment them and check that the values are what they need to be.

```
hdmi_force_hotplug=1
disable_overscan=1
hdmi_group=1
hdmi_mode=16

```

### Systemd service

Edit the webcambilight.service file to match your needs. For guidance, check: https://www.raspberrypi.org/documentation/linux/usage/systemd.md

Check that ...

* the WorkingDirectory matches to where webcambilight.py is
* the path to python interpreter is correct. I used a virtualenvironment so the path is most likely different than yours.

Test the webcambilight by launching it as 'sudo'. It it works, copy the file to correct directory and activate the service.

```
sudo cp webcambilight.service /etc/systemd/system/webcambilight.service
sudo systemctl enable webcambilight
```
