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


