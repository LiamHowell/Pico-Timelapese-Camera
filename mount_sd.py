from machine import SPI, Pin
import sdcard, uos

'''
MISO - RX
MOSI - TX
'''

spi_sd = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(8))
cs_sd = Pin(0)
sd = sdcard.SDCard(spi_sd, cs_sd)
uos.mount(sd, '/sd')