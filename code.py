'''
PasswordVault
- in CircuitPython
- on Raspberry Pi Pico2 W
- with Waveshare 1.44 screen with four buttons

https://passwordvault.de

(c)2025 Olav Schettler <olav@schettler.net
'''
from adafruit_hid.keyboard import Keyboard
from keyboard_layout_win_de import KeyboardLayout
import disp
import os
import usb_hid
import time
import xxtea

app = None
screen = None

class Screen():

    def __init__(self):
        self.lcd = disp.Display()
        #self.backlight(0.5)
        #self.clear()
    
    def config_buttons(self):
        return self.lcd.config_buttons()
    
    def button(self, i):
        return self.lcd.button(i)

    def example(self):
        return self.lcd.example()
    
    @property
    def width(self):
        return self.lcd.width

    @property
    def height(self):
        return self.lcd.height

    def backlight(self, percent):
        pin = Pin(wslcd.BL) if app.display_type == 'ws1.44' else Pin(wslcd13.BL)
        pwm = PWM(pin)
        pwm.freq(1000)
        pwm.duty_u16(round(65536 * percent))
    
    def clear(self):
        self.lcd.clear()
    
    def fill_rect(self, x,y, w,h, color):
        return self.lcd.fill_rect(x,y, w,h, color)

    def text(self, txt, x,y, color):
        return self.lcd.text(txt, x,y, color)
    
    def hline(self, x,y, w, color):
        return self.lcd.hline(x,y, w, color)

    def show_header(self, prompt, title):
        self.fill_rect(0,0, self.width,8, self.lcd.BLACK)
        self.text(prompt, 0,0, self.lcd.WHITE)
        self.text(title, 10,0, self.lcd.WHITE)
        self.hline(0,10, self.width, self.lcd.GBLUE)

    def show(self):
        pass
        #return self.lcd.show()


class App:
    def __init__(self, pages):
        self.pages = pages
        self.buttons_count = screen.config_buttons()
        self.keys = [False for k in range(self.buttons_count)]

    def read_keys(self):
        '''
        Read the keys into self.keys.
        If any key was pressed or released,
        flag this in the return values.
        '''
        pressed = False
        released = False
        prev_keys = self.keys
        changed_keys = [False for k in range(self.buttons_count)]
        self.keys = []
        for i in range(self.buttons_count):
            value = screen.button(i) == 0
            self.keys.append(value)
            if value > prev_keys[i]:
                pressed = True
                changed_keys[i] = True
            elif value < prev_keys[i]:
                released = True
                changed_keys[i] = True
        return (pressed, released, changed_keys)
    
    def goto(self, page_name, **kwargs):
        print(f"goto {page_name}", kwargs)
        screen.clear()
        self.page = self.pages[page_name]
        self.page.setup(**kwargs)

    def run(self):
        while(True):
            pressed, released, changed_keys = self.read_keys()

            if pressed and getattr(self.page, "on_key_pressed", None):
                self.page.on_key_pressed(changed_keys)
            if released and getattr(self.page, "on_key_released", None):
                self.page.on_key_released(changed_keys)

            if hasattr(self.page, 'update'):
                self.page.update()

            if self.page.dirty:
                self.page.draw()
                screen.show()
                self.page.dirty = False

        time.sleep(1)
        screen.clear()



