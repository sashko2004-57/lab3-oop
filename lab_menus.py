from tkinter import Menu

COMMON_TYPE = "common"
CHECK_TYPE = "check"
RADIO_TYPE = "radio"

VAR_KEY = "var"
CB_KEY = "callback"
VAL_KEY = "value"

class MenuInBar():
    def __init__(self, menubar):
        self.menu = Menu(menubar)
        self.menubar = menubar

    def add_item(self, label, type_, **kw):
        callback = kw.get(CB_KEY)
        if type_ == COMMON_TYPE:
            self.menu.add_command(label = label, command = callback)
        elif type_ == CHECK_TYPE:
            var = kw.get(VAR_KEY)
            self.menu.add_checkbutton(label = label, command = callback, variable = var)
        elif type_ == RADIO_TYPE:
            var, val = kw.get(VAR_KEY), kw.get(VAL_KEY)
            self.menu.add_radiobutton(label = label, command = callback, variable = var, value = val)

    def show(self, menu_label):
        self.menubar.add_cascade(label = menu_label, menu = self.menu)
