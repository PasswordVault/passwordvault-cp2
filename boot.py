import board
import digitalio
import storage

key3 = digitalio.DigitalInOut(board.GP3)
key3.switch_to_input(digitalio.Pull.UP)

if key3.value:
    storage.disable_usb_drive()
    storage.remount("/", readonly=False)
    print("Mounted read/write")
else:
    print("Mounted read-only")

