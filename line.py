# %%

from PIL import Image
import numpy as np

from models import Color, Point2D

image = Image.new(mode="RGB", size=(400, 400), color="black")
image
# %%
image
# %%
# image.getpixel((200, 200))
image.putpixel((200, 200), tuple(np.array([255, 255, 255], dtype=int)))
white_color = Color(255, 255, 255)
red_color = Color(255, 0, 0)
# %%

def draw_line(image: Image.Image, point_1: Point2D, point_2: Point2D, line_color: Color):
    for i in np.linspace(0, 1, num=2000):
        x = point_1.x * (1 - i) + point_2.x * i
        y = point_1.y * (i - i) + point_2.y * i
        image.putpixel((int(x), int(y)), value=line_color)
# %%
def draw_line_2(image: Image.Image, point_1: Point2D, point_2: Point2D, line_color: Color):
    if point_1.x > point_2.x:
        point_1, point_2 = point_2, point_1
    gradient = (point_2.y - point_1.y) / (point_2.x - point_1.x)
    intercept = point_1.y - gradient * point_1.x
    for i in range(point_1.x, point_2.x + 1):
        y = intercept + gradient * i
        image.putpixel((i, int(y)), value=line_color)
# %%
def draw_line_3(image: Image.Image, point_1: Point2D, point_2: Point2D, line_color: Color):
    if point_1.x > point_2.x:
        point_1, point_2 = point_2, point_1
    gradient = (point_2.y - point_1.y) / (point_2.x - point_1.x)
    intercept = point_1.y - gradient * point_1.x
    x = np.arange(point_1.x, point_2.x + 1)
    y = intercept + gradient * x
    for i in range(len(x)):
        image.putpixel((x[i], int(y[i])), value=line_color)
# %%
%%timeit

draw_line_2(image, Point2D(1, 1), Point2D(200, 200), line_color=white_color)
# %%
%%timeit

draw_line_3(image, Point2D(399, 20), Point2D(100, 150), line_color=white_color)
image
# %%

draw_line(image, Point2D(1, 1), Point2D(200, 200), line_color=white_color)
# %%
list(range(2, 0))
# %%
image
# %%

np.linspace()

