from __future__ import with_statement
from functions import VideoCapture
import tkinter as tk
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
        res_y, res_x, _ = self.video.make_video_frame().shape

        # It can only really do like 15 fps since it lags
        self.delay = int(1000/fps)

        # Temporary placeholder image
        self.frame = None

        # Boolean continuous video
        self.video_continuous = True

        # Make GUI
        # ----------------------------------------------------------------------
        # make initial window
        self.window = window
        self.window.title(window_title)
        self.window.iconphoto(True, tk.PhotoImage(file="app_icon.png"))

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
        self.dropdown_label = tk.Label(self.ui_canvas, text="Colour Map")
        self.dropdown_label.pack(side=tk.TOP)
        filters = ["jet", "magma", "viridis", "gray", "binary"]
        self.chosen_filter = tk.StringVar()
        self.chosen_filter.set(filters[0])
        self.filter_selector = tk.OptionMenu(self.ui_canvas, self.chosen_filter, *filters)
        self.filter_selector.config(width=15, anchor=tk.CENTER)
        self.filter_selector.pack(side=tk.TOP)

        # add snapshot button
        self.snapshot_button = tk.Button(self.ui_canvas, text="Take Snapshot", width=17, command=self.take_snapshot)
        self.snapshot_button.pack(side=tk.TOP)

        # add pause button
        self.continuous_button = tk.Button(self.ui_canvas, text="Continuous", width=17, command=self.toggle_video)
        self.continuous_button.config(relief=tk.SUNKEN)
        self.continuous_button.pack(side=tk.TOP)

        self.update()

        self.window.mainloop()


    def take_snapshot(self):
        image = PIL.Image.fromarray(self.frame)
        filename = time.strftime("%Y%m%d-%H%M%S") + ".png"
        image.save(filename)
        print("Image saved!")


    def toggle_video(self):
        if self.video_continuous:
            self.continuous_button.config(relief=tk.RAISED)
        else:
            self.continuous_button.config(relief=tk.SUNKEN)
        self.video_continuous = not self.video_continuous
        self.update()
        return


    def update(self):

        # get frame from camera and place it in window
        self.frame = self.video.make_video_frame(cmap=self.chosen_filter.get(), dpi=self.monitor_dpi)
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

        if self.video_continuous:
            self.window.after(self.delay, self.update)


if __name__ == "__main__":
    Camera_App(tk.Tk(), "Camera App", dummy=True, fps=30, host_ip="10.198.202.145", port=9999)
