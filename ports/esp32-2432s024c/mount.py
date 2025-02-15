'''
'''
import adafruit_sdcard
import busio
import digitalio
import board
import storage

print("mount.py: Mounting SD card")
# Connect to the card and mount the filesystem.
spi = busio.SPI(board.SD_SCK, board.SD_MOSI, board.SD_MISO)
cs = digitalio.DigitalInOut(board.SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
print("mount.py: Finished")