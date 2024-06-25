import os

name = lambda: "linux"
def set_terminal_size(width:int, height:int)-> None:
    os.system(f'printf "\e[8;{height};{width}t"')

def set_terminal_title(title:str)-> None:
    os.system(f'echo -ne "\033]0;{title}\007"')