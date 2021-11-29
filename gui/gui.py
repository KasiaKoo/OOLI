from __future__ import with_statement
from image_processing.functions import VideoCapture
import tkinter as tk
from tkinter import filedialog
import PIL.Image
import PIL.ImageTk
import json
import os, sys, subprocess

class Camera_App:

    # APP INITIALISE
    # --------------------------------------------------------------------------
    
    def __init__(self, window, window_title, fps=30):

        """OOLI User Interface class

        :param window: tk window object
        :param window_title: Title to display in window
        :param fps: Frames per second of preview feed

        """
        # Make resources
        # ----------------------------------------------------------------------

        # It can only really do like 15 fps since it lags
        self.delay = int(1000/fps)

        # Temporary placeholder photo array and preview array
        self.photo = None
        self.preview = None

        # Boolean continuous video
        self.video_continuous = False

        # Details of available cameras
        with open("assets/camera_list.json") as f:
            self.camera_details = json.load(f)

        # Allowed preview resolutions (add any required)
        self.resolutions = {"256x144 (16:9)": (256, 144),
                            "320x240 (4:3)": (320, 240),
                            "426x240 (16:9)": (426, 240),
                            "640x480 (4:3)": (640, 480),
                            "854x480 (16:9)": (854, 480),
                            "1280x720 (16:9)": (1280, 720)}


        # Get initial preview resolution
        self.res_x, self.res_y = self.resolutions["854x480 (16:9)"]

        # Allowed filters
        filters = ["jet", "magma", "viridis", "gray", "binary"]

        # Height of reference graph in pixels
        self.reference_graph_height = 150

        # Initial bounds of graphs
        self.horizontal_xmin = None
        self.horizontal_xmax = None
        self.vertical_xmin = None
        self.vertical_xmax = None

        # Make GUI
        # ----------------------------------------------------------------------
        # make initial window
        self.window = window
        self.window.title(window_title)
        self.window.iconphoto(True, tk.PhotoImage(file="assets/app_icon.png"))

        # get monitor specs
        self.monitor_dpi = self.window.winfo_fpixels('1i') # get monitor dpi
        self.yres = self.window.winfo_screenheight()
        self.xres = self.window.winfo_screenwidth()

        # set window size to be fullscreen for the monitor
        self.window.geometry(str(self.xres)+"x"+str(self.yres))

        # add a canvas in which image feed and graphs will sit
        self.preview_canvas = tk.Canvas(self.window, width=self.res_x + self.reference_graph_height, height=self.res_y + self.reference_graph_height)
        self.preview_canvas.grid(row=0, column=0, sticky=tk.N)

        # add a canvas in which all the buttons will sit
        self.ui_canvas = tk.Frame(self.window)
        self.ui_canvas.grid(row=0, column=1, sticky=tk.N, pady=5)

        # add a dropdown menu for selecting camera
        self.camera_select_label = tk.Label(self.ui_canvas, text="Select Camera")
        self.camera_select_label.pack(side=tk.TOP)
        camera_list = list(self.camera_details.keys())
        self.chosen_camera = tk.StringVar()
        self.chosen_camera.set(camera_list[0])
        self.camera_selector = tk.OptionMenu(self.ui_canvas, self.chosen_camera, *camera_list)
        self.camera_selector.config(width=15, anchor=tk.CENTER)
        self.camera_selector.pack(side=tk.TOP)

        # add button to open camera list json file
        self.add_camera_button = tk.Button(self.ui_canvas, text="Open Server List", width=17, command=self.open_server_list)
        self.add_camera_button.pack(side=tk.TOP)

        # add dropdown menu for preview resolution
        self.resolution_dropdown_label = tk.Label(self.ui_canvas, text="Preview Resolution")
        self.resolution_dropdown_label.pack(side=tk.TOP)
        res_list = list(self.resolutions.keys())
        self.chosen_res = tk.StringVar()
        self.chosen_res.set("854x480 (16:9)")
        self.res_selector = tk.OptionMenu(self.ui_canvas, self.chosen_res, *res_list)
        self.res_selector.config(width=15, anchor=tk.CENTER)
        self.res_selector.pack(side=tk.TOP)

        # add dropdown menu for colourmap
        self.colourmap_dropdown_label = tk.Label(self.ui_canvas, text="Colour Map")
        self.colourmap_dropdown_label.pack(side=tk.TOP)
        self.chosen_filter = tk.StringVar()
        self.chosen_filter.set(filters[0])
        self.filter_selector = tk.OptionMenu(self.ui_canvas, self.chosen_filter, *filters)
        self.filter_selector.config(width=15, anchor=tk.CENTER)
        self.filter_selector.pack(side=tk.TOP)

        # add update button (for when not continuous)
        self.update_button = tk.Button(self.ui_canvas, text="Update", width=17, command=self.update_all)
        self.update_button.pack(side=tk.TOP)

        # add pause button
        self.continuous_button = tk.Button(self.ui_canvas, text="Continuous", width=17, command=self.toggle_video)
        self.continuous_button.config(relief=tk.SUNKEN, fg="green")
        self.continuous_button.pack(side=tk.TOP)

        # add horizontal graph X limits text input
        self.horizontal_limits_label = tk.Label(self.ui_canvas, text="Horizontal Limits")
        self.horizontal_limits_label.pack(side=tk.TOP)
        self.horizontal_xmin_entry = tk.Entry(self.ui_canvas, width=19)
        self.horizontal_xmin_entry.pack(side=tk.TOP)
        self.horizontal_xmax_entry = tk.Entry(self.ui_canvas, width=19)
        self.horizontal_xmax_entry.pack(side=tk.TOP)
        self.horizontal_crop_button = tk.Button(self.ui_canvas, text="Crop Horizontal", width=17, command=self.crop_horizontal)
        self.horizontal_crop_button.pack(side=tk.TOP)

        # add vertical graph X limits text input
        self.vertical_limits_label = tk.Label(self.ui_canvas, text="Vertical Limits")
        self.vertical_limits_label.pack(side=tk.TOP)
        self.vertical_xmin_entry = tk.Entry(self.ui_canvas, width=19)
        self.vertical_xmin_entry.pack(side=tk.TOP)
        self.vertical_xmax_entry = tk.Entry(self.ui_canvas, width=19)
        self.vertical_xmax_entry.pack(side=tk.TOP)
        self.vertical_crop_button = tk.Button(self.ui_canvas, text="Crop Vertical", width=17, command=self.crop_vertical)
        self.vertical_crop_button.pack(side=tk.TOP)

        self.reset_limits_button = tk.Button(self.ui_canvas, text="Crop Reset", width=17, command=self.reset_crop)
        self.reset_limits_button.pack(side=tk.TOP)

        # add snapshot button
        self.snapshot_button = tk.Button(self.ui_canvas, text="Take Snapshot", width=17, command=self.take_snapshot)
        self.snapshot_button.pack(side=tk.TOP)


        # Start app
        # ----------------------------------------------------------------------

        # Connect to camera before the update
        self.connect_to_camera()

        # start update loop for app
        self.update()
        self.window.mainloop()


    # APP FUNCTIONS
    # --------------------------------------------------------------------------


    def take_snapshot(self):

        """Saves a single image created from original image of current preview """

        image = PIL.Image.fromarray(self.photo)
        file = filedialog.asksaveasfile(mode="wb", defaultextension=".bmp", filetypes=(("Bitmap File", "*.bmp"),
                                                                                       ("PNG File", "*.png"),
                                                                                       ("JPEG File", "*.jpg"),
                                                                                       ("All Files", "*.*")))
        if file:
            image.save(file)
            print("Image saved!")
        else:
            print("Could not save image!")


    def toggle_video(self):

        """Toggles whether preview video feed is continuous"""

        if self.video_continuous:
            self.continuous_button.config(relief=tk.RAISED, fg="red")
        else:
            self.continuous_button.config(relief=tk.SUNKEN, fg="green")
        self.video_continuous = not self.video_continuous
        self.update()
        return


    def crop_horizontal(self):

        """Crops the image horizontally based on user-input in GUI and redisplays previews"""

        try:
            self.horizontal_xmin = float(self.horizontal_xmin_entry.get())
            self.horizontal_xmax = float(self.horizontal_xmax_entry.get())

            if self.horizontal_xmin >= self.horizontal_xmax:
                print("x_min too big!")
                self.horizontal_xmin = 0

            if self.horizontal_xmin < 0:
                print("x_min cannot be negative!")
                self.horizontal_xmin = None

            if self.horizontal_xmax < 0:
                print("x_max cannot be negative!")
                self.horizontal_xmax = None

        except:
            print("Please enter valid numbers")

        # make preview image and horizontal graph
        self.make_preview_image()
        self.make_horizontal_graph()

        
    def crop_vertical(self):

        """Crops the image vertically based on user-input in GUI and redisplays previews"""

        try:
            self.vertical_xmin = float(self.vertical_xmin_entry.get())
            self.vertical_xmax = float(self.vertical_xmax_entry.get())

            if self.vertical_xmin >= self.vertical_xmax:
                print("x_min too big!")
                self.vertical_xmin = 0

            if self.vertical_xmin < 0:
                print("x_min cannot be negative!")
                self.vertical_xmin = None

            if self.vertical_xmax < 0:
                print("x_max cannot be negative!")
                self.vertical_xmax = None

        except:
            print("Please enter valid numbers")

        # make preview image and vertical graph
        self.make_preview_image()
        self.make_vertical_graph()


    def reset_crop(self, update=True):

        """Resets crop on preview images and graphs"""

        self.vertical_xmin = None
        self.vertical_xmax = None
        self.horizontal_xmin = None
        self.horizontal_xmax = None

        if update:
            self.update_all()


    def make_preview_image(self):

        """Constructs preview image from image array and places in GUI"""

        self.preview = self.video.make_cropped_image(self.photo,
                                                     cmap=self.chosen_filter.get(),
                                                     dpi=self.monitor_dpi,
                                                     resolution=(self.res_x, self.res_y),
                                                     min_x=self.horizontal_xmin,
                                                     max_x=self.horizontal_xmax,
                                                     min_y=self.vertical_xmin,
                                                     max_y=self.vertical_xmax)
        self.image = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(self.preview))
        self.preview_canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        

    def make_horizontal_graph(self):

        """Constructs horizontal intensity graph from image array and places in GUI"""

        graph = self.video.make_graph(self.preview, axis=0, dpi=self.monitor_dpi, graph_height=self.reference_graph_height, min_x=self.horizontal_xmin, max_x=self.horizontal_xmax)
        self.graph1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(graph))
        self.preview_canvas.create_image(0, self.image.height(), image=self.graph1, anchor=tk.NW)


    def make_vertical_graph(self):

        """Constructs vertical intensity graph from image array and places in GUI"""

        graph = self.video.make_graph(self.preview, axis=1, dpi=self.monitor_dpi, graph_height=self.reference_graph_height, min_x=self.vertical_xmin, max_x=self.vertical_xmax)
        self.graph2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(graph))
        self.preview_canvas.create_image(self.image.width(), 0, image=self.graph2, anchor=tk.NW)


    def change_preview_resolution(self):

        """Changes preview resolution according to user selection in drop down menu"""

        # check to see if the preview resolution has been changed
        self.res_x, self.res_y = self.resolutions[self.chosen_res.get()]

        # Update the preview canvas
        self.preview_canvas.config(width=self.res_x + self.reference_graph_height, height=self.res_y + self.reference_graph_height)


    def connect_to_camera(self):

        """Sets video class to connect to chosen camera from drop-down menu"""

        try:
            chosen_camera = self.camera_details[self.chosen_camera.get()]
            print(chosen_camera)
            host_ip = chosen_camera["host_ip"]
            port = int(chosen_camera["port"])
            name = self.chosen_camera.get()
            self.video = VideoCapture(host_ip=host_ip, port=port, cameraname=name)
        except:

            self.chosen_camera.set("Laptop Webcam")
            chosen_camera = self.camera_details[self.chosen_camera.get()]

            print(chosen_camera)
            host_ip = chosen_camera["host_ip"]
            port = int(chosen_camera["port"])
            self.video = VideoCapture(host_ip=host_ip, port=port)


    def open_server_list(self):

        """Opens server list json file in default system text editor"""

        if sys.platform == "win32":
            os.startfile("camera_list.json")
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, "camera_list.json"])


    def update_all(self):

        """Update all elements in the GUI"""

        self.connect_to_camera()
        self.change_preview_resolution()
        self.make_preview_image()
        self.make_horizontal_graph()
        self.make_vertical_graph()


    def update(self):

        """Update loop which checks for user changes and redisplays images"""

        # check if preview res has been changed and update it
        self.change_preview_resolution()

        # Get original-size image
        self.photo = self.video.get_video_frame()

        # get frame from camera and place it in window
        self.make_preview_image()

        # make horizontal graph
        self.make_horizontal_graph()

        # make vertical graph
        self.make_vertical_graph()

        if self.video_continuous:
            self.window.after(self.delay, self.update)
