import socket
from _thread import *
import threading 
import imutils
import pickle
import cv2
import struct
from pypylon import pylon
import sys, errno
import json

""" Defining function to transmit specific camera feeds to client """
#working with dictionary of all computers in the lab
#allows us to only differentiate them by type
#if new camera type needs to be added you need to create new transmitting function
#and add an elif statement to the new_client_thread function

def webcam_trans(c, cam_numb=0):
    print('in webcam')
    vid = cv2.VideoCapture(cam_numb)
    while vid.isOpened():
        img, frame = vid.read()
        frame = imutils.resize(frame, width=320)
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a))+a
        c.sendall(message)


def basler_trans(c):
    print('in basler')
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())    
    camera.Open() 
    camera.StartGrabbing()
    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        frame = grabResult.Array
        frame = imutils.resize(frame, width=320)
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a))+a
        c.sendall(message)

""" New client Thread functions allow to transmit to multiple people at ones """
#allows for multiple camera transmittion at ones
#error handling necessary to not stop listening when client disconnects
def new_client_thread(c, addr):
    while True:
        try:        
            data = c.recv(1024).decode('ascii')
            print('Client {} wants to connect to {}'.format((addr[0],addr[1]), data))
            cam_type = cam_det[data]['cam_type']
            if cam_type =='basler':
                basler_trans(c)
            elif cam_type == 'webcam':
                cam_num = cam_det[data]['cam_num']
                webcam_trans(c, cam_numb=cam_num)

            elif not data:
                print('Bye to ', addr[0],addr[1])
                # print_lock.release()
                break
        except IOError as e:
            #neccesary to not lose listening when client breaks of
            if e.errno == errno.EPIPE:
                print('Bye to ', addr[0],addr[1])
                print('Released the camera', data)
                # print_lock.release()
                break
    # connection closed
    c.close()

""" Main function """
#Loading the camera dictionary
with open("camera_list.json") as f:
    cam_det = json.load(f)  

#Opening the socket
port = 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
s.bind(("", port))
s.listen(5)
print('Listening at',host_ip, port)


# a forever loop until client wants to exit
while True:

    # establish connection with client
    c, addr = s.accept()
    print('Connected to :', addr[0], ':', addr[1])
    # Start a new thread
    start_new_thread(new_client_thread, (c,addr))
s.close()

