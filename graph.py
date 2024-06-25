import sys
import platform
from time import sleep
from .terminalObject import terminalObject

# Determine which module to use based on the operating system
if platform.system() == 'Windows': from.win_funcs import *
else: from .linux_funcs import *


class display:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.caption = ""
        self.map = []

    # Method to set the screen size
    def set_mode(self, width: int, height: int) -> None:
        '''set screen size'''
        self.width, self.height = width, height
        set_terminal_size(self.width, self.height)
        self.map = [[" "]*self.width for _ in range(self.height)]

    # Method to set the screen title
    def set_caption(self, text: str) -> None:
        '''set caption'''
        self.caption = text
        set_terminal_title(text)

    # Method to refresh the screen
    def refresh(self) -> None:
        '''refresh screen'''
        self.map = [[" "]*self.width for _ in range(self.height)]
    #Method to fill color
    
    # Method to draw an object on the screen
    def blit(self, obj: terminalObject) -> None:
        for i in range(obj.height):
            for j in range(obj.width):
                x, y = obj.x + j, obj.y + i
                if obj.is_fill_blocks[i][j]:  # Check if the block is filled
                    self.map[y][x] = obj.color_map[i][j].first + obj.current_ascii_Image_map[i][j] + obj.color_map[i][j].second
    @staticmethod
    def clear_screen()-> None:
        '''clear_screen'''
        sys.stdout.write('\x1b[2J\x1b[1;1H')
        sys.stdout.flush()
    
    def draw_map(self)-> None:
        for i in range(self.height):
            for j in range(self.width):
                sys.stdout.write(self.map[i][j])
            sys.stdout.write("\n")

    # Method to update the screen at a given frequency
    def update(self, frequency=0.1)-> None:
        sleep(frequency)
        # Update screen
        self.clear_screen()
        #draw map
        self.draw_map()