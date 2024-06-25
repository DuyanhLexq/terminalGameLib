

class pair:
    def __init__(self,*args):
        self.first,self.second = args

# Function to convert matching special characters to their counterpart
def convert_coupe_chars(char: str) -> str:
    sp_chars = ["<>", "\/", "[]", r"{}", "()"]
    for sp_char in sp_chars:
        if not char in sp_char: continue
        return sp_char[not sp_char.find(char)]  # Assume the character found is 1 -> !1 = 0
    return char

def first_ele_without_space(string: str) -> int:
    SPACE = " "
    for i in range(len(string)):
        if string[i] != SPACE: return i
    return -1

def last_ele_without_space(string: str) -> int:
    SPACE = " "
    for i in range(len(string)-1, -1, -1):
        if string[i] != SPACE: return i
    return -1

def find_first(string:str,arr:list)-> int:
    for color in arr:
        if string.find(color) != -1: return string.find(color)
    return -1