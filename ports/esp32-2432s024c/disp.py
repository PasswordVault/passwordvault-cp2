'''
Use a Waveshare Pico-LCD-1.44
@see https://www.waveshare.com/wiki/Pico-LCD-1.44
'''
import board
import cst820
import digitalio
import displayio
import gc
import terminalio

from adafruit_display_text import bitmap_label
#from adafruit_display_text.scrolling_label import ScrollingLabel
from adafruit_display_shapes import line, rect

BL = board.LCD_BCKL

class Display():
    BLACK  = 0x000000
    GRAY   = 0x808080
    WHITE  = 0xFFFFFF
    GBLUE  = 0x00FFFF
    GREEN  = 0x00FF00
    YELLOW = 0xFFFF00

    def __init__(self):
        self.ctp = cst820.CST820()
        self.e = cst820.EVENTS

    def config_buttons(self):
        return 0

    @property
    def width(self):
        return board.DISPLAY.width

    @property
    def height(self):
        return board.DISPLAY.height

    @property
    def touched(self):
        return self.ctp.touched

    @property
    def touches(self):
        return self.ctp.touches

    @property
    def events(self):
        return self.e

    def button(self, i):
        #print(i, self.pins[i].value)
        return self.pins[i].value

    def clear(self):
        #print("clear")
        #self.bl.value = False
        board.DISPLAY.root_group = None
        gc.collect()
        splash = displayio.Group()
        board.DISPLAY.root_group = splash

    def text(self, txt, x,y, color, background_color):
        lbl = bitmap_label.Label(terminalio.FONT, text=txt, scale=2, color=color, background_color=background_color, x=x, y=y, anchor_point=(0,0), save_text=False)
        board.DISPLAY.root_group.append(lbl)
        return lbl

    def hline(self, x,y, w, color):
        ln = line.Line(x0=x, y0=y, x1=w, y1=y, color=color)
        board.DISPLAY.root_group.append(ln)
        return ln

    def fill_rect(self, x,y, w,h, color):
        r = rect.Rect(x=x, y=y, width=w, height=h, fill=color, outline=color)
        board.DISPLAY.root_group.append(r)
        return r

    def rect(self, x,y, w,h, color):
        r = rect.Rect(x=x, y=y, width=w, height=h, outline=color)
        board.DISPLAY.root_group.append(r)
        return r

    def pop(self):
        board.DISPLAY.root_group.pop()

    def show(self):
        pass
        #print("show")
        #self.bl.value = True
        #board.DISPLAY.show()

