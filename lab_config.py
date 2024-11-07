from tkinter.simpledialog import Dialog
from tkinter import Label, OptionMenu, Frame, Button, Variable, LEFT

WIN_TITLE = "Налаштування"
BACK_TEXT = "Назад"

TRAIL_LABEL = "Тип гумового сліду:"
RECT_COO_LABEL = "Увід прямокутника:"
RECT_FILL_LABEL = "Заповнення прямокутника:"
ELL_COO_LABEL = "Увід еліпса:"
ELL_FILL_LABEL = "Заповнення еліпса:"
SHOW_SHAPE_LABEL = "Показати обраний тип фігури в:"
TRAIL_TUPLE = (
    "чорна суцільна лінія",
    "червона суцільна лінія",
    "синя суцільна лінія",
    "чорна пунктирна лінія"
)
COO_ALGO_TUPLE = (
    "по двох протилежних кутах",
    "від центру до одного з кутів"
)
SHAPE_FILL_TUPLE = (
    "біле",
    "жовте",
    "світло-зелене",
    "блакитне",
    "рожеве",
    "помаранчеве",
    "сіре",
    "відсутнє"
)
SHOW_SHAPE_TUPLE = (
    "меню \"Фігури\"",
    "заголовку вікна"
)

class DialogConfig(Dialog):
    def __init__(self, window, trail_type, rect_coo, rect_fill, ell_coo, ell_fill, show_choose):
        title = WIN_TITLE
        convert = self.convert_index_option
        self.trail_type = convert(window, trail_type, TRAIL_TUPLE)
        self.rect_coo = convert(window, rect_coo, COO_ALGO_TUPLE)
        self.rect_fill = convert(window, rect_fill, SHAPE_FILL_TUPLE)
        self.ell_coo = convert(window, ell_coo, COO_ALGO_TUPLE)
        self.ell_fill = convert(window, ell_fill, SHAPE_FILL_TUPLE)
        self.show_choose = convert(window, show_choose, SHOW_SHAPE_TUPLE)
        Dialog.__init__(self, window, title)

    def change_index(self, index_var, opt_var, opt_list):
        opt_value = opt_var.get()
        index_var.set(opt_list.index(opt_value))

    def convert_index_option(self, win, index_var, opt_list):
        value = index_var.get()
        option_var = Variable(win, opt_list[value])
        option_var.trace_add("write", lambda *args : self.change_index(index_var, option_var, opt_list))
        return option_var

    def body(self, window):
        Label(window, text = TRAIL_LABEL).pack()
        OptionMenu(window, self.trail_type, *TRAIL_TUPLE).pack()
        Label(window, text = RECT_COO_LABEL).pack()
        OptionMenu(window, self.rect_coo, *COO_ALGO_TUPLE).pack()
        Label(window, text = RECT_FILL_LABEL).pack()
        OptionMenu(window, self.rect_fill, *SHAPE_FILL_TUPLE).pack()
        Label(window, text = ELL_COO_LABEL).pack()
        OptionMenu(window, self.ell_coo, *COO_ALGO_TUPLE).pack()
        Label(window, text = ELL_FILL_LABEL).pack()
        OptionMenu(window, self.ell_fill, *SHAPE_FILL_TUPLE).pack()
        Label(window, text = SHOW_SHAPE_LABEL).pack()
        OptionMenu(window, self.show_choose, *SHOW_SHAPE_TUPLE).pack()
        
      
    def buttonbox(self):
        box = Frame(self)
        Button(box, text = BACK_TEXT, command = self.ok).pack(side = LEFT)
        box.pack()
