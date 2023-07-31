from matplotlib.cbook import file_requires_unicode
import numpy as np
import json
import pandas as pd
import os
import itertools
from PIL import Image
from tqdm import tqdm
import csv
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy.interpolate import interp2d
import time

class ScanGenerator:
    def __init__(self):
        self.detector = None
        self.stage_list = {}
        self.save_directory = ""
        self.axis_array = None


    def set_detector(self, camera_object):
        self.detector = camera_object


    def set_save_directory(self, path, name):
        if os.path.exists(path):
            self.save_directory = os.path.join(path, name)

            if not os.path.exists(self.save_directory):
                os.makedirs(self.save_directory)

        else: 
            raise Exception("Parent directory does not exist!")


    def add_axis(self, stage_object, position_list):
        self.stage_list.setdefault(stage_object, []).append(position_list)


    def make_variable_space(self):
        dimensions = [len([item for sublist in self.stage_list[key] for item in sublist]) for key in list(self.stage_list.keys())]
        self.axis_array = np.linspace(0, np.product(dimensions)-1, np.product(dimensions)).reshape(dimensions)
        

    def output_config(self):
        stage_list_output = {}

        flat_lists = [[item for sublist in self.stage_list[key] for item in sublist] for key in list(self.stage_list.keys())]

        for key in list(self.stage_list.keys()):
            stage_list_output[key.name] = [float(item) for sublist in self.stage_list[key] for item in sublist]
        print(stage_list_output)
        print(type(stage_list_output))
        np.savez(os.path.join(self.save_directory, "index_file.npz"), self.axis_array)
        with open(os.path.join(self.save_directory, "axis.json"), "w") as f:
            json.dump(stage_list_output, f, indent=4)



    def run_repeats(self, N):
        for i in tqdm(range(N)):

            timestamp = time.strftime("-%Y%m%d-%H%M%S")
            # image = Image.fromarray(self.detector.photo_capture().astype(np.uint8))
            arr_new =  self.detector.photo_capture().astype(np.uint16)
            filename = os.path.join(self.save_directory, str(i)+timestamp +  ".npy")
            #image.save(filename)
            np.save(filename, arr_new)
            print('Saved', filename)


    def run_scan(self, repeat=1):

        self.make_variable_space()
        flat_lists = [[item for sublist in self.stage_list[key] for item in sublist] for key in list(self.stage_list.keys())]
        combinations = list(itertools.product(*flat_lists))

        stages = list(self.stage_list.keys())
        for i in tqdm(range(len(combinations))):
            timestamp = time.strftime("-%Y%m%d-%H%M%S")
            
            combination = combinations[i]

            # move stages
            for j in range(len(stages)):
                if np.round(stages[j].get_position(),1) != np.round(combination[j],1):
                    stages[j].set_position(combination[j])

            # wait for stages to finish and lock stages
            for j in range(len(stages)):
                stages[j].enable_lock()
                print(stages[j].get_position())

            # take photo
            # image = Image.fromarray(self.detector.photo_capture_repeat(repeat).astype(np.uint8))
            arr_new =  self.detector.photo_capture_repeat(repeat).astype(np.uint16)
            filename = os.path.join(self.save_directory, str(i)+timestamp + ".npy")
            #image.save(filename)
            np.save(filename, arr_new)
            print(filename)

            # unlock stages
            for j in range(len(stages)):
                stages[j].disable_lock()


    def run_scan_spec(self, no_averaging, lowest_wl= 0, highest_wl = 2000):

        self.make_variable_space()
        flat_lists = [[item for sublist in self.stage_list[key] for item in sublist] for key in list(self.stage_list.keys())]
        combinations = list(itertools.product(*flat_lists))

        stages = list(self.stage_list.keys())
        data_dict = {}
        x,y = self.detector.get_spec()
        mask_wl = (x>lowest_wl)*(x<highest_wl)
        data_dict['wavelength'] = x[mask_wl]
        for i in tqdm(range(len(combinations))):
            
            combination = combinations[i]

            # move stages
            for j in range(len(stages)):
                if np.round(stages[j].get_position(),decimals=4) != np.round(combination[j],decimals=4):
                    stages[j].set_position(combination[j])

            # wait for stages to finish and lock stages
            for j in range(len(stages)):
                stages[j].enable_lock()
                print(stages[j].get_position())

            # take spectrum



            all_y = []
            for i in range(no_averaging):
                x, y= self.detector.get_spec()
                all_y.append(y)
            spec = np.mean(np.array(all_y),axis=0)

            data_dict[np.round(stages[j].get_position(), decimals=4)] = spec[mask_wl] 

            # unlock stages
            for j in range(len(stages)):
                stages[j].disable_lock()


        #Saving to csv
        filename = os.path.join(self.save_directory, "data.csv")
        filename_pic = os.path.join(self.save_directory, "trace.png")
        filename_txt = os.path.join(self.save_directory, 'trace_info.txt')
        df = pd.DataFrame.from_dict(data_dict)
        df.to_csv(filename)

        print('saved', filename)
        #Saving to image
        wl_nm = df['wavelength'].to_numpy()
        pos_mm = df.columns.to_numpy()[1:].astype('float') 
        delay_mm = 2*(pos_mm -pos_mm[0])
        delay_fs = (delay_mm/3)*1e4
        X,Y = np.meshgrid(3e5/wl_nm,delay_fs)

        df_data = df.drop('wavelength', axis = 1)
        img_arr = df_data.to_numpy()
        fig, ax = plt.subplots(2, sharex = True)
        ax[0].pcolormesh(Y,X, img_arr.T, norm=LogNorm())
        ax[1].pcolormesh(Y,X, img_arr.T, norm=LogNorm(), shading='gouraud')
        ax[1].set_xlabel('Time delay [fs]')
        ax[1].set_ylabel('Frquency [THz]')
        plt.tight_layout()
        plt.savefig(filename_pic)

        #saving to text
        np.savetxt(filename_txt, img_arr.T, delimiter='\t')
        wl = df['wavelength'].to_numpy()
        steps = df_data.columns.to_numpy().astype('float')
        no_points = len(steps)
        no_wl = len(wl)
        delay_increment_mm = 2*(steps[1]-steps[0])
        delay_increment_fs = (delay_increment_mm*1e-3/3e8)*1e15
        wl_increment_nm = wl[1]-wl[0]
        middle_wl = wl[len(wl)//2]
        first_line = '{}\t{}\t{}\t{}\t{}'.format(no_points, no_wl, delay_increment_fs, wl_increment_nm, middle_wl)
        with open(filename_txt, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(first_line.rstrip('\r\n') + '\n' + content)

