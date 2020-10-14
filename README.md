# SousVide
This repository contains programs to create a user interface and control the Sous Vide hardware.

<hr>

The goal of this project was to build a functioning Sous Vide device that maintains a bath of water at a constant, user specified temperature for use in precison cooking. The SousVide.py program creates a user interface to a Proportional Integral Derivative (PID)/phaseangle controlled heating element. This hardware/software combinations allows a user to precisely control the temperature of a water bath.


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




## External Hardware

  
<table style="width:100%">
  <tr>
    <th> Part </th>
    <th> Description </th> 
    <th> Qty </th>
    <th> Source </th>
  </tr>
  <tr>
    <td> 2W 1.5k ohm resistor </td>
    <td> </td> 
    <td> 1 </td>
    <td> Mouser </td>
  </tr>
  <tr>
    <td> 2W 15k ohm resistor </td>
    <td> </td> 
    <td> 2 </td>
    <td> Mouser </td>
  </tr>
  <tr>
    <td> 2W 2.4k ohm resistor </td>
    <td> </td> 
    <td> 1 </td>
    <td> Mouser </td>
  </tr>
  <tr>
    <td> 2W 180 ohm resistor </td>
    <td> </td> 
    <td> 1 </td>
    <td> Mouser </td>
  </tr>
  <tr>
    <td> 1/4W 1k ohm resistor </td>
    <td> </td> 
    <td> 1 </td>
    <td> Santa Barbara Electronics </td>
  </tr>
  <tr>
    <td> 1/4W 220 ohm resistor </td>
    <td> </td> 
    <td> 1 </td>
    <td> Santa Barbara Electronics </td>
  </tr>
  <tr>
    <td> 0.01&#956F </td>
    <td> filtering capacitor </td> 
    <td> 1 </td>
    <td> Mouser </td>
  </tr>
  <tr>
    <td> H11AA1 </td>
    <td> zero cross detection optocoupler </td> 
    <td> 1 </td>
    <td> Mouser </td>
  </tr>
  <tr>
    <td> MOC3021 </td>
    <td> TRIAC firing optocoupler </td> 
    <td> 1 </td>
    <td> Mouser </td>
  </tr>
  <tr>
    <td> Q6015L5 </td>
    <td> 15A TRIAC </td> 
    <td> 1 </td>
    <td> Mouser </td>
  </tr>
  <tr>
    <td> 2N5551 </td>
    <td> NPN transistor </td> 
    <td> 1 </td>
    <td> Mouser </td>
  </tr>
  <tr>
    <td> 634-20ABPE </td>
    <td> TRIAC heat sink </td> 
    <td> 1 </td>
    <td> Mouser </td>
  </tr>
  <tr>
    <td> 709-IRM10-5 </td>
    <td> 5V 2A 10W power supply </td> 
    <td> 1 </td>
    <td> Mouser </td>
  </tr>
  <tr>
    <td> DS18B20 </td>
    <td> Temperature Sensor </td> 
    <td> 1 </td>
    <td> Adafruit </td>
  </tr>
  <tr>
    <td> Raspberry Pi Zero </td>
    <td> </td> 
    <td> 1 </td>
    <td> Adafruit </td>
  </tr>
  <tr>
    <td> Proto Bonnet </td>
    <td> </td> 
    <td> 1 </td>
    <td> Adafruit </td>
  </tr>
  <tr>
    <td> 12mm E Support button </td>
    <td> pack of 5 </td> 
    <td> 1 </td>
    <td> Amazon </td>
  </tr>
  <tr>
    <td> Tolako 5V Relay </td>
    <td> </td> 
    <td> 1 </td>
    <td> Amazon </td>
  </tr>
  <tr>
    <td> EWP3502HT6V </td>
    <td> high temp pump/food grade </td> 
    <td> 1 </td>
    <td> Amazon </td>
  </tr>
  <tr>
    <td> 1500W Heat Element </td>
    <td> </td> 
    <td> 1 </td>
    <td> Amazon </td>
  </tr>
  <tr>
    <td> 0.96 OLED 128x64 </td>
    <td> SSD1306 </td> 
    <td> 1 </td>
    <td> Amazon </td>
  </tr>
</table>
