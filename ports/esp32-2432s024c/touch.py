'''
Copied from https://github.com/adafruit/Adafruit_CircuitPython_CST8XX/blob/main/examples/cst8xx_simpletest.py
'''

import cst820

ctp = cst820.CST820()
events = cst820.EVENTS

while True:
    if ctp.touched:
        for touch_id, touch in enumerate(ctp.touches):
            x = touch["x"]
            y = touch["y"]
            event = events[touch["event_id"]]
            print(f"touch_id: {touch_id}, x: {x}, y: {y}, event: {event}")