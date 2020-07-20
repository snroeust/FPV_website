from website import app
from flask_apscheduler import APScheduler
import StreamMemory as mem

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

if __name__ == "__main__":
    # app = create_app()
    app.app_context().push()
    print("joooooooo")
    mem.APP_MEM.set_app(app)
    print("joooooooo")
    scheduler = APScheduler()
    print("joooooooo")
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    print("joooooooo")
    scheduler.start()
    print("joooooooo")


    app.run()
