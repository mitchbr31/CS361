#!/usr/bin/env python3
import socket
import os
import csv
import importlib
content = importlib.import_module("content-generator-test")

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 65433        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            dat1 = "2020"
            dat2 = "California"
            print('Population Server received', dat1, "and", dat2)

            with open("pop_content_in.csv", "w") as file:
                csv_out = csv.writer(file)
                csv_out.writerow([dat1 + ";" + dat2])
            os.system("python3 Pop_Gen_Gui.py pop_content_in.csv")
            if not data:
                break
            conn.sendall(data)
            break