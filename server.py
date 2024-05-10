from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import os
import sys
import json
import socket
import requests
from threading import Thread
from urllib.parse import parse_qs
import glob

import base64
import cv2
import numpy as np

from blobDetect import detect_blobs


tempSpline = []
img = []
mask = []
small_img = []

class Handler(BaseHTTPRequestHandler):
        
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><body><h1>Hello World!</h1></body></html>", "utf-8"))

    def do_POST(self):
        global tempSpline, img, mask, small_img

        length = int(self.headers.get('content-length'))
        request_type = self.headers.get('Request-Type')
        print("request type: " + str(request_type));
        print("headers: " + str(self.headers));
        headers = self.headers

        if request_type == 'ComCheck':
            print('Sending super secret message to client.')
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Request-Timestamp', datetime.utcnow().strftime('\t%Y-%m-%d %H:%M:%S.%f')[:-3])
            self.end_headers()
            self.wfile.write(bytes("A super secret message that only the server knows.", "utf-8"))

        elif request_type == 'SaveStats':
            print('Recieved Stats with data size '+ str(length))
            data = self.rfile.read(length)

            timenow = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]

            fileName = "matrix_stats/Stats" + str(timenow) + ".txt"
            stats_data_file = open(fileName, "wb+")
            stats_data_file.write(data)
            stats_data_file.close()

            print('Stats data written to: ' + fileName + '\n\n')

            parsed_data = data.decode('utf-8')

            self.send_response(200)
            self.send_header("Content-type", "text")
            self.send_header('Request-Timestamp', datetime.utcnow().strftime('\t%Y-%m-%d %H:%M:%S.%f')[:-3])
            self.end_headers()
            self.wfile.write(bytes("The server has recieved the stats data.", "utf-8"))


        elif request_type == 'BlobDetect':
            print('Recieved request to call Blob Detect routine with data size '+ str(length))
            data = self.rfile.read(length)
            img = cv2.imdecode(np.frombuffer(data, dtype='uint8'), 1)

            #Debugging
            #img = cv2.imread('PXL_20240328_182819987.jpg')

            cv2.imwrite("blobImage.jpg",img)

            stats = detect_blobs(img)

            self.send_response(200)
            self.send_header("Content-type", "text")
            self.send_header('Request-Timestamp', datetime.utcnow().strftime('\t%Y-%m-%d %H:%M:%S.%f')[:-3])
            self.end_headers()
            results_bytes = bytes(json.dumps(stats.tolist()),'utf-8')
            print("Bytes size = " + str(len(results_bytes)))
            print('Sending: (total size)' + str(len(str(json.dumps(stats.tolist())))) + '\nFirst lines: ' + str(json.dumps(stats.tolist())[:200]))
            self.wfile.write(bytes(json.dumps(stats.tolist()),'utf-8'))
            
        else:
            self.send_response(500)

def send_ip_to_hl2(hostName, serverPort, hl2_ip):

    hl2_port = 4444
    hl2_endpoint = "http://{}:{}".format(hl2_ip,hl2_port)

    headers = {
        'Content-Type': 'application/json"',
    }
    data = {"ipAddress":hostName, "port":str(serverPort)}

    connected = False
    while not connected:
        try:
            print("Sending Post! Connected = " + str(connected))
            requests.post(hl2_endpoint, json=data, headers=headers) 
            if not connected:
                print('Connecting to HoLoLens 2 device...')
            connected = True
        except:
            connected = False
            pass
        sleep(1)
        
def get_ip_manually(device,fname):
    default_ip = ''
    out_path = ''
    if os.path.exists(fname):
        with open(fname,'r') as f:
            try:
                default_ip = f.readlines()[0]        
            except:
                pass
    IP = input("\nEnter Your {} local IP then press ENTER (default: {}): ".format(device,default_ip)) 
    if IP == '':
        IP = default_ip           
    with open(fname,'w') as f:
        f.write(IP)

    return IP

def displayImage(img):
    cv2.imshow('test image window', img)
    time.sleep(1)
    cv2.destroyAllWindows()

editor = False

if editor:
    HOST = '192.168.4.21'#Desktop
    hl2_ip = HOST

else:
    HOST = '192.168.4.21'#Desktop
    hl2_ip = '192.168.4.30'#HoloLens



PORT = 8090
time_out = 1e-6

server = HTTPServer((HOST, PORT), Handler)
server.socket.settimeout(time_out)


#hl2_ip = get_ip_manually('HoloLens 2','hl2_ip.txt')

#thread = Thread(target = send_ip_to_hl2, args = (HOST, PORT, hl2_ip))
#thread.start()

try:
    print("\nServer now running on http://%s:%s" % (HOST, PORT)+ datetime.utcnow().strftime('\t%Y-%m-%d %H:%M:%S.%f')[:-3])
    server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()

