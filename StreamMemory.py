
from mock import app_mem
import threading

#IP_SEG = ip_seg_dic()
APP_MEM = app_mem()


import threading

lock = threading.Lock()
ip_seg = {}


def update_dic(addr, seg):
    lock.acquire()
    List = [seg, True]
    ip_seg[addr[0]] = List
    lock.release()



def get_seg(addr):
    return ip_seg[addr[0]]


def dell_seg(addr):
    lock.acquire()
    ip_seg[addr[0]][1] = False
    lock.release()


def get_dic(self):
    return ip_seg


def clear_dic():
    ip_seg.clear()


