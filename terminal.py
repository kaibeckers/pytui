import os

# util
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def convertColorToAnsiFg(color):
    match color:
        case 0: return 30
        case 1: return 31
        case 2: return 32
        case 3: return 33
        case 4: return 34
        case 5: return 35
        case 6: return 36
        case 7: return 37
        case 8: return 90
        case 9: return 91
        case 10: return 92
        case 11: return 93
        case 12: return 94
        case 13: return 95
        case 14: return 96
        case 15: return 97
        
        case _: return 97

def convertColorToAnsiBg(color):
    match color:
        case 0: return 40
        case 1: return 41
        case 2: return 42
        case 3: return 43
        case 4: return 44
        case 5: return 45
        case 6: return 46
        case 7: return 47
        case 8: return 48
        case 9: return 49        
        case _: return 49

# terminal interaction
class Terminal:
    def __init__(self):
        cls()
        self.buffer = []
        self.oldBuffer = [] # Used to store the previous frame

    def getTerminalSize(self):
        columns, lines = os.get_terminal_size()
        return columns, lines

    def clearBuffer(self):
        self.buffer = []

    def setPixel(self, x, y, char, fgColor=15, bgColor=None):
        if len(char) > 1:
            for i, c in enumerate(char):
                self.buffer.append((x+i, y, fgColor, bgColor, c))
        else:
            self.buffer.append((x, y, fgColor, bgColor, char))

    def clearCell(self, x, y):
        for i, (x_, y_, _, _, _) in enumerate(self.buffer):
            if x_ == x and y_ == y:
                self.buffer.pop(i)
                return

    def render(self):
        # get diff between old and new buffer
        diff = [x for x in self.buffer if x not in self.oldBuffer]

        # if pixel removed, add it to diff? does this work already?

        # render diff with ANSI escape codes
        for x, y, fgColor, bgColor, char in diff:
            color = convertColorToAnsiFg(fgColor) if bgColor is None else f"{convertColorToAnsiBg(bgColor)};{convertColorToAnsiFg(fgColor)}"
            print(f"\033[{y};{x}H\033[{color}m{char}\033[0m")

        self.oldBuffer = self.buffer.copy()
    
term = Terminal()
term.setPixel(1, 1, " WARN ", 15, 3)
term.setPixel(1, 2, " INFO ", 15, 2)
term.setPixel(1, 3, " ERROR ", 15, 1)
term.setPixel(1, 4, " DEBUG ", 15, 4)
term.render()
