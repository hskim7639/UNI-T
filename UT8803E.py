# UT8803E

# pip install pywinusb
import time
import libusb
#libusb.config(LIBUSB="./libusb-1.0.dll")
from pywinusb import  hid
import usb
import usb.backend.libusb1

UNI_T_VID=0x10C4
UNI_T_PID=0xEA80

aa='12345678901234567890123456789012345678901234567890123456789012374'
bb = b'12\x00'

def read_handler(data):
    if len(data)>=2:
        v = data[1]
        if v == 4:
            v = 10
        ch = chr(v); print(ch)

class UT8803E:
    INTRPT_IN=0x81; INTRPT_OUT=0x02
    def __init__(self,  device=None):
        self.usbdev = device
        self.usbhandle = None
        self.bb = b'12345678'
        for i in range(56):
            self.bb += b'\x00'
        
        
    def initDevice(self):
        
        pass
        
    def open(self,  **kwargs):
        self.usbhandle = self.usbdev.open()
        self.usbdev.set_raw_data_handler(read_handler)
        pass
        
    def close(self):
        self.usbdev.close()
        
    def write(self,  data):
        pass
        
    def readValue(self):
        pass
        

        
    @staticmethod
    def findDevices():
        devices = usb.core.find(idVendor=UNI_T_VID,idProduct=UNI_T_PID)
        #devices.write(0x81,  b'12345678')
        # devices = filter.get_devices()
        devlist = libusb.usbdevice.get_device_list_with_vid_pid(UNI_T_VID,  UNI_T_PID)
        filter = hid.HidDeviceFilter(vendor_id=UNI_T_VID,  product_id=UNI_T_PID)
        hiddevs = filter.get_devices()
        
        #return devlist
        return hiddevs
        



if __name__ == '__main__':
   
    xx = usb.core.find()
    devs = UT8803E.findDevices()
    print(devs)
    dev= UT8803E(devs[0])
    dev.open()
    dev.initDevice()
    time.sleep(1)
    dev.close()
    for i in range(10):
        v = dev.readValue()
        print(v)
        
