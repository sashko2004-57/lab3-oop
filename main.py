from tkinter import Tk, Menu, Variable, Canvas, PhotoImage, Frame, Button, TOP, LEFT, BOTTOM, SUNKEN, RAISED
from lab_menus import MenuInBar, COMMON_TYPE, RADIO_TYPE, VAR_KEY, CB_KEY, VAL_KEY
from lab_shapes import Point, Line, Rectangle, Ellipse, TRAIL_KEY, COO_ALGO_KEY, FILL_KEY, RECT_KEY, ELL_KEY
from lab_config import DialogConfig

MY_NUMBER = 6
IS_DYNAMIC = True

ARRAY_LEN = MY_NUMBER + 100

BUTTON_SIZE = 20

WIN_TITLE = "Головне вікно"

LABEL_KEY = "label"
ICON_KEY = "icon"
FILE_MENU_LABEL = "Файл"
SHAPES_MENU_LABEL = "Фігури"
EXIT_LABEL = "Вихід"
POINT_LABEL = "Точка"
LINE_LABEL = "Лінія"
RECTANGLE_LABEL = "Прямокутник"
ELLIPSE_LABEL = "Еліпс"

SHOW_SHAPE_KEY = "show_shape"

FILE_MENU = lambda obj : (
    {
        LABEL_KEY : "Налаштування",
        CB_KEY : obj.open_config
    },
    {
        LABEL_KEY : EXIT_LABEL,
        CB_KEY : obj.win.destroy,
    },
)
SHAPES_LIST = (Point, Line, Rectangle, Ellipse)
SHAPES_MENU = (
    {
        LABEL_KEY : POINT_LABEL,
        VAL_KEY : 0
    },
    {
        LABEL_KEY : LINE_LABEL,
        VAL_KEY : 1
    },
    {
        LABEL_KEY : RECTANGLE_LABEL,
        VAL_KEY : 2
    },
    {
        LABEL_KEY : ELLIPSE_LABEL,
        VAL_KEY : 3
    }
)
BUTTONS = (
    {
        ICON_KEY : "point.png",
        LABEL_KEY : POINT_LABEL,
        VAL_KEY : 0
    },
    {
        ICON_KEY : "line.png",
        LABEL_KEY : LINE_LABEL,
        VAL_KEY : 1
    },
    {
        ICON_KEY : "rectangle.png",
        LABEL_KEY : RECTANGLE_LABEL,
        VAL_KEY : 2
    },
    {
        ICON_KEY : "ellipse.png",
        LABEL_KEY : ELLIPSE_LABEL,
        VAL_KEY : 3
    }
)

INIT_CONFIG = lambda win : {
    TRAIL_KEY : Variable(win, value = 2),
    RECT_KEY : {
        COO_ALGO_KEY : Variable(win, value = 1),
        FILL_KEY : Variable(win, value = 1)
    },
    ELL_KEY : {
        COO_ALGO_KEY : Variable(win, value = 0),
        FILL_KEY : Variable(win, value = 0)
    },
    SHOW_SHAPE_KEY : Variable(win, value = 1)
}


INIT_SHAPE = SHAPES_MENU[0]

