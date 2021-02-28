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
            dat = data.decode("utf-8").split(sep=';')
            dat=dat[0].split(",")
            print('Content Server received: ', dat)
            if not data:
                break
            #conn.sendall(data)
            with open("life_input.csv", "w") as file:
                csv_out = csv.writer(file, delimiter=',')
                csv_out.writerow(dat)
            filename = 'C:\\Users\\Tate\\Desktop\\CS361\\life-generator.py life_input.csv'
            os.system('"' + filename + '"')
            with open("life_output.csv", "r") as file1:
                filereader = csv.reader(file1)
                outs = []
                for row in filereader:
                    if len(row)>0:
                        print(row)
                        out1 = row[3]
            print("Content server sending: " + str(out1))
            conn.sendall(str.encode(out1))

            break