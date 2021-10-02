from __future__ import with_statement
from gui import gui
from image_processing.functions import VideoCapture
import tkinter as tk
from tkinter import filedialog
import PIL.Image
import PIL.ImageTk
import json
import os, sys, subprocess
import cv2

if __name__ == "__main__":
    gui.Camera_App(tk.Tk(), "OOLI", fps=30)