class Win:
    def __init__(self):
        self.win = Tk()
        self.menubar = Menu(self.win)
        self.win.config(menu = self.menubar)
        self.create_vars()
        self.shape_name = INIT_SHAPE[LABEL_KEY]
        self.change_title()
        self.create_menus()
        self.create_button_panel()
        self.create_canvas()
        self.shapes = [] if IS_DYNAMIC else [None for num in range(ARRAY_LEN)]

    def change_show_shape(self, *args):
        self.menubar.delete(SHAPES_MENU_LABEL)
        self.create_shapes_menu()
        self.change_title()

    def open_config(self):
        trail_type = self.config[TRAIL_KEY]
        rect_coo_algo = self.config[RECT_KEY][COO_ALGO_KEY]
        rect_fill = self.config[RECT_KEY][FILL_KEY]
        ell_coo_algo = self.config[ELL_KEY][COO_ALGO_KEY]
        ell_fill = self.config[ELL_KEY][FILL_KEY]
        show_shape = self.config[SHOW_SHAPE_KEY]
        dialog = DialogConfig(self.win, trail_type, rect_coo_algo,
                              rect_fill, ell_coo_algo, ell_fill, show_shape)

    def change_title(self):
        suffix = (" - " + self.shape_name) if self.config[SHOW_SHAPE_KEY].get() else ""
        self.win.title(WIN_TITLE + suffix)

    def create_vars(self):
        self.shape_var = Variable(self.win, value = INIT_SHAPE[VAL_KEY])
        self.config = INIT_CONFIG(self.win)
        self.config[SHOW_SHAPE_KEY].trace_add("write", self.change_show_shape)

    def create_shape_buttons(self):
        self.buttons = []
        for item in BUTTONS:
            icon_name = item.get(ICON_KEY)
            icon = PhotoImage(file = icon_name, width = BUTTON_SIZE, height = BUTTON_SIZE)
            val = item.get(VAL_KEY)
            label = item.get(LABEL_KEY)
            cb = self.create_callback(self.shape_var, val, label)
            button = Button(self.button_panel, image = icon, command = cb, width = BUTTON_SIZE, height = BUTTON_SIZE)
            self.buttons.append(button)
            if val == self.shape_var.get():
                button.config(relief = SUNKEN)
                self.sunken = button
            button.image = icon
            button.pack(side = LEFT)

    def create_button_panel(self):
        self.button_panel = Frame(self.win)
        self.create_shape_buttons()
        self.button_panel.pack(side = TOP)

    def delete_shape(self, shape):
        if not shape == None:
            shape.delete()

    def create_shape(self, event):
        shape_class = SHAPES_LIST[self.shape_var.get()]
        self.shape = shape_class(self.config)
        if len(self.shapes) >= ARRAY_LEN:
            self.delete_shape(self.shapes.pop(0))
        self.shapes.append(self.shape)
        self.shape.create_shape(self.canvas, event.x, event.y)

    def create_canvas(self):
        self.canvas = Canvas(self.win)
        self.canvas.pack()
        self.canvas.bind("<1>", self.create_shape)
        self.canvas.bind("<B1-Motion>", lambda event : self.shape.resize_shape(event))
        self.canvas.bind("<ButtonRelease-1>", lambda event : self.shape.stop_draw(event))

    def create_menus(self):
        self.create_file_menu()
        self.create_shapes_menu()
        
    def create_menu(self):
        return MenuInBar(self.menubar)
    
    def create_file_menu(self):
        menu = self.create_menu()
        win = self.win
        items = FILE_MENU(self)
        for item in items:
            label = item.get(LABEL_KEY)
            callback = item.get(CB_KEY)
            menu.add_item(label, COMMON_TYPE, callback = callback)
        menu.show(FILE_MENU_LABEL)

    def switch_buttons(self, shape_id):
        self.sunken.config(relief = RAISED)
        self.sunken = self.buttons[shape_id]
        self.sunken.config(relief = SUNKEN)

    def change_shape(self, var, shape_id, shape_name):
        var.set(shape_id)
        self.shape_name = shape_name
        self.switch_buttons(shape_id)
        self.change_title()

    def create_callback(self, var, shape_id, shape_name):
        return lambda : self.change_shape(var, shape_id, shape_name)

    def fill_shapes_menu(self, menu, items, var):
        for item in items:
            label = item.get(LABEL_KEY)
            val = item.get(VAL_KEY)
            if not self.config[SHOW_SHAPE_KEY].get():
                cb = lambda : self.switch_buttons(var.get())
                menu.add_item(label, RADIO_TYPE, var = var, value = val, callback = cb)
            else:
                cb = self.create_callback(var, val, label)
                menu.add_item(label, COMMON_TYPE, callback = cb)

    def create_shapes_menu(self):
        items = SHAPES_MENU
        menu = self.create_menu()
        var = self.shape_var
        self.fill_shapes_menu(menu, items, var)
        menu.show(SHAPES_MENU_LABEL)

def main():
    win = Win()

main()
