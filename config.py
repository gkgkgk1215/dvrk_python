"""Adjust configuration here for settings, to be loaded in other code.

This is used for surgical robotics and any Python2 code. DO NOT MERGE WITH
load_config in the neural net code.
"""
import os
import cv2
import sys
import time
import pickle
import numpy as np
from os.path import join
import utils as U

# Colors for cv2.
BLUE  = (255,0,0)
GREEN = (0,255,0)
RED   = (0,0,255)

# ---------------------------------------------------------------------------- #
# WHERE DVRK CODE SAVES IMAGES -- must be same as in: image_manip/load_config.py
# ---------------------------------------------------------------------------- #
DVRK_IMG_PATH = 'dir_for_imgs/'

# ---------------------------------------------------------------------------- #
# CALIBRATION FILE
# ---------------------------------------------------------------------------- #

CALIB_FILE = 'tests/mapping_table'
ROW_BOARD = 6
COL_BOARD = 6
CLOTH_HEIGHT = -0.006  # meters

DATA_SQUARE = U.load_mapping_table(row_board=ROW_BOARD,
                                   column_board=COL_BOARD,
                                   file_name=CALIB_FILE,
                                   cloth_height=CLOTH_HEIGHT)

