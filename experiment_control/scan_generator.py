import numpy as np
import json
import os
import itertools
from PIL import Image
from tqdm import tqdm

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
            stage_list_output[key.name] = [item for sublist in self.stage_list[key] for item in sublist]
        print(stage_list_output)
        with open(os.path.join(self.save_directory, "axis.json"), "w") as f:
            json.dump(stage_list_output, f, indent=4)

        np.savez(os.path.join(self.save_directory, "index_file.npz"), self.axis_array)


    def run_repeats(self, N):
        for i in tqdm(range(N)):

            # image = Image.fromarray(self.detector.photo_capture().astype(np.uint8))
            arr_new =  self.detector.photo_capture().astype(np.uint8)
            filename = os.path.join(self.save_directory, str(i) + ".npy")
            #image.save(filename)
            np.save(filename, arr_new)
            print('Saved', filename)


    def run_scan(self):

        self.make_variable_space()
        flat_lists = [[item for sublist in self.stage_list[key] for item in sublist] for key in list(self.stage_list.keys())]
        combinations = list(itertools.product(*flat_lists))

        stages = list(self.stage_list.keys())
        for i in tqdm(range(len(combinations))):
            
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
            image = Image.fromarray(self.detector.photo_capture().astype(np.uint8))
            arr_new =  self.detector.photo_capture().astype(np.uint8)
            filename = os.path.join(self.save_directory, str(i) + ".npy")
            #image.save(filename)
            np.save(filename, arr_new)
            print(filename)

            # unlock stages
            for j in range(len(stages)):
                stages[j].disable_lock()
