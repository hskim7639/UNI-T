# UT8803E

# pip install pywinusb
import time
#import libusb
#libusb.config(LIBUSB="./libusb-1.0.dll")
from pywinusb import  hid
import ctypes
import usb
#import usb.backend.libusb1

UNI_T_VID=0x10C4
UNI_T_PID=0xEA80

sig_r='\x07\xab\xcd\x04\x58\x00\x01\xd4' # data packet signature
sig_sn = '\x4f\xab\xcd\x17\x00' 


feature_41 = b'\x41\x01'  #  uni-t setting
feature_50 = b'\x50\x00\x00\x25\x80\x00\x00\x03\x00' # uni-t setting
q_serialnum = b'\x07\xab\xcd\x04\x58\x00\x01\xd4' # data to send to query serial number
q_resistance = b'\x07\xab\xcd\x04\x5a\x00\x01\xd6' # data to send to query resistance

my_readbuf = ''
mycount = 0

def read_handler(data):
    global mycount
    global my_readbuf
    if data[0]!=1:
        print('return {}'.format(data[0]))
        return
    v = data[1]
    my_readbuf += chr(v)
    if len(my_readbuf)>=6:
        last5 = my_readbuf[-5:]
        if last5 =='\xab\xcd\x12\x02\x08':
            newdata = my_readbuf[:-5]
            print(newdata)
            my_readbuf = last5
        elif last5 == sig_sn:
            sn = my_readbuf[:-5]
            print('SN:{}'.format(sn))
            my_readbuf = last5
        else:
            print(my_readbuf)
        #print(my_readbuf)
            
    else:
        return
    

class UT8803E:
    INTRPT_IN=0x81; INTRPT_OUT=0x02
    def __init__(self,  device=None):
        self.usbdev = device
        self.usbhandle = None
        
    def initDevice(self):
        
        pass
        
    def open(self,  **kwargs):
        self.usbhandle = self.usbdev.open()
        self.usbdev.send_feature_report(self.to_cbyte_array(feature_41))
        time.sleep(0.01)
        self.usbdev.send_feature_report(self.to_cbyte_array(feature_50))
        time.sleep(0.01)
        self.usbdev.set_raw_data_handler(read_handler) # register read handler
        time.sleep(0.2)
        self.usbdev.send_output_report(q_serialnum) # send message to get serial -> Not working
        time.sleep(0.3)
        self.usbdev.send_output_report(q_resistance) # send message to get resistance
        
    def to_cbyte_array(self,  data):
        # data: bytes: 
        buf = (ctypes.c_byte*len(data))();
        for i in range(len(data)):
            buf[i] = data[i]
        return buf
        
    def close(self):
        self.usbdev.close()
        
    @staticmethod
    def findDevices():
        #devices = usb.core.find(idVendor=UNI_T_VID,idProduct=UNI_T_PID)
        #devlist = libusb.usbdevice.get_device_list_with_vid_pid(UNI_T_VID,  UNI_T_PID)
        filter = hid.HidDeviceFilter(vendor_id=UNI_T_VID,  product_id=UNI_T_PID)
        hiddevs = filter.get_devices()
        return hiddevs
        


if __name__ == '__main__':
    devs = UT8803E.findDevices()
    print(devs)
    dev= UT8803E(devs[0])
    dev.open()
    dev.initDevice()
    time.sleep(20)
    dev.close()
