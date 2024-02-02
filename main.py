# Arducam port to Pico

from machine import Pin, SPI, reset



# Developing on 1.19
'''
#################### PINOUT ###############
Camera pin - Pico Pin
VCC - 3V3
GND - GND
SCK - GP18 - white
MISO - RX - GP16 - brown
MOSI - TX - GP19 - yellow
CS - GP17 - orange
'''

from utime import sleep_ms
import utime


import os
import ujson

import sdcard
from Camera import FileManager, Camera

def save_error_log(error_message):
    try:
        # Open a file in write mode
        with open('/error_log.txt', 'a') as file:
            # Write the error message along with a timestamp
            file.write(error_message + '\n')
        print('Error log saved successfully.')
    except Exception as e:
        print('Error saving error log:', e)


################################################################## CODE ACTUAL ##################################################################
DONE = Pin(22, Pin.OUT)
onboard_LED = Pin('LED', Pin.OUT)

try:

    spi = SPI(0,sck=Pin(18), miso=Pin(16), mosi=Pin(19), baudrate=8000000)
    cs = Pin(17, Pin.OUT)

    # SD card
    sleep_ms(1000) # Trying to fix 'no SD card error'
    spi_sd = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(8))
    cs_sd = Pin(0)
    sd = sdcard.SDCard(spi_sd, cs_sd)
    os.mount(sd, '/sd')

    onboard_LED.on()
    fm = FileManager()
    image_filename = fm.new_jpg_filename('/sd/image')
    print(image_filename)

    # button = Pin(15, Pin.IN,Pin.PULL_UP)


    cam = Camera(spi, cs)

    cam.resolution = '1280x720'
    # cam.set_filter(cam.SPECIAL_REVERSE)
    cam.set_brightness_level(cam.BRIGHTNESS_PLUS_4)
    cam.set_contrast(cam.CONTRAST_MINUS_3)



    cam.capture_jpg()
    sleep_ms(50)
    cam.saveJPG(image_filename)
    onboard_LED.off()
    sleep_ms(50)
    os.umount('/sd')
    sleep_ms(50)
    DONE.on()
except Exception as e:
    # Capture the exception and save the error log
    error_message = f'Exception: {type(e).__name__}, Message: {str(e)}'
    print(error_message)
    save_error_log(error_message)

