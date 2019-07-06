# WebcAmbilight

This ambilight clone is meant to work with any TV source, since the screen data is gathered using a Logitech C920 webcam.

The software runs on Raspberry Pi. Tested on Raspberry Pi 3 Model B, Rasbian Stretch Lite.

Features:

* Detect your television from image (HDMI cable between TV and RasPi is required during the calibration phase)
* Save calibration data into file. Re-calibration is only needed if webcam or TV has been moved.
* Isolate TV from webcam stream (using the calibration data, which includes xy-coordinatess of corners.)
* Transfer the edge pixels' RGB data to WS2801 RGB LED strip.
* Optionally: Blur image
* Optionally: Blend frames over time. (_n_ frames before current frame)

The project is currently in progress.

_Note: sudo rights required_