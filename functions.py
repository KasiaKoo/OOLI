import cv2
import struct
import socket
import pickle
import PIL.ImageTk
import PIL.Image
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('agg')


class VideoCapture:
    def __init__(self, host_ip="0.0.0.0", port=9999, dummy=False):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = host_ip
        self.port = port
        self.data = b""
        self.payload_size = struct.calcsize("Q")

        # if testing, then connect to laptop webcam
        self.dummy = dummy
        if self.dummy:
            self.video = cv2.VideoCapture(0)

        # otherwise, connect to server
        else:
            try:
                self.client_socket.connect((self.host_ip, self.port))
            except:
                print("Could not connect to server")
                pass


    def get_data(self, filt="Greyscale"):

        # if testing, then return laptop webcam feed
        if self.dummy:

            filters = {"Greyscale": cv2.COLOR_BGR2GRAY,
                       "RGB": cv2.COLOR_BGR2RGB}
            chosen_filter = filters[filt]

            ret, img = self.video.read()
            img = cv2.cvtColor(img, chosen_filter)
            return img

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
        frame = pickle.loads(frame_data)
        return frame

    def make_graph(self, frame, axis=0, dpi=100):

        # convert to greyscale if in rgb
        if len(frame.shape) > 2:
            rgb_weights = [0.2989, 0.5870, 0.1140]
            frame = np.dot(frame[...,:3], rgb_weights)

        height, width = frame.shape
        if axis == 0:
            figure = plt.figure(figsize=(width/dpi, (height/dpi)/5), dpi=dpi)
        else:
            figure = plt.figure(figsize=(height/dpi, (height/dpi)/5), dpi=dpi)
            

        summation = np.sum(frame, axis=axis)

        plt.plot(summation, c="r")
        plt.axis('off')
        plt.tight_layout(pad=0)
        figure.canvas.draw()

        plt.close(figure)

        graph = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8, sep="")
        graph = graph.reshape(figure.canvas.get_width_height()[::-1] + (3,))
        if axis == 1:
            graph = cv2.rotate(graph, cv2.ROTATE_90_CLOCKWISE)

        return graph
