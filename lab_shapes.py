POINT_RADIUS = 1

BLACK_TRAIL_TYPE = 0
RED_TRAIL_TYPE = 1
BLUE_TRAIL_TYPE = 2
BLACK_DASHED_TRAIL_TYPE = 3

ANGLE_TO_ANGLE = 0
CENTER_TO_ANGLE = 1

TRAIL_KEY = "trail"
COO_ALGO_KEY = "coo_algo"
FILL_KEY = "fill"
RECT_KEY = "rect"
ELL_KEY = "ell"

TRAIL_MAX = BLACK_DASHED_TRAIL_TYPE
TRAIL_COLORS = 3
BLACK = "black"
RED = "red"
BLUE = "blue"
LINE_COLOR_DEFAULT = BLACK
LINE_COLORS = (BLACK, RED, BLUE)
SOLID = ()
DASHED = (1, 1)
DASH_PATTERN_DEFAULT = SOLID
DASH_PATTERNS = (SOLID, DASHED)
WHITE = "#fff"
YELLOW = "#ff0"
GREEN = "#0f0"
CYAN = "#0ff"
MAGENTA = "#f0f"
ORANGE = "#ff8000"
GREY = "#c0c0c0"
EMPTY_FILL_ID = 7
FILL_COLORS = (WHITE, YELLOW, GREEN, CYAN, MAGENTA, ORANGE, GREY, "")

ANOTHER_ANGLE_COORD = lambda coord_center, coord_angle1 : 2 * coord_center - coord_angle1

class Shape():
    def __init__(self, config):
        trail_type = config[TRAIL_KEY].get()
        self.set_trail(trail_type)
        self.coords_algo = 0
        self.is_point = False
        self.shape_id = None

    def set_trail(self, trail_type):
        line_color_id, dash_pattern_id = self.trail_type_to_params(trail_type)
        self.trail_color = self.line_color_by_id(line_color_id)
        self.trail_dash = self.dash_pattern_by_id(dash_pattern_id)

    def calc_coords(self, x0, y0, x1, y1):
        if self.coords_algo == CENTER_TO_ANGLE:
            x2 = ANOTHER_ANGLE_COORD(x0, x1)
            y2 = ANOTHER_ANGLE_COORD(y0, y1)
            return x2, y2
        return x0, y0

    def resize_shape(self, event):
        x0, y0 = self.calc_coords(self.x_start, self.y_start, event.x, event.y)
        self.canvas.coords(self.shape_id, x0, y0, event.x, event.y)
        self.canvas.update()

    def trail_type_to_params(self, trail_type):
        if not (0 <= trail_type <= TRAIL_MAX):
            trail_type = 0
        return trail_type % TRAIL_COLORS, trail_type // TRAIL_COLORS

    def line_color_by_id(self, color_id):
        return LINE_COLORS[color_id]

    def dash_pattern_by_id(self, dash_patt_id):
        return DASH_PATTERNS[dash_patt_id]

    def stop_draw(self, event):
        self.resize_shape(event)
        self.trail_to_shape()
        self.canvas.update()

    def trail_to_shape(self):
        pass

    def create_trail(self, x_start, y_start):
        pass
    
    def create_shape(self, canvas, x_start, y_start):
        self.canvas = canvas
        self.x_start, self.y_start = x_start, y_start
        self.shape_id = self.create_trail(x_start, y_start)
        self.canvas.update()

    def delete(self):
        self.canvas.delete(self.shape_id)
        

class Point(Shape):
    def create_trail(self, x_start, y_start):
        return self.canvas.create_oval(x_start - POINT_RADIUS, y_start - POINT_RADIUS,
                                  x_start + POINT_RADIUS, y_start + POINT_RADIUS,
                                  outline = self.trail_color, fill = self.trail_color)

    def resize_shape(self, event):
        return

    def trail_to_shape(self):
        self.canvas.itemconfig(self.shape_id, outline = LINE_COLOR_DEFAULT,
                          fill = LINE_COLOR_DEFAULT)

class Line(Shape):
    def create_trail(self, x_start, y_start):
        return self.canvas.create_line(x_start, y_start, x_start + 1, y_start + 1,
                                  fill = self.trail_color, dash = self.trail_dash)
    
    def trail_to_shape(self):
        self.canvas.itemconfig(self.shape_id, fill = LINE_COLOR_DEFAULT, dash = DASH_PATTERN_DEFAULT)

class Rectangle(Shape):
    def __init__(self, config):
        Shape.__init__(self, config)
        rect_conf = config[RECT_KEY]
        self.coords_algo = rect_conf[COO_ALGO_KEY].get()
        self.fill = rect_conf[FILL_KEY].get()

    def create_trail(self, x_start, y_start):
        return self.canvas.create_rectangle(x_start, y_start, x_start + 1, y_start + 1,
                                       outline = self.trail_color, dash = self.trail_dash)

    def trail_to_shape(self):
        self.canvas.itemconfig(self.shape_id, outline = LINE_COLOR_DEFAULT, dash = DASH_PATTERN_DEFAULT,
                          fill = FILL_COLORS[self.fill])

class Ellipse(Shape):
    def __init__(self, config):
        Shape.__init__(self, config)
        ell_conf = config[ELL_KEY]
        self.coords_algo = ell_conf[COO_ALGO_KEY].get()
        self.fill = ell_conf[FILL_KEY].get()

    def create_trail(self, x_start, y_start):
        return self.canvas.create_oval(x_start, y_start, x_start + 1, y_start + 1,
                                  outline = self.trail_color, dash = self.trail_dash)

    def trail_to_shape(self):
        self.canvas.itemconfig(self.shape_id, outline = LINE_COLOR_DEFAULT, dash = DASH_PATTERN_DEFAULT,
                          fill = FILL_COLORS[self.fill])


