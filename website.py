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



if __name__ == '__main__':
    count = 0
    c = 0
    app = create_app()
    app.app_context().push()

    mem.APP_MEM.set_app(app)

    scheduler = APScheduler()
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

    app.run(host="127.0.0.1", port=5000, debug=True,
            threaded=True, use_reloader=False)
