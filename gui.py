from functions import VideoCapture
import tkinter as tk
import cv2
import PIL.Image
import PIL.ImageTk


class Camera_App:
    def __init__(
        self, window, window_title, host_ip="0.0.0.0", port=9999, dummy=False, fps=30):

        # Get resources
        # ----------------------------------------------------------------------
        # for testing. if dummy is true, use laptop webcam instead of server
        self.dummy = dummy

        # Connect to video feed
        self.video = VideoCapture(host_ip=host_ip, port=port, dummy=self.dummy)

        # It can only really do like 15 fps since it lags
        self.delay = 15

        # Make GUI
        # ----------------------------------------------------------------------
        self.window = window
        self.window.title(window_title)
        self.monitor_dpi = self.window.winfo_fpixels('1i') # get monitor dpi

        self.canvas = tk.Canvas(window, width=1920, height=1080)
        self.canvas.pack()

        self.update()

        self.window.mainloop()


    def update(self):

        # get frame from camera and place it in window
        frame = self.video.get_data()
        self.image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        image_width = self.image.width()
        image_height = self.image.height()
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

        # make vertical graph
        graph = self.video.make_graph(frame, axis=0, dpi=self.monitor_dpi)
        self.graph1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(graph))
        self.canvas.create_image(0, image_height, image=self.graph1, anchor=tk.NW)

        # make horizontal graph
        graph = self.video.make_graph(frame, axis=1, dpi=self.monitor_dpi)
        self.graph2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(graph))
        self.canvas.create_image(image_width, 0, image=self.graph2, anchor=tk.NW)

        self.window.after(self.delay, self.update)


if __name__ == "__main__":
    Camera_App(tk.Tk(), "Camera App", dummy=True, fps=30, host_ip="10.198.202.145", port=9999)
