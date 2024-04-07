""" 
This is our main driver file. It will be responsible for handling user input and displaying the curent 
GameState object.
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512 
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15 #for animations 
IMAGES = {}

"""
Initalize a global dictionary of images. This will be called exactly once in the main
"""

def load_images():
    pieces = 