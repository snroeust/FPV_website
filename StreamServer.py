from __future__ import division

import struct
import threading
import socket

from _thread import *

from app import db
from app.models import User, Post, Rpi


MAX_DGRAM = 2**16


def dump_buffer(s):
    """ Emptying buffer frame """
    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        if struct.unpack("B", seg[0:1])[0] == 1:
            print("finish emptying buffer")
            break


class udp_handler(threading.Thread):
    def __init__(self, name, di):
        threading.Thread.__init__(self)
        self.name = name
        self.di = di
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('127.0.0.1', 12345))
        dump_buffer(self.s)


    def run(self):
        c = 0
        print("UDP RUNS")
        while True:
            if c > 1000:
                self.di.clear_dic()
                dump_buffer(self.s)
                c=0
                print("clear")
            try:
                seg, addr = self.s.recvfrom(MAX_DGRAM)
                self.di.update_dic(addr, seg)
                c += 1
            except:
                print("excetp")
                dump_buffer(self.s)
                self.di.clear_dic()

class tcp_handler(threading.Thread):
    def __init__(self, name, app):
        threading.Thread.__init__(self)
        self.name = name
        self.ServerSocket = socket.socket()
        self.host = '127.0.0.1'
        self.port = 1233
        self.ThreadCount = 0
        self.app = app


    def threaded_client(self, connection, adress, app):

        try:
            while True:
                data = connection.recv(2048)
                name = data.decode('utf-8')

                with app.app_context():

                    # hol alle rpi und merke die ids von dem selben namen
                    rpis = Rpi.query.all()
                    dell = []
                    for i in rpis:
                        if i.get_Rpi()[2] == name:
                            dell.append(i.get_Rpi()[0])

                    rpi = Rpi(ip=adress)
                    rpi.set_name(name)
                    db.session.add(rpi)
                    db.session.commit()

                    for i in dell:
                        db.session.query(Rpi).filter(Rpi.id == i).delete()
                        db.session.commit()

                if not data:
                    break
        except:
            connection.close()
            return None

        finally:
            connection.close()
            return None

    def run(self):

        try:
            self.ServerSocket.bind((self.host, self.port))
            print("TCP-Server ready")
        except socket.error as e:
            print(str(e))

        print('TCP Waitiing for a Connection..')
        self.ServerSocket.listen(5)
        try:
            while True:
                Client, address = self.ServerSocket.accept()
                print('Connected to: ' + address[0] + ':' + str(address[1]))
                start_new_thread(self.threaded_client, (Client, address[0], self.app))
                self.ThreadCount += 1
                print('Thread Number: ' + str(self.ThreadCount))
        except:
            print("ka :/")
        finally:
            self.ServerSocket.close()


def start_tcp_server(app):

    tcp_thread = tcp_handler("TCP_HANDEL", app)
    tcp_thread.start()


def start_udp_server(di):

    udp_thread = udp_handler("UDP_Handle", di)
    udp_thread.start()
