from app import create_app
from flask_apscheduler import APScheduler
import StreamServer as con
import StreamMemory as mem
global app

def th():
    for i in range(0, 10):
        print("JOOOOOOOOOO")
        print(i)


def start_udp_Connections():
    global c
    if c == 0:
        c+=1
        print("UDP Connection Threads started ...")
        con.start_udp_server(mem.IP_SEG)
        print("UDP_Connection Threads running!")
        c += 1
    else:
        print("all right -- UDP")



def start_tcp_Connections():
    global count
    if count == 0:
        print("TCP Connection Threads started ...")
        con.start_tcp_server(app)
        print("TCP_Connection Threads running!")
        count+=1
    else:
        print("all right -- TCP")



count = 0
c = 0
print("joooooooo")

app = create_app()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
