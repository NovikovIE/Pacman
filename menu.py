from button import Button
from config import BUTTONWIDTH, BUTTONHEIGHT, BUTTONCOLOR, BUTTONPOSITION, TEXTMENUPOSITION


# has 3 variations of self.state:
# -menu
# -running
# -maps
class Menu:
    def __init__(self):
        self.state = 'menu'
        self.play_button = Button(BUTTONPOSITION[0][0], BUTTONPOSITION[0][1], BUTTONWIDTH, BUTTONHEIGHT, BUTTONCOLOR)
        self.restart_button = Button(BUTTONPOSITION[1][0], BUTTONPOSITION[1][1], BUTTONWIDTH, BUTTONHEIGHT, BUTTONCOLOR)
        self.change_map_button = Button(BUTTONPOSITION[2][0], BUTTONPOSITION[2][1], BUTTONWIDTH, BUTTONHEIGHT, BUTTONCOLOR)
        self.exit_button = Button(BUTTONPOSITION[3][0], BUTTONPOSITION[3][1], BUTTONWIDTH, BUTTONHEIGHT, BUTTONCOLOR)
        self.return_button = Button(BUTTONPOSITION[4][0], BUTTONPOSITION[4][1], BUTTONWIDTH, BUTTONHEIGHT, BUTTONCOLOR)
        self.map_button = []
        for i in range(3):
            self.map_button.append(
                Button(BUTTONPOSITION[i + 5][0], BUTTONPOSITION[i + 5][1], BUTTONWIDTH, BUTTONHEIGHT, BUTTONCOLOR))

    def switch(self):
        if self.state == 'running':
            self.state = 'menu'
        else:
            self.state = 'running'

    def get_active_buttons(self):
        if self.state == 'menu':
            return [self.play_button, self.restart_button, self.change_map_button, self.exit_button]
        elif self.state == 'maps':
            return [self.return_button, self.map_button[0], self.map_button[1], self.map_button[2]]

    def press_button(self, index):
        if self.state == 'menu':
            if index == 0:
                self.state = 'running'
            elif index == 1:
                return 'restart'
            elif index == 2:
                self.state = 'maps'
            elif index == 3:
                return 'exit'
        elif self.state == 'maps':
            if index == 0:
                self.state = 'menu'
            else:
                return index