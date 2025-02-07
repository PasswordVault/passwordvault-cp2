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
import gc
import terminalio

from adafruit_display_text import bitmap_label
#from adafruit_display_text.scrolling_label import ScrollingLabel
from adafruit_display_shapes import line, rect

SCK = board.GP10
MOSI = board.GP11
CS = board.GP9
DC = board.GP8
RESET = board.GP12
BL = board.GP13

class Display(ST7735R):
    BLACK  = 0x000000
    GRAY   = 0x808080
    WHITE  = 0xFFFFFF
    GBLUE  = 0x00FFFF
    GREEN  = 0x00FF00
    YELLOW = 0xFFFF00
    def __init__(self):
        displayio.release_displays()
        spi = busio.SPI(SCK, MOSI)
        self.bl = digitalio.DigitalInOut(BL)
        self.bl.direction = digitalio.Direction.OUTPUT
        self.bl.value = False
        display_bus = fourwire.FourWire(spi, command=DC, chip_select=CS, reset=RESET)
        super().__init__(display_bus,
                          width=128, height=128,
                          colstart=2, rowstart=3,
                          rotation=270)
        self.bl.value = True

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
        #print("clear")
        #self.bl.value = False
        self.root_group = None
        gc.collect()
        splash = displayio.Group()
        self.root_group = splash

    def text(self, txt, x,y, color, background_color):
        lbl = bitmap_label.Label(terminalio.FONT, text=txt, color=color, background_color=background_color, x=x, y=y, anchor_point=(0,0), save_text=False)
        self.root_group.append(lbl)

    def hline(self, x,y, w, color):
        ln = line.Line(x0=x, y0=y, x1=w, y1=y, color=color)
        self.root_group.append(ln)

    def fill_rect(self, x,y, w,h, color):
        r = rect.Rect(x=x, y=y, width=w, height=h, fill=color, outline=color)
        self.root_group.append(r)

    def show(self):
        #print("show")
        #self.bl.value = True
        pass

