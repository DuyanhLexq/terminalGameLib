import re
import copy
from colorama import Fore
from .baseFuncAndClass import pair
from .baseFuncAndClass import find_first
from .baseFuncAndClass import first_ele_without_space
from.baseFuncAndClass import last_ele_without_space
from .baseFuncAndClass import convert_coupe_chars



class terminalObject:
    def __init__(self):
        self.x:int
        self.y:int
        self.width:int
        self.height:int

# Class to represent a terminal object with position and ASCII image properties
class terminalObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ascii_Image = 'unknown'
        self.ascii_Image_map = []
        self.current_ascii_Image_map = []
        self.is_fill_blocks = []
        self.color_map = []
        self.width = 0
        self.height = 0
        self.background = True

    # Static method to calculate width and height of an ASCII image
    @staticmethod
    def caculate_width_height(ascii_Image: str) -> list:
        width = height = 0
        '''order [width, height]'''
        width = max(len(child_image) for child_image in ascii_Image.split("\n"))
        height = len(ascii_Image.split("\n"))
        return width, height
    @staticmethod
    def fill_color(ascii_Image_map:list[str])-> list:
        '''fill color for image'''
        temp_map = []
        for child in ascii_Image_map:
            temp_map.append(list(child))
        
        color = "unkown"
        is_fill = False
        colors = {
            "r":Fore.LIGHTRED_EX,
            'b':Fore.LIGHTBLUE_EX,
            'y':Fore.LIGHTYELLOW_EX,
            'w':Fore.LIGHTWHITE_EX,
            'p':Fore.LIGHTMAGENTA_EX,
            'rs':Fore.RESET
        }
        for i in range(len(ascii_Image_map)):

            for j in range(len(ascii_Image_map[i])-1,-1,-1):
                    if ascii_Image_map[i][j] != ' ':
                          pos = j
                          break
                    else:pos = 0

            temp_map[i][pos] = temp_map[i][pos] + colors['rs']


            pattern = r'<(?:r|b|y|w|p|rs)>'
            matches = re.finditer(pattern,ascii_Image_map[i])
            ele = []
            if is_fill:
                match = re.search(r'\S', ascii_Image_map[i])
                if match:
                     temp_map[i][match.start()] = colors[color] + temp_map[i][match.start()] 

            if matches:
                ele = [match.start() for match in matches]
                for pos in ele:
                    try:
                        color_code = ascii_Image_map[i][pos+1]
                        is_fill = True
                        color = color_code
                        temp_map[i][pos],temp_map[i][pos+1] = " "," "
                        temp_map[i][pos+2] = " " +colors[color]

                    except  Exception as Bug:
                         print(Bug)
                         return
                    
        return temp_map
    
    @staticmethod
    def create_fill_color_map(fill_color_map:list[list[str]])-> list:
        colors_data = [Fore.LIGHTRED_EX,Fore.LIGHTGREEN_EX,Fore.LIGHTYELLOW_EX,Fore.LIGHTBLUE_EX,Fore.LIGHTMAGENTA_EX,Fore.RESET]
        temp_map = copy.deepcopy(fill_color_map)
        res = [[pair]*len(child) for child in temp_map]
        color_code = ''
        for i in range(len(temp_map)):
            for j in range(len(temp_map[i])):
                temp_str = temp_map[i][j]
                first = find_first(temp_str,colors_data)
                if first == 0:
                    color_code = temp_str[0:5]
                    last = find_first(temp_str[first+1:],colors_data) + 5 #không tìm thấy khi = 4
                    res[i][j] = pair(color_code,temp_str[last:last+5] if last != 4 else colors_data[-1])
                    if last != 4: color_code = temp_str[last:last+5]

                elif first != -1:
                    last = find_first(temp_str[first+1:],colors_data) + 5
                    res[i][j]  = pair(color_code,Fore.RESET)
                    if last == 4:
                        color_code = temp_str[first:first+5]
                else:
                    res[i][j] = pair(color_code,Fore.RESET)

        return res
    
    def create_color_map_and_ascii_map_without_colorcode(self,fill_color_map:list)-> list[list]:
        '''handle color and remove color code from ascii_Image_map'''
        color_map = self.create_fill_color_map(fill_color_map)
        pattern = r'\x1b\[91m|\x1b\[92m|\x1b\[93m|\x1b\[94m|\x1b\[95m|\x1b\[39m'
        # Iterate through the nested list and apply re.subn to each string element
        for i in range(len(fill_color_map)):
            for j in range(len(fill_color_map[i])):
                if isinstance(fill_color_map[i][j], str):  # Check if dt[i][j] is a string
                    fill_color_map[i][j], num_subs = re.subn(pattern, '', fill_color_map[i][j])

        return color_map,fill_color_map


    # Static method to remove background spaces from the ASCII image
    @staticmethod
    def remove_bg(is_fill_blocks: list[list], ascii_Image_map: list[str]) -> None:

        for i in range(len(ascii_Image_map)):
            f_e, l_e = first_ele_without_space(ascii_Image_map[i]), last_ele_without_space(ascii_Image_map[i])
            if f_e == -1 or l_e == -1: continue
            for j in range(f_e, l_e+1): is_fill_blocks[i][j] = 1

    # Method to handle background removal
    def handle_bg(self) -> None:
        '''remove background'''
        if self.background: return
        self.is_fill_blocks = [[0]*self.width for _ in range(self.height)]
        self.remove_bg(self.is_fill_blocks, self.current_ascii_Image_map)

    # Method to add an ASCII image from a file
    def add_asciiImage(self, path: str, background=True) -> None:
        self.background = background
        with open(path, 'r') as file:
            self.ascii_Image = file.read()
        # Calculate width, height
        self.width, self.height = self.caculate_width_height(self.ascii_Image)

        for child_Image in self.ascii_Image.split("\n"):
            self.current_ascii_Image_map.append(
                child_Image + ' '*(self.width-len(child_Image))
            )
        #handle color and remove color code from ascii_Image_map
        self.color_map,self.current_ascii_Image_map = self.create_color_map_and_ascii_map_without_colorcode(self.fill_color(self.current_ascii_Image_map))
        self.ascii_Image_map = copy.deepcopy(self.current_ascii_Image_map)
        # Handle background
        self.handle_bg()
    
    def reverse_color(self)-> None:
        for i in range(self.height):
            for j in range(self.width//2):
                oposite = self.width-j-1
                self.color_map[i][j],self.color_map[i][oposite] = self.color_map[i][oposite],self.color_map[i][j]

    # Method to reverse the ASCII image horizontally
    def reverse(self) -> None:
        '''this function could change the ascii_Image_map value not ascii_Image'''
        temp_map = copy.deepcopy(self.current_ascii_Image_map)
        for i in range(len(temp_map)):
            temp_map[i] = list(temp_map[i])
        
        for i in range(self.height):
            j = 0
            while j < self.width//2:
                oposite = self.width-j-1         
                temp_map[i][j], temp_map[i][oposite] = convert_coupe_chars(temp_map[i][oposite]), convert_coupe_chars(temp_map[i][j])
                j+= 1

        for i in range(len(temp_map)):
            temp_map[i] = ''.join(temp_map[i])

        self.current_ascii_Image_map = temp_map
        # Handle background after reversing
        self.handle_bg()
        #reverse color after reversing
        self.reverse_color()


    # Method to check if this object collides with another object
    def colliderect(self, obj: terminalObject) -> bool:
        x1_rect1, x2_rect1 = self.x, self.x+self.width-1
        y1_rect1, y2_rect1 = self.y, self.y+self.height-1
        #------------------------
        x1_rect2, x2_rect2 = obj.x, obj.x+obj.width-1
        y1_rect2, y2_rect2 = obj.y, obj.y+obj.height-1

        con1 = x1_rect1 < x2_rect2
        con2 = x1_rect2 < x2_rect1
        con3 = y1_rect1 < y2_rect2
        con4 = y1_rect2 < y2_rect1

        return con1 and con2 and con3 and con4
