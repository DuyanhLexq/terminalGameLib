
import os
name = lambda: "win"
def set_terminal_size(width:int, height:int)-> None:
    os.system(f'mode con: cols={width} lines={height}')


def set_terminal_title(title:str)-> None:
    os.system(f'title {title}')