from __future__ import with_statement
from image_processing.functions import VideoCapture
from image_processing.functions import PhotoCapture
from image_processing.functions import PhotoLoader
import tkinter as tk
from tkinter import filedialog
import PIL.Image
import PIL.ImageTk
import json
import os, sys, subprocess
import imutils
import numpy as np
import matplotlib.pyplot as plt 

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
                                                     cmap=self.chosen_filter,
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
        # self.make_horizontal_graph()
        # self.make_vertical_graph()


    def update(self):

        """Update loop which checks for user changes and redisplays images"""

        # check if preview res has been changed and update it
        self.change_preview_resolution()

        # Get original-size image
        self.photo = self.video.get_video_frame()

        # get frame from camera and place it in window
        self.make_preview_image()

        # make horizontal graph
        # self.make_horizontal_graph()

        # make vertical graph
        # self.make_vertical_graph()

        if self.video_continuous:
            self.window.after(self.delay, self.update)

class Detector_App:

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

        #Camera parameters
        self.camera_connected = tk.BooleanVar()
        self.camera_connected.set(False)
        self.dir = None


        #Saving parameters
        self.save_dir = 'None'
        self.save_post = False
        self.save_raw = False
        self.save_dir=None
        

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
        inter = ['antialiased', 'gaussian', 'bessel','sinc','lanczos']

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
        self.preview_canvas = tk.Canvas(self.window, width=self.res_x+20, height=self.res_y+10)
        self.preview_canvas.grid(row=0, column=0, sticky=tk.N)

        """________UI Canvases___________________________"""
        # add a canvas in which all the buttons will sit
        self.camera_canvas = tk.Frame(self.window)
        self.camera_canvas.grid(row=0, column=1, sticky=tk.N, pady=0)
        self.post_canvas = tk.Frame(self.window)
        self.post_canvas.grid(row=1, column=0, sticky=tk.N, pady=0)
        self.save_canvas = tk.Frame(self.window)
        self.save_canvas.grid(row=1, column=1, sticky=tk.N, pady=0)

        # add a dropdown menu for selecting camera
        """_________Camera Options________________________"""
        self.camera_select_label = tk.Label(self.camera_canvas, text="Select Camera")
        self.camera_select_label.pack(side=tk.TOP)
        camera_list = list(self.camera_details.keys())
        self.chosen_camera = tk.StringVar()
        self.chosen_camera.set(camera_list[0])
        self.camera_selector = tk.OptionMenu(self.camera_canvas, self.chosen_camera, *camera_list)
        self.camera_selector.config(width=15, anchor=tk.CENTER)
        self.camera_selector.pack()

        # add button to open camera list json file
        self.add_camera_button = tk.Button(self.camera_canvas, text="Open Server List", width=17, command=self.open_server_list)
        self.add_camera_button.pack()
        self.camera_checkbox = tk.Checkbutton(self.camera_canvas, text='Connect to Camera', variable = self.camera_connected,command=self.check_camera)
        self.camera_checkbox.pack()

        # add take picture button
        self.take_photo_button = tk.Button(self.camera_canvas, text='Take Picture', command=self.take_photo)
        self.take_photo_button.pack()
        # add camera options
        self.exposuretime_scale = tk.Scale(self.camera_canvas, from_=0, to=100, orient=tk.HORIZONTAL)
        self.exposuretime_scale.bind("<ButtonRelease-1>", self.change_cam_exposure)
        self.exposuretime_scale.pack(side=tk.TOP)
        self.exposuretime_label = tk.Label(self.camera_canvas, text='Exposure Time')
        self.exposuretime_label.pack()
        self.gain_scale = tk.Scale(self.camera_canvas, from_=0, to=100, orient = tk.HORIZONTAL)
        self.gain_scale.bind("<ButtonRelease-1>", self.change_cam_gain)
        self.gain_scale.pack(side=tk.TOP)
        self.gain_label = tk.Label(self.camera_canvas, text='Gain')
        self.gain_label.pack()

        # add loading picture from file option
        self.dir_button = tk.Button(self.camera_canvas, text = 'Choose File Directory', command = self.dir_selector)
        self.dir_button.pack()
        self.dir_text = tk.StringVar()
        self.dir_text.set('Current Directory')
        self.dir_label = tk.Label(self.camera_canvas, textvariable=self.dir_text, width=20, anchor=tk.E)
        self.dir_label.pack()
        self.loadfile_button = tk.Button(self.camera_canvas, text = 'Load File', command=self.loadfile, initialdir=self.dir)
        self.loadfile_button.pack()

        """___________PostProcessing Options_________________"""
        # Creating Smaller Canvases inside
        self.drop_canvas = tk.Frame(self.post_canvas)
        self.drop_canvas.grid(row=0, column=0, sticky=tk.W, pady=3)
        self.scale_canvas = tk.Frame(self.post_canvas)
        self.scale_canvas.grid(row=0, column=1, sticky=tk.E, pady=3)

        # add dropdown menu for preview resolution
        self.resolution_dropdown_label = tk.Label(self.drop_canvas, text="Preview Resolution")
        self.resolution_dropdown_label.pack()
        res_list = list(self.resolutions.keys())
        self.chosen_res = tk.StringVar()
        self.chosen_res.set("854x480 (16:9)")
        self.res_selector = tk.OptionMenu(self.drop_canvas, self.chosen_res, *res_list)
        self.res_selector.config(width=15, anchor=tk.CENTER)
        self.res_selector.pack()

        # add dropdown menu for colourmap
        self.colourmap_dropdown_label = tk.Label(self.drop_canvas, text="Colour Map")
        self.colourmap_dropdown_label.pack()
        self.chosen_filter = tk.StringVar()
        self.chosen_filter.set(filters[0])
        self.filter_selector = tk.OptionMenu(self.drop_canvas, self.chosen_filter, *filters, command=self.change_cmp)
        self.filter_selector.pack()

        # add dropdown menu for interpolation
        self.inter_dropdown_label = tk.Label(self.drop_canvas, text="Interpolation Map")
        self.inter_dropdown_label.pack()
        self.chosen_inter = tk.StringVar()
        self.chosen_inter.set(inter[0])
        self.inter_selector = tk.OptionMenu(self.drop_canvas, self.chosen_inter, *inter, command=self.change_inter)
        self.inter_selector.pack()

        # add processing scales

        #add scale for contrast
        self.gamma=tk.DoubleVar()
        self.gamma.set(1)
        self.contrast_scale = tk.Scale(self.scale_canvas, from_=1, to=0.01, orient=tk.HORIZONTAL, resolution=0.01)
        self.contrast_scale.set(1)
        self.contrast_scale.bind("<ButtonRelease-1>", self.change_contrast)
        self.contrast_scale.grid(column=0, row=0)
        self.contrast_label = tk.Label(self.scale_canvas, text='Contrast')
        self.contrast_label.grid(column=0,row=1)

        #add scale for vmax
        self.vmax=tk.IntVar()
        self.vmax.set(255)
        self.vmax_scale = tk.Scale(self.scale_canvas, from_=1, to=255, orient=tk.HORIZONTAL)
        self.vmax_scale.set(255)
        self.vmax_scale.bind("<ButtonRelease-1>", self.change_vmax)
        self.vmax_scale.grid(column=1, row=0)
        self.vmax_label = tk.Label(self.scale_canvas, text='Max Value')
        self.vmax_label.grid(column=1,row=1)

        """___________Saving Options______________________________________"""
        # add snapshot button
        self.savedir_button = tk.Button(self.save_canvas, text = 'Choose Save File Directory', command = self.savedir_selector)
        self.savedir_button.pack()

        self.savedir_text = tk.StringVar()
        self.savedir_text.set('Current Directory')
        self.savedir_label = tk.Label(self.save_canvas, textvariable=self.savedir_text)
        self.savedir_label.pack()
        
        self.raw_saving = tk.Checkbutton(self.save_canvas, text='Raw', variable=self.save_raw)
        self.raw_saving.pack()
        
        self.post_saving = tk.Checkbutton(self.save_canvas, text='Processed', variable=self.save_post)
        self.post_saving.pack()
        self.savefile_button = tk.Button(self.save_canvas, text = 'Save', command=self.savefile, initialdir=self.save_dir)
        self.savefile_button.pack()
        # Start app
        # ----------------------------------------------------------------------

       
        # start update loop for app
        # self.update()
        self.window.mainloop()


    # APP FUNCTIONS
    # --------------------------------------------------------------------------


    def connect_to_camera(self):
        """Sets video class to connect to chosen camera from drop-down menu"""
        try:
            chosen_camera = self.camera_details[self.chosen_camera.get()]
            host_ip = chosen_camera["host_ip"]
            port = int(chosen_camera["port"])
            camera_type = chosen_camera['cam_type']
            name = self.chosen_camera.get()
            self.camera = PhotoCapture(host_ip=host_ip, port=port, cameraname=name, cameratype=camera_type)
        except:

            self.chosen_camera.set("Laptop Webcam")
            chosen_camera = self.camera_details[self.chosen_camera.get()]
            host_ip = chosen_camera["host_ip"]
            port = int(chosen_camera["port"])
            camera_type = 'webcam'
            self.camera = PhotoCapture(host_ip=host_ip, port=port, cameratype=camera_type)

        self.gain_scale.configure(to = self.camera.gain_max, from_=self.camera.gain_min)
        self.exposuretime_scale.configure(to = self.camera.exposuretime_max, from_=self.camera.exposuretime_min)



    def disconnect_to_camera(self):
        self.camera.release()


    def open_server_list(self):

        """Opens server list json file in default system text editor"""

        if sys.platform == "win32":
            os.startfile("camera_list.json")
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, "camera_list.json"])


    def update(self):

        """Update loop which checks for user changes and redisplays images"""
        pass

    def savefile(self):
        """Saves a single image created from original image of current preview """

        # image = PIL.Image.fromarray(self.photo)
        file = filedialog.asksaveasfile(mode="wb", defaultextension=".bmp",initialdir=self.save_dir, filetypes=(("Bitmap File", "*.bmp"),
                                                                                       ("PNG File", "*.png"),
                                                                                       ("JPEG File", "*.jpg"),
                                                                                       ("All Files", "*.*")))
        if file:
            # image.save(file)
            print("Image saved!")
        else:
            print("Could not save image!")
   
    def loadfile(self):
        """Saves a single image created from original image of current preview """

        file = filedialog.askopenfilename(defaultextension=".bmp", filetypes=(("Bitmap File", "*.bmp"),
                                                                                       ("PNG File", "*.png"),
                                                                                       ("JPEG File", "*.jpg"),
                                                                                       ("All Files", "*.*")))

        if file:            
            self.photo = PIL.Image.open(file)
            self.camera = PhotoLoader()
            self.camera_connected.set(False)
            self.preview = self.camera.make_cropped_image(self.photo,cmap=self.chosen_filter.get(),dpi=self.monitor_dpi,resolution=(self.res_x,self.res_y), gamma = self.gamma.get(), vmax=self.vmax.get()) 
            self.image = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(self.preview))
            self.preview_canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
            print("Image {} opened!".format(file))
        else:
            print("Could not open image!")

    def dir_selector(self):
        self.dir = filedialog.askdirectory(initialdir=os.getcwd())
        self.dir_text.set('Load file from: '+ self.dir)

    def savedir_selector(self):
        self.save_dir = filedialog.askdirectory(initialdir=os.getcwd())
        self.savedir_text.set('Saving to '+self.save_dir)

    def take_photo(self):
        # if self.camera_connected.get() == True:
        try:
            self.photo = PIL.Image.fromarray(self.camera.get_photo())

            self.preview = self.camera.make_cropped_image(self.photo,cmap=self.chosen_filter.get(),dpi=self.monitor_dpi,resolution=(self.res_x,self.res_y), gamma = self.gamma.get(), vmax=self.vmax.get()) 
            self.image = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(self.preview))
            self.preview_canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        # else:
        except:
            print('No Connected Camera')

    def check_camera(self):
        if self.camera_connected.get() == True:
            self.connect_to_camera()
        if self.camera_connected.get() == False:
            self.disconnect_to_camera()

    def change_cam_exposure(self,event):
        x = self.exposuretime_scale.get()
        if self.camera_connected.get() == True:
            self.camera.change_exposure(x)
        else:
            print('No camera connected')
    def change_cam_gain(self,event):
        x = self.gain_scale.get()
        if self.camera_connected.get() == True:
            self.camera.change_gain(x)
        else:
            print('No camera connected')

    def change_cmp(self,choice):
        if self.photo != None:
            self.preview = self.camera.make_cropped_image(self.photo,cmap=self.chosen_filter.get(),dpi=self.monitor_dpi,resolution=(self.res_x,self.res_y), gamma = self.gamma.get(), vmax=self.vmax.get()) 
            self.image = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(self.preview))
            self.preview_canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        else:
            print('No Picture to Edit')

    def change_inter(self,choice):
        if self.photo != None:
            self.preview = self.camera.make_cropped_image(self.photo,cmap=self.chosen_filter.get(),dpi=self.monitor_dpi,resolution=(self.res_x,self.res_y), gamma = self.gamma.get(), vmax=self.vmax.get()) 
            self.image = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(self.preview))
            self.preview_canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        else: 
            print('No Picture to Edit')

    def change_contrast(self,event):
        self.gamma.set(self.contrast_scale.get())
        if self.photo != None:
            self.preview = self.camera.make_cropped_image(self.photo,cmap=self.chosen_filter.get(),dpi=self.monitor_dpi,resolution=(self.res_x,self.res_y), gamma = self.gamma.get(), vmax=self.vmax.get()) 
            self.image = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(self.preview))
            self.preview_canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

        else:
            print('No Picture to Edit')

    def change_vmax(self,event):
        self.vmax.set(self.vmax_scale.get())
        if self.photo != None:
            self.preview = self.camera.make_cropped_image(self.photo,cmap=self.chosen_filter.get(),dpi=self.monitor_dpi,resolution=(self.res_x,self.res_y), gamma = self.gamma.get(), vmax=self.vmax.get()) 
            self.image = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(self.preview))
            self.preview_canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

        else:
            print('No Picture to Edit')
