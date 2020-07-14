import threading


class ip_seg_dic(object):
    dic = {}

    def __init__(self):
        self.lock = threading.Lock()

    def update_dic(self, addr, seg):
        self.lock.acquire()
        List = [seg, True]
        self.dic[addr[0]] = List
        self.lock.release()

    def get_seg(self, addr):
        return self.dic[addr[0]]

    def dell_seg(self, addr):
        self.lock.acquire()
        self.dic[addr[0]][1] = False
        self.lock.release()


    def get_dic(self):
        return self.dic

    def clear_dic(self):
        self.dic.clear()


class app_mem(object):
    app = None
    def __init__(self):
        print("init")

    def get_app(self):
        return self.app

    def set_app(self, app):
        self.app = app
