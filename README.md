# SousVide
This repository contains programs to create a user interface and control the Sous Vide hardware.

<hr>

The goal of this project was to build a functioning Sous Vide device that maintains a bath of water at a constant, user specified temperature for use in precison cooking. The SousVide.py program creates a user interface to a Proportional Integral Derivative (PID)/phaseangle controlled heating element. This hardware/software combinations allows a user to precisely control the temperature of a water bath.

For a more thorough description, see the [final project report](SousVide_ProjectReport.pdf).


## Software
Necessary software for the SousVide.py program includes the RPi.GPIO module, the w1thermsensor module,the Adafruit Python SSD1306 library, the Python PID module, the Python Imaging Library, and the NumPylibrary.  This software must be installed for the program to operate.

The RPi.GPIO module is installed by default in Raspbian.  To make sure that it is at the latest version:
<pre><code> sudo apt-get update
 sudo apt-get install python-rpi.gpio python3-rpi.gpio
</code></pre>

To install the w1thermsensor module:
<pre><code> sudo apt-get install python3-w1thermsensor
</code></pre>

To install the Adafruit Python SSD1306 library:
<pre><code> git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
 cd Adafruit_Python_SSD1306
 sudo python setup.py install
</code></pre>

To install the Python PID module:
<pre><code> git clone git://github.com/sandves/pid.git
</code></pre>

<b> Note: After download, the file containing the PID module must be placed in the same directory as the main program. </b>

To install the Python Imaging Library (PIL):
<pre><code> sudo apt-get install python-imaging
</code></pre>

To install NumPy:
<pre><code> python -m pip install --user numpy
</code></pre>

