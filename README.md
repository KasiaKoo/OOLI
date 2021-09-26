# Open Optics Laboratory Interface (OOLI)

## About this Project
OOLI is an open-source software project for managing and interfacing with
socketed data from detection devices.

## Features
- Manage and edit a server list for connection to different devices
- Camera viewer app for viewing images from detectors

## Usage
- Make the conda environment using:
```sh
conda env create -f environment.yml
conda activate camera-viewer
```
- Then run the app using:
```sh
python gui.py
```

## Todo
- [ ] Make environment system agnostic
- [ ] Merge socketing project
- [ ] Add beam measurement feature

## License
This project is licensed under the terms of the GNU General Public License v3.0.