class TextEntry:
    CELL_WIDTH = 10
    Y_OFFSET = 18
    CELL_HEIGHT = 12
    BUF_SIZE = 20

    def calc_key_lines(self):
        self.key_lines = math.ceil(len(self.keys) / self.width)

    def __init__(self, keys, width, next_page = None, prompt = ">"):
        self.dirty = True
        self.keys = keys
        self.width = width
        self.prompt = prompt
        self.next_page = next_page
        self.calc_key_lines()

    def setup(self, input = "", message = "", **kwargs):
        self.input = input
        self.message = message
        self.x_offs = screen.width / 2 - self.CELL_WIDTH * self.width / 2 -12
        self.cursor_x = self.cursor_y = 0
        self.mode = 'v' # vertical or horizontal

        if 'keys' in kwargs:
            self.keys = kwargs['keys']
            self.calc_key_lines()

    def show_key_labels(self):
        labels = {
            'v': ['NXT', ' UP', 'DWN', 'HOR'],
            'h': ['SEL', 'LFT', 'RGT', 'VER'],
        }
        for i,y in enumerate([1, 39, 75, screen.height - 15]):
            screen.fill_rect(screen.width - 24,y, 24,9, screen.lcd.YELLOW)
            screen.text(labels[self.mode][i], screen.width - 24, y+1, screen.lcd.BLACK)

    def draw(self):
        x = y = 0
        screen.show_header(self.prompt, self.input)

        for i in range(0, len(self.keys)):
            c = self.keys[i]
            pos_x = round(self.x_offs + x * self.CELL_WIDTH)
            pos_y = round(self.Y_OFFSET + y * self.CELL_HEIGHT)
            if x == self.cursor_x and y == self.cursor_y:
                screen.text(c, pos_x, pos_y, screen.lcd.GBLUE) 
            else:
                screen.text(c, pos_x, pos_y, screen.lcd.WHITE)
            x += 1
            if x >= self.width:
                x = 0
                y += 1

        line_y = 20 + self.key_lines * self.CELL_HEIGHT
        screen.hline(0, line_y, screen.width, screen.lcd.GBLUE)
        screen.fill_rect(0,80, screen.width,8, screen.lcd.BLACK)
        screen.text(self.message, 0,80, screen.lcd.GREEN)
        self.about()
        self.show_key_labels()

    def about(self):
        top = 88
        screen.text("passwordvault.de", 0,top+8, screen.lcd.GREEN)
        screen.text(PV_VERSION, 40,top+18, screen.lcd.WHITE)
        print(f"DISPLAY TYPE {app.display_type} {screen.width}x{screen.height}")

    def on_key_pressed(self, keys):
        '''
        Handles key and returns true if handledS.
        Returns false if key is not handled
        '''
        self.dirty = True
        if keys[2]: # LEFT or UP
            if self.mode == 'v':         # UP
                if self.cursor_y > 0:
                    self.cursor_y -= 1
            else:                        # LEFT
                if self.cursor_x > 0:
                    self.cursor_x -= 1

        elif keys[1]: # RIGHT or DOWN
            if self.mode == 'v':         # DOWN
                new_i = (self.cursor_y + 1) * self.width + self.cursor_x
                if self.cursor_y < self.key_lines and new_i < len(self.keys):
                    self.cursor_y += 1
                else:
                    self.cursor_y = 0
            else:                        # RIGHT
                new_i = self.cursor_y * self.width + self.cursor_x + 1
                if self.cursor_x < self.width - 1 and new_i < len(self.keys):
                    self.cursor_x += 1
                else:
                    self.cursor_x = 0

        elif keys[0]: # HOR or VRT
            if self.mode == 'v':
                self.mode = 'h'          # HORIZONTAL
            else:
                self.mode = 'v'          # VERTICAL

        elif keys[3]: # SEL or NXT
            if self.mode == 'h':         # SELECT
                i = self.cursor_y * self.width + self.cursor_x
                key = self.keys[i]
                if key == '<':           # BACKSPACE
                    print("BACKSPACE")
                    if len(self.input) > 0:
                        self.input = self.input[:-1]
                elif key == '>':         # CLEAR
                    self.input = ''
                elif len(self.input) + 1 < self.BUF_SIZE:
                    self.input += key
            else:                        # NEXT
                if self.next_page:
                    next_page = self.next_page(self.input) if callable(self.next_page) else self.next_page
                    app.goto(next_page, input=self.input)

        else:
            self.dirty = False


class LockPage(TextEntry):

    def __init__(self):
        super().__init__("123456789<0>", 3, "unlock")

    def setup(self, message = "Please unlock"):
        super().setup(message = message)


class UnlockPage:

    def setup(self, input):
        if input == PASSWORD:
            app.goto('filter')
        else:
            app.goto('lock', message="Try again")


class DummyPage:
    def __init__(self):
        self.dirty = True

    def setup(self):
        pass

    def draw(self):
        screen.example()

    def on_key_pressed(self, changed_keys):
        if changed_keys[3]:
            kbd = Keyboard(usb_hid.devices)
            layout = KeyboardLayout(kbd)
            layout.write("qwertzäöüß!\"§$%&/()=")


#-------------------------------------------------------------------

screen = Screen()
app = App({
    'dummy': DummyPage(),
    'lock': LockPage(),
})

pv_password = os.getenv("PV_PASSWORD")

app.goto('lock')
app.run()


