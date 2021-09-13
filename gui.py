from __future__ import with_statement
from functions import VideoCapture
import tkinter as tk
import cv2
import PIL.Image
import PIL.ImageTk
import time

class Camera_App:
    def __init__(self, window, window_title, host_ip="0.0.0.0", port=9999, dummy=False, fps=30):

        # Make resources
        # ----------------------------------------------------------------------
        # for testing. if dummy is true, use laptop webcam instead of server
        self.dummy = dummy

        # Connect to video feed
        self.video = VideoCapture(host_ip=host_ip, port=port, dummy=self.dummy)

        # Get camera resolution
        res_y, res_x = self.video.get_data().shape

        # It can only really do like 15 fps since it lags
        self.delay = int(1000/fps)

        # Boolean to decide whether video should be continuous
        self.video_continuous = True

        # Temporary placeholder image
        self.frame = None

        # Make GUI
        # ----------------------------------------------------------------------
        # make initial window
        self.window = window
        self.window.title(window_title)

        # get monitor specs
        self.monitor_dpi = self.window.winfo_fpixels('1i') # get monitor dpi
        self.yres = self.window.winfo_screenheight()
        self.xres = self.window.winfo_screenwidth()

        # set window size to be fullscreen for the monitor
        self.window.geometry(str(self.xres)+"x"+str(self.yres))

        # add a canvas in which image feed and graphs will sit
        self.image_canvas = tk.Canvas(self.window, width=res_x + res_y/5, height=res_y + res_y/5)
        self.image_canvas.grid(row=0, column=0)

        # add a canvas in which all the buttons will sit
        self.ui_canvas = tk.Frame(self.window)
        self.ui_canvas.grid(row=0, column=1, sticky=tk.N, pady=5)

        # add dropdown menu
        filters = ["Grayscale", "RGB"]
        variable = tk.StringVar()
        variable.set(filters[0])
        self.filter_selector = tk.OptionMenu(self.ui_canvas, variable, *filters)
        self.filter_selector.config(width=15, anchor=tk.CENTER)
        self.filter_selector.pack(side=tk.TOP)

        # add snapshot button
        self.snapshot_button = tk.Button(self.ui_canvas, text="Snapshot", width=17, command=self.take_snapshot)
        self.snapshot_button.pack(side=tk.TOP)

        # add pause button
        self.snapshot_button = tk.Button(self.ui_canvas, text="Snapshot", width=17, command=self.take_snapshot)
        self.snapshot_button.pack(side=tk.TOP)

        self.update()

        self.window.mainloop()

    def take_snapshot(self):
        image = PIL.Image.fromarray(self.frame)

        filename = time.strftime("%Y%m%d-%H%M%S") + ".png"
        image.save(filename)
        print("Image saved!")
        

    def update(self):

        # get frame from camera and place it in window
        self.frame = self.video.get_data()
        self.image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.frame))
        image_width = self.image.width()
        image_height = self.image.height()
        self.image_canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

        # make vertical graph
        graph = self.video.make_graph(self.frame, axis=0, dpi=self.monitor_dpi)
        self.graph1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(graph))
        self.image_canvas.create_image(0, image_height, image=self.graph1, anchor=tk.NW)

        # make horizontal graph
        graph = self.video.make_graph(self.frame, axis=1, dpi=self.monitor_dpi)
        self.graph2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(graph))
        self.image_canvas.create_image(image_width, 0, image=self.graph2, anchor=tk.NW)

        self.window.after(self.delay, self.update)


if __name__ == "__main__":
    Camera_App(tk.Tk(), "Camera App", dummy=True, fps=30, host_ip="10.198.202.145", port=9999)
