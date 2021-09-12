import cv2
import struct
import socket
import pickle
import PIL.ImageTk
import PIL.Image

# class VideoCapture:
#     def __init__(self, video_source=0):
#         self.video = cv2.VideoCapture(video_source)
#         if not self.video.isOpened():
#             raise ValueError("Unable to open video source", video_source)

#         self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
#         self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

#     def __del__(self):
#         if self.video.isOpened():
#             self.video.release()

#     def get_frame(self):
#         if self.video.isOpened():
#             _, frame = self.video.read()
#             return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert to RGB
#         else:
#             return None

class VideoCapture:
    def __init__(self, host_ip="0.0.0.0", port=9999):
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host_ip = host_ip
        self.port = port
        self.data = b""
        self.payload_size = struct.calcsize("Q")
        self.video = cv2.VideoCapture(0)

        try:
            self.client_socket.connect((self.host_ip, self.port))
        except:
            print("Could not connect to server")
            pass

    def get_data(self):
        while len(self.data) < self.payload_size:
            packet = self.client_socket.recv(4*1024)
            if not packet: break
            self.data += packet
        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        while len(self.data) < msg_size:
            self.data += self.client_socket.recv(4*1024)
        frame_data = self.data[:msg_size]
        self.data  = self.data[msg_size:]
        frame = pickle.loads(frame_data)
        return frame

    def get_dummy_data(self):
        ret, img  = self.video.read()
        return img

