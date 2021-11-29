import cv2
import struct
import socket
import pickle
import PIL.ImageTk
import PIL.Image
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import time
from pypylon import pylon
matplotlib.use('agg')


class VideoCapture:
    def __init__(self, host_ip="0.0.0.0", port=9999, cameraname='Kasia Camera'):

        """Video class that controls connecting to server and returning images to gui

        :param host_ip: IP address of server hosting camera
        :param port: Open port on server where camera is hosted
        :param cameraname: Name of camera stored in camera list dictionary

        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(5) # set timeout to be 5 seconds
        self.host_ip = host_ip
        self.port = port
        self.cameraname = cameraname
        self.data = b""
        self.payload_size = struct.calcsize("Q")
        self.basler = False
        print('host ip', host_ip)
        # if testing, then connect to laptop webcam
        if host_ip=="None":
            self.connected_to_server = False
            self.video = cv2.VideoCapture(0)
            self.video.set(cv2.CAP_PROP_FPS, 60) # set camera fps if possible
            self.video.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            print('i am here')
            # self.video.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
            # self.video.set(cv2.CAP_PROP_EXPOSURE, -7)

        elif host_ip=="Basler":
            self.connected_to_server = False
            self.basler = True
            self.video = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())    
            self.video.Open() 
            self.video.StartGrabbing()

        # otherwise, connect to server
        else:
            try:
                self.client_socket.connect((self.host_ip, self.port))
                self.client_socket.send(self.cameraname.encode('ascii'))
                self.connected_to_server = True
            except: # Raise exception
                self.connected_to_server = False
                print("Could not connect to server!")
                raise Exception("Could not connect to server!")


    def get_video_frame(self):

        """Connects to chosen server and gets single frame to return to gui

        :returns: Grayscale single image array

        """
        # if testing, then return laptop webcam feed
        if self.connected_to_server == False:
            ret, img = self.video.read()
            original_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            return original_img

        if self.basler == True:
            grabResult = self.video.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            img = grabResult.Array
            img = imutils.resize(frame, width=320)
            original_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # not sure if this is necessary
            return frame
            

        # otherwise, return server camera feed
        while len(self.data) < self.payload_size:
            packet = self.client_socket.recv(4 * 1024)
            if not packet:
                break
            self.data += packet
        packed_msg_size = self.data[: self.payload_size]
        self.data = self.data[self.payload_size :]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(self.data) < msg_size:
            self.data += self.client_socket.recv(4 * 1024)
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]

        original_img = pickle.loads(frame_data)

        return original_img


    def make_cropped_image(self, original_img, cmap="jet", dpi=100, resolution=(854,480), min_x=None, max_x=None, min_y=None, max_y=None):

        """Takes original image array and returns cropped image given x and y limits

        :param original_img: Original image array
        :param cmap: Chosen colour map
        :param dpi: DPI of display screen
        :param resolution: Chosen resolution for preview
        :param min_x: X lower limit for crop
        :param max_x: X upper limit for crop
        :param min_y: Y lower limit for crop
        :param max_y: Y upper limit for crop
        :returns: Cropped image array

        """
        width, height = resolution
        figure = plt.figure(figsize=(width/dpi, height/dpi), dpi=dpi)
        plt.imshow(original_img, cmap=cmap, aspect="auto")
        plt.xlim(min_x, max_x)
        plt.ylim(max_y, min_y) # this has to be reversed since the numbers on the vert graph are reverse of the image
        plt.axis("off")
        plt.tight_layout(pad=0)
        figure.canvas.draw()
        plt.close(figure)

        preview_img = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8, sep="")
        preview_img = preview_img.reshape(figure.canvas.get_width_height()[::-1] + (3,))

        return preview_img


    def make_graph(self, preview_img, axis=0, dpi=100, graph_height=100, min_x=None, max_x=None, min_y=None, max_y=None):

        """Takes preview image and returns X and Y intensity graphs

        :param preview_img: Preview image to construct graphs for
        :param axis: If 0, return horizontal graph. Else, return vertical graph
        :param dpi: DPI of display screen
        :param graph_height: Height of output horizontal graph (width for vertical graphs)
        :param min_x: X lower limit for pixel number
        :param max_x: X upper limit for pixel number
        :param min_y: Y lower limit for pixel number
        :param max_y: Y upper limit for pixel number
        :returns: Image array of intensity graph

        """
        # convert to greyscale if in rgb
        if len(preview_img.shape) > 2:
            rgb_weights = [0.2989, 0.5870, 0.1140]
            preview_img = np.dot(preview_img[...,:3], rgb_weights)

        height, width = preview_img.shape
        if axis == 0:
            figure = plt.figure(figsize=(width/dpi, (graph_height/dpi)), dpi=dpi)
        else:
            figure = plt.figure(figsize=(height/dpi, (graph_height/dpi)), dpi=dpi)
            

        summation = np.sum(preview_img, axis=axis)

        plt.plot(summation, c="r")

        plt.xlim(min_x, max_x)
        plt.ylim(min_y, max_y)
        # plt.axis('off')
        plt.yticks([], [])
        plt.grid()
        plt.box(0)
        plt.tight_layout(pad=0)
        figure.canvas.draw()

        plt.close(figure)

        graph = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8, sep="")
        graph = graph.reshape(figure.canvas.get_width_height()[::-1] + (3,))
        if axis == 1:
            graph = cv2.rotate(graph, cv2.ROTATE_90_CLOCKWISE)

        return graph
