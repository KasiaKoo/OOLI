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
            # self.video.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
            # self.video.set(cv2.CAP_PROP_EXPOSURE, -7)

        # otherwise, connect to server
        else:
            try:
                self.client_socket.connect((self.host_ip, self.port))
            except:
                print("Could not connect to server")
                pass


    def make_video_frame(self, cmap="jet", dpi=100, resolution=(854,480), min_x=None, max_x=None, min_y=None, max_y=None):

        # if testing, then return laptop webcam feed
        if self.dummy:
            ret, img = self.video.read()
            original_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            width, height = resolution
            figure = plt.figure(figsize=(width/dpi, height/dpi), dpi=dpi)
            plt.imshow(original_img, cmap=cmap, aspect="auto")
            plt.xlim(min_x, max_x)
            plt.ylim(min_y, max_y)
            plt.axis("off")
            plt.tight_layout(pad=0)
            figure.canvas.draw()
            plt.close(figure)

            preview_img = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8, sep="")
            preview_img = preview_img.reshape(figure.canvas.get_width_height()[::-1] + (3,))

            return preview_img, original_img

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

        figure = plt.figure()
        plt.imshow(original_img, cmap=cmap, aspect="auto")
        plt.xlim(min_x, max_x)
        plt.ylim(min_y, max_y)
        plt.axis("off")
        plt.tight_layout(pad=0)
        figure.canvas.draw()
        plt.close(figure)

        preview_img = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8, sep="")
        preview_img = preview_img.reshape(figure.canvas.get_width_height()[::-1] + (3,))

        return preview_img, original_img

    def make_graph(self, preview_img, axis=0, dpi=100, graph_height=100, min_x=None, max_x=None, min_y=None, max_y=None):

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
        plt.tight_layout()
        figure.canvas.draw()

        plt.close(figure)

        graph = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8, sep="")
        graph = graph.reshape(figure.canvas.get_width_height()[::-1] + (3,))
        if axis == 1:
            graph = cv2.rotate(graph, cv2.ROTATE_90_CLOCKWISE)

        return graph
