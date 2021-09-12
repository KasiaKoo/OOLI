from functions import VideoCapture
import tkinter as tk
import cv2
import PIL.Image
import PIL.ImageTk

class Camera_App:
    def __init__(self, window, window_title, host_ip="0.0.0.0", port=9999, dummy=False, fps=30):

        # Get resources
        # ----------------------------------------------------------------------
        # for testing purposes
        self.dummy = dummy

        # Connect to video feed
        self.video = VideoCapture(host_ip=host_ip, port=port, dummy=self.dummy)

        # It can only really do like 15 fps since it lags
        self.delay = int(1000/fps)


        # Make GUI
        # ----------------------------------------------------------------------
        self.window = window
        self.window.title(window_title)

        self.canvas = tk.Canvas(window, width=1920, height=1080)
        self.canvas.pack()

        self.update()

        self.window.mainloop()

    
    def update(self):
        frame = self.video.get_data()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

            

if __name__ == "__main__":
    Camera_App(tk.Tk(), "Camera App", dummy=True, fps=30, host_ip="10.198.202.145", port=9999)
