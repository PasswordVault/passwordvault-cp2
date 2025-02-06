'''
'''
from adafruit_hid.keyboard import Keyboard
import btree
from keyboard_layout_win_de import KeyboardLayout
import disp
import os
import usb_hid
import time
import xxtea

app = None
screen = None
db = None

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

'''
app = App({
    'lock': LockPage(),
    'unlock': UnlockPage(),
    'filter': FilterPage(),
    'fav': FavPage(),
    'list': ListPage(),
    'detail': DetailPage(),
})
'''
screen = Screen()
app = App({'dummy': DummyPage()})

pv_password = os.getenv("PV_PASSWORD")
#import_passwords(pv_password)

#kbd = Keyboard()
#usb.device.get().init(kbd, builtin_driver=True)
app.goto('dummy')
#app.run()
