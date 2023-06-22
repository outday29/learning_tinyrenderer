# %%

import numpy as np
from PIL import Image

from models import Color, LineParametric, Point, Triangle, Line
from utils import to_image

image_array = np.zeros(shape=(400, 400, 3), dtype=np.uint8)
image = to_image(image_array=image_array)
# %%
image.mode
# %%
triangle: Triangle = (Point(80, 100), Point(100, 300), Point(300, 100))
# %%
line_1 = Line.from_points(point_1=triangle[0], point_2=triangle[1])
# %%
def draw_triangle(image_array: np.ndarray, triangle: Triangle, color: Color):
    sorted_vertex = sorted(triangle, key=lambda i: i.y)
    boundary_y = sorted_vertex[1].y
    _fill_half(lower_y=sorted_vertex[0].y, upper_y=boundary_y)
    _fill_half(lower_y=boundary_y, upper_y=sorted_vertex[1].y)
    
def _fill_half(image: Image, upper_y: int, lower_y: int, line_1: Line, line_2: Line):
    if upper_y and lower_y:
        raise ValueError("Can only specify upper_y or lower_y")

    if upper_y:
        line_1, line_2 = sorted([line_1, line_2], key= lambda)
    
    if lower_y:
        pass