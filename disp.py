'''
Use a Waveshare Pico-LCD-1.44
@see https://www.waveshare.com/wiki/Pico-LCD-1.44
'''
from adafruit_bus_device.spi_device import SPIDevice
from adafruit_st7735r import ST7735R
import board
import busio
import digitalio
import displayio
import fourwire
import terminalio

from adafruit_display_text import label
#from adafruit_display_text.scrolling_label import ScrollingLabel

SCK = board.GP10
MOSI = board.GP11
CS = board.GP9
DC = board.GP8
RESET = board.GP12
BL = board.GP13

class Display(ST7735R):
    def __init__(self):
        displayio.release_displays()
        spi = busio.SPI(SCK, MOSI)
        bl = digitalio.DigitalInOut(BL)
        bl.direction = digitalio.Direction.OUTPUT
        bl.value = True
        display_bus = fourwire.FourWire(spi, command=DC, chip_select=CS, reset=RESET)
        super().__init__(display_bus,
                          width=128, height=128,
                          colstart=2, rowstart=3,
                          rotation=270)

    def config_buttons(self):
        self.pins = [
            digitalio.DigitalInOut(board.GP15), 
            digitalio.DigitalInOut(board.GP17), 
            digitalio.DigitalInOut(board.GP2), 
            digitalio.DigitalInOut(board.GP3)
        ]
        for pin in self.pins:
            pin.switch_to_input(digitalio.Pull.UP)
        return len(self.pins)

    def button(self, i):
        #print(i, self.pins[i].value)
        return self.pins[i].value
    
    def clear(self):
        self.root_group = None

    def example(self):
        # Make the display context
        splash = displayio.Group()
        self.root_group = splash

        color_bitmap = displayio.Bitmap(128, 128, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0x00FF00  # Bright Green

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(bg_sprite)

        # Draw a smaller inner rectangle
        inner1_bitmap = displayio.Bitmap(126, 126, 1)
        inner1_palette = displayio.Palette(1)
        inner1_palette[0] = 0xFF0000  # Red
        inner1_sprite = displayio.TileGrid(inner1_bitmap, pixel_shader=inner1_palette, x=1, y=1)
        splash.append(inner1_sprite)

        # Draw a smaller inner rectangle
        inner2_bitmap = displayio.Bitmap(108, 108, 1)
        inner2_palette = displayio.Palette(1)
        inner2_palette[0] = 0xAA0088  # Purple
        inner2_sprite = displayio.TileGrid(inner2_bitmap, pixel_shader=inner2_palette, x=10, y=10)
        splash.append(inner2_sprite)

        # Draw a label
        text = "Hallo Welt!"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=30, y=64)
        splash.append(text_area)
        #text = "Hallo Welt. Ich bin ein sehr langer Text mit Ümläuten ;)"
        #label = ScrollingLabel(
        #    terminalio.FONT, text=text, max_characters=18, animate_time=0.3
        #)
        #label.x = 10
        #label.y = 64
        #splash.append(label)

        #while True:
        #    label.update()


