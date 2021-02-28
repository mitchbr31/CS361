#/usr/local/bin/env
import sys
import socket
import os
import csv
import importlib


#content = importlib.import_module("content-generator")

csv_file = "./life_output.csv"

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    waiting = True
    while waiting:
        if os.path.exists(csv_file):
            with open(csv_file, "r") as infile:
                filereader = csv.reader(infile, delimiter=';')
                for row in filereader:
                    # Grab the two keywords
                    if len(row) > 0:
                        row = row[0].split(",")
                        in1 = row[0] + "," + row[1]
                    waiting = False

    print("Client sending: " + in1)
    s.sendall(str.encode(in1))
    while True:
        data = s.recv(1024)
        break

dat = data.decode("utf-8").split(sep=';')
print('Content Client received', dat)
