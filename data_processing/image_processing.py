import numpy as np

class Image():
    def __init__(self):
        self.image = np.zeros((2,2))
        self.image_raw = np.zeros((2,2))
        self.bg = np.zeros((2,2))
        self.vlim = (None, None)
        self.cmap ='magma'
        self.gamma = 1
        self.Hmask = []
        self.Vmask = []
        
    def load_image(self, image_array):
        self.image = image_array
        self.image_raw = self.image
        return self

    def load_bg_array(self, bg_array):
        self.bg = bg_array
        return self

    def extract_bg(self, bg_lim = [0,500,10,10]):
        x,y,w,h = bg_lim
        bg_val = np.median(self.image[y:y+h, x:x+w])
        self.bg = bg_val*np.ones(self.image.shape)
        return self

    def sub_bg(self):
        self.image = self.image - self.bg 
        return self


    def remove_dead_pix(self):
        sorted_flt = sorted(self.image.flatten())
        rouge_pixel = np.argwhere(np.array(np.diff(sorted_flt))>max(sorted_flt)/10)
        if len(rouge_pixel) !=0:
            cutoff = sorted_flt[int(min(rouge_pixel))]
            self.image[self.image>cutoff]=0
        return self

    def set_vlim(self, low, high):
        self.image[self.image<low] = low
        self.image[self.image>high] = high
        self.vlim = (low, high)

    def improve_contrast(self, gamma):
        self.gamma = gamma
        max_pix = max(abs(self.image.flatten()))
        if max_pix != 0:
            self.image = ((self.image/max_pix)**self.gamma)*max_pix

        return self
    
    def apply_mask(self, Hmask, Vmask):
        self.image = self.image[Vmask, :]
        self.image = self.image[:,Hmask]
        self.Hmask = Hmask
        self.Vmask = Vmask
        return self

    def set_cmap(self, cmap):
        self.cmap = cmap
    
    def quick_image(self, image_array, gamma, Hmask, Vmask, vmin, vmax):
        self.load_image(image_array)
        self.apply_mask(Hmask, Vmask)
        self.set_vlim(vmin,vmax)
        self.remove_dead_pix()
        self.improve_contrast(gamma)
        return self.image


