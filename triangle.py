# %%

import numpy as np
from PIL import Image
from logger import logger
from models import Color, Point2D, Point3D, Triangle, Line
import numpy.typing as npt
from utils import to_image
# %%
def draw_triangle(image_array: np.ndarray, triangle: Triangle, color: Color):
    sorted_vertex = sorted(triangle, key=lambda i: i.y)
    boundary_y = sorted_vertex[1].y
    line_2_to_3 = Line.from_points(point_1=sorted_vertex[1], point_2=sorted_vertex[2])
    line_3_to_1 = Line.from_points(point_1=sorted_vertex[2], point_2=sorted_vertex[0])
    line_1_to_2 = Line.from_points(point_1=sorted_vertex[0], point_2=sorted_vertex[1])
    _fill_half(
        image_array=image_array,
        lower_y=boundary_y,
        line_1=line_2_to_3,
        line_2=line_3_to_1,
        color=color,
    )
    _fill_half(
        image_array=image_array,
        upper_y=boundary_y,
        line_1=line_1_to_2,
        line_2=line_3_to_1,
        color=color,
    )
    return image_array


def visualize_point(image_array: npt.NDArray, triangle: Triangle, color: Color):
    for i in triangle:
        image_array[i.y][i.x] = np.array(color)
    image = to_image(image_array=image_array)
    image.show("Visualizing triangle points")


def _fill_half(
    image_array: npt.NDArray,
    line_1: Line,
    line_2: Line,
    color: Color,
    upper_y: int = None,
    lower_y: int = None,
):
    if upper_y and lower_y:
        raise ValueError("Can only specify upper_y or lower_y")

    if not upper_y and not lower_y:
        raise ValueError("Must specify either upper_y or lower_y")

    line_1, line_2 = sorted(
        [line_1, line_2], key=lambda x: x.get_x_value(upper_y or lower_y)
    )

    if upper_y:
        logger.debug(f"Doing upper_y")
        # shade from upper_y to above (In PIL, that is negative y direction)
        for i in range(upper_y, -1, -1):
            logger.debug(f"{i=}")
            lower_bound_x = int(line_1.get_x_value(y=i))
            logger.debug(f"{lower_bound_x=}")
            upper_bound_x = int(line_2.get_x_value(y=i))
            logger.debug(f"{upper_bound_x=}")
            for j in range(lower_bound_x, upper_bound_x + 1):
                image_array[i][j] = np.array(color)

    if lower_y:
        logger.debug(f"Doing lower_y")
        for i in range(lower_y, image_array.shape[0]):
            logger.debug(f"{i=}")
            lower_bound_x = int(line_1.get_x_value(y=i))
            logger.debug(f"{lower_bound_x=}")
            upper_bound_x = int(line_2.get_x_value(y=i))
            logger.debug(f"{upper_bound_x=}")
            for j in range(lower_bound_x, upper_bound_x + 1):
                image_array[i][j] = np.array(color)


def get_barycentric_scalar(triangle: Triangle, point: Point2D) -> tuple[float, float]:
    v1, v2, v3 = map(lambda x: x.as_ndarray(), triangle)
    base_1 = v2 - v1
    base_2 = v3 - v1
    origin_change = v1 - point.as_ndarray()
    temp_1 = [
        base_1[0],
        base_2[0],
        origin_change[0]
    ]
    temp_2 = [
        base_1[1],
        base_2[1],
        origin_change[1]
    ]
    p = np.cross(temp_1, temp_2)
    p = p / p[2]
    return (p[0], p[1])

def _find_bounding_box(triangle: Triangle) -> tuple[Point2D, Point2D]:
    all_x = list(map(lambda p: p.x, triangle))
    all_y = list(map(lambda p: p.y, triangle))
    logger.debug(f"{all_x=}")
    logger.debug(f"{all_y=}")
    upper_left = Point2D(min(all_x), min(all_y))
    lower_right = Point2D(max(all_x), max(all_y))
    return (upper_left, lower_right)
    

def draw_triangle_barycentric(image_array: npt.NDArray, triangle: Triangle, color: Color) -> None:
    upper_left, lower_right = _find_bounding_box(triangle)
    for x in range(upper_left.x, lower_right.x + 1):
        for y in range(upper_left.y, lower_right.y + 1):
            coefficient = get_barycentric_scalar(triangle=triangle, point=Point2D(x, y))
            if coefficient[0] < 0 or coefficient[1] < 0:
                continue
            
            if 0 <= sum(coefficient) <= 1:
                image_array[y][x] = np.array(color)
                

# %%
image_array = np.zeros(shape=(400, 400, 3), dtype=np.uint8)
triangle: Triangle = (Point2D(80, 100), Point2D(100, 250), Point2D(300, 150))
color: Color = Color(255, 0, 0)
visualize_point(image_array, triangle=triangle, color=color)
# %%
draw_triangle_barycentric(image_array=image_array, color=color, triangle=triangle)
# %%
get_barycentric_scalar(triangle=triangle, point=Point2D(100, 120))
# %%
image_array = np.zeros(shape=(400, 400, 3), dtype=np.uint8)
triangle: Triangle = (Point2D(150, 100), Point2D(180, 350), Point2D(80, 300))
color: Color = Color(255, 255, 255)
visualize_point(image_array, triangle=triangle, color=color)
# %%
image_array = draw_triangle(image_array=image_array, triangle=triangle, color=color)
# %%
to_image(image_array)
