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
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ','bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) 
        #Note: we can access an image by saying 'IMAGES['wP']'
    
"""
The main function. This will handle user input and updating graphics. 
"""

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState() 
    load_images() #only do this once, before the while loop 
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.Quit:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip() 

"""
Responsible for all the graphics within a current game state. 
"""

def drawGameState(screen, gs): 
    drawBoard(screen) #draw squares on the board
    drawPieces(screen, gs.board) #draw pieces on top of squares

def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION): 
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board): 

    if __name__ == "__main__":
        main() 