from instrument_control.camera import Camera
from data_processing.image_processing import Image
import tkinter as tk
import numpy as np
from tkinter import filedialog
import PIL.Image
import PIL.ImageTk
import json
import os, sys, subprocess
import imutils
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time

class Detector_App:

    # APP INITIALISE
    # --------------------------------------------------------------------------
    
    def __init__(self):

        """OOLI User Interface class

        :param window: tk window object
        :param window_title: Title to display in window
        :param fps: Frames per second of preview feed

        """
        # Make resources
        # ----------------------------------------------------------------------

        # It can only really do like 15 fps since it lags
        window = tk.Tk()
        fps=30
        self.delay = int(1000/fps)

        # Temporary placeholder photo array and preview array
        self.photo = None
        self.preview = None
        self.raw_image = np.zeros(1)
        self.imgproc = Image()

        #Camera parameters
        self.camera_connected = tk.BooleanVar()
        self.camera_connected.set(False)
        self.feed_continous = tk.BooleanVar()
        self.feed_continous.set(False)
        self.dir = None


        #Saving parameters
        self.save_dir = 'None'
        self.save_post = tk.BooleanVar()
        self.save_post.set(False)
        self.save_raw = tk.BooleanVar()
        self.save_raw.set(True)
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
        filters = ["jet", "magma", "viridis", "gray", "binary", "nipy_spectral"]
        inter = ['antialiased', 'gaussian', 'bessel','sinc','lanczos']

        # Height of reference graph in pixels
        self.reference_graph_height = 150

        # Initial bounds of graphs
        self.horizontal_xmin = tk.IntVar()
        self.horizontal_xmax = tk.IntVar()
        self.vertical_xmin = tk.IntVar()
        self.vertical_xmax = tk.IntVar()
        

        # Make GUI
        # ----------------------------------------------------------------------
        # make initial window
        self.window = window
        self.window.title('Detector')
        self.window.iconphoto(True, tk.PhotoImage(file="assets/full-spectrum.png"))

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

        self.camera_checkbox = tk.Checkbutton(self.camera_canvas, text='Connect to Camera', variable = self.camera_connected,command=self.check_camera)
        self.camera_checkbox.pack()

        # add take picture button
        self.take_photo_button = tk.Button(self.camera_canvas, text='Take Picture', command=self.take_photo)
        self.take_photo_button.pack()

        # add button to open camera list json file

        self.continous_checkbox = tk.Checkbutton(self.camera_canvas, text='Continous', variable = self.feed_continous,command=self.stream)
        self.continous_checkbox.pack()


        # add camera options
        self.exposuretime = tk.IntVar()
        self.exposuretime.set(100)
        self.exposuretime_scale = tk.Scale(self.camera_canvas, from_=0, to=100, orient=tk.HORIZONTAL)
        self.exposuretime_scale.bind("<ButtonRelease-1>", self.change_cam_exposure)
        self.exposuretime_scale.pack(side=tk.TOP)
        self.exposuretime_label = tk.Label(self.camera_canvas, text='Exposure Time')
        self.exposuretime_label.pack()
        self.gain = tk.IntVar()
        self.gain.set(1)
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


        # add dropdown menu for colourmap
        self.colourmap_dropdown_label = tk.Label(self.drop_canvas, text="Colour Map")
        self.colourmap_dropdown_label.pack()
        self.chosen_filter = tk.StringVar()
        self.chosen_filter.set(filters[0])
        self.filter_selector = tk.OptionMenu(self.drop_canvas, self.chosen_filter, *filters, command=self.change_cmp)
        self.filter_selector.pack()

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

        #add color limits
        self.color_lim_label = tk.Label(self.drop_canvas, text="Color Scale Limits")
        self.cl = tk.StringVar()
        self.cl.set('0')
        self.color_low = tk.Entry(self.drop_canvas, textvariable=self.cl)
        self.ch = tk.StringVar()
        self.ch.set('255')
        self.color_high = tk.Entry(self.drop_canvas, textvariable=self.ch)
        self.color_lim_label.pack()
        self.color_low.pack()
        self.color_high.pack()

        #add Hmask limits
        self.hor_lim_label = tk.Label(self.drop_canvas, text="Horizontal Scale Limits")
        self.hl = tk.StringVar()
        self.hl.set('0')
        self.hor_low = tk.Entry(self.drop_canvas, textvariable=self.cl)
        self.hh = tk.StringVar()
        self.hh.set('5000')
        self.hor_high = tk.Entry(self.drop_canvas, textvariable=self.ch)
        self.hor_lim_label.pack()
        self.hor_low.pack()
        self.hor_high.pack()

        #add color limits
        self.ver_lim_label = tk.Label(self.drop_canvas, text="Vertical Scale Limits")
        self.vl = tk.StringVar()
        self.vl.set('0')
        self.ver_low = tk.Entry(self.drop_canvas, textvariable=self.cl)
        self.vh = tk.StringVar()
        self.vh.set('5000')
        self.ver_high = tk.Entry(self.drop_canvas, textvariable=self.ch)
        self.ver_lim_label.pack()
        self.ver_low.pack()
        self.ver_high.pack()

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

        self.camera = Camera(self.chosen_camera.get()).initiate()
        new_gain = self.camera.get_gain()
        gl, gh = self.camera.get_gain_limits()
        new_expT = self.camera.get_exposure()
        eTl, eTh = self.camera.get_exposure_limits()
        self.camera.set_exposure(new_expT)
        self.camera.set_gain(new_gain)
        self.gain_scale.configure(to = int(gh), from_=int(gl))
        self.gain_scale.set(new_gain)
        self.exposuretime_scale.configure(to = int(eTh), from_=int(eTl))
        self.exposuretime_scale.set(new_expT)


    def disconnect_to_camera(self):
        self.camera.close()

    def savefile(self):
        """Saves a single image created from original image of current preview """

        # image = PIL.Image.fromarray(self.photo)
        file = filedialog.asksaveasfile(mode="wb", defaultextension=".bmp",initialdir=self.save_dir, filetypes=(("Bitmap File", "*.bmp"),
                                                                                       ("PNG File", "*.png"),
                                                                                       ("JPEG File", "*.jpg"),
                                                                                       ("All Files", "*.*")))
        if file:
            if self.save_raw.get()==True:
                self.image.save(file)
            if self.save_post.get()==True:
                plt.savefig(file.split('.')[0] + '_processed.'+ file.split('.')[1])
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
            self.make_preview()
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
        if self.camera_connected.get() == True:
            self.raw_image = self.camera.photo_capture()
            self.make_preview()
            self.image = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(self.preview))
            self.preview_canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        else:
            print('No Connected Camera')

    def make_preview(self):
        cmap = cm.get_cmap(self.chosen_filter.get())
        haxis = np.arange(self.raw_image.shape[1])
        vaxis = np.arange(self.raw_image.shape[0])
        Hmask = (haxis>int(self.hl.get()))*(haxis<int(self.hh.get()))
        Vmask = (vaxis>int(self.vl.get()))*(vaxis<int(self.vh.get())) 
        img = self.imgproc.quick_image(self.raw_image, Hmask = Hmask, Vmask = Vmask, vmin=int(self.cl.get()), vmax=int(self.ch.get()), gamma = self.gamma.get())
        self.preview = np.uint8(cmap(img/int(self.ch.get())))*int(self.ch.get())        
    def check_camera(self):
        if self.camera_connected.get() == True:
            print('It is true')
            self.connect_to_camera()
        if self.camera_connected.get() == False:
            print('It is false')
            self.disconnect_to_camera()

    def stream(self):
        while self.feed_continous.get()==True:
            self.take_photo()
            

    def change_cam_exposure(self,event):
        x = self.exposuretime_scale.get()
        if self.camera_connected.get() == True:
            self.camera.set_exposure(x)
        else:
            print('No camera connected')
    def change_cam_gain(self,event):
        x = self.gain_scale.get()
        if self.camera_connected.get() == True:
            self.camera.set_gain(x)
        else:
            print('No camera connected')

    ########################################################### 
    def change_cmp(self,choice):
        if self.photo != None:
            self.make_preview()
            self.image = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(self.preview))
            self.preview_canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        else:
            print('No Picture to Edit')


    def change_contrast(self,event):
        self.gamma.set(self.contrast_scale.get())
        if self.photo != None:
            self.make_preview()
            self.image = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(self.preview))
            self.preview_canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

        else:
            print('No Picture to Edit')

