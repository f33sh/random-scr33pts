#!/usr/bin/env python3

import socket

HOST = "192.168.56.102"
PORT = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect( (HOST, PORT) )

    msg = ""
    while msg != "exit":
        msg = input("> ").strip()
        s.send(msg.encode('utf-8'))
        res = s.recv(2048)
        print("\n", res,"\n")

except Exception as e:
    print("Exception:", e)
