#/usr/local/bin/env
import sys
import socket
import os
import csv
import importlib
#content = importlib.import_module("content-generator-test")

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            dat1, dat2 = data.decode("utf-8").split(sep=',')
            print('Content server received: ', dat1, "and", dat2)
            if not data:
                break
            #conn.sendall(data)
            with open("content_in.csv", "w") as file:
                csv_out = csv.writer(file)
                csv_out.writerow([dat1 + ";" + dat2])
            filename = 'C:\\Users\\Tate\\Desktop\\CS361\\content-generator.py content_in.csv'
            os.system('"' + filename + '"')
            with open("cont_output.csv", "r") as file:
                filereader = csv.reader(file)
                for row in filereader:
                    if len(row) >1:
                        out1 = row[0] + "," + row[1] + "," + row[2]
            print("Content server sending: " + out1)
            conn.sendall(str.encode(out1))

            break