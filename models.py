# %%
from __future__ import annotations
from typing import Any, NamedTuple, TypeAlias
from pydantic import BaseModel
from logger import logger
import numpy as np
import numpy.typing as npt


class Color(NamedTuple):
    r: int
    g: int
    b: int


class Point(NamedTuple):
    x: int
    y: int
    
    def as_ndarray(self) -> npt.NDArray:
        return np.array([self.x, self.y])

class LineParametric(BaseModel):
    # Parametric representation of a 2D line
    start_point: Any # Pydantic does not support npt.NDArray
    direction_vector: Any
    
    class Config:
        arbitrary_types_allowed: True
    
    @classmethod
    def from_points(cls, point_1: Point, point_2: Point):
        point_1 = point_1.as_ndarray()
        point_2 = point_2.as_ndarray()
        logger.info(f"{point_1=}")
        direction_vector = (point_2 - point_1).reshape(1, -1)
        start_point = point_1.reshape(1, -1)
        logger.info(f"{start_point=}")
        return cls(start_point=start_point, direction_vector=direction_vector)

class Line(BaseModel):
    slope: float
    y_intercept: float
    
    @classmethod
    def from_points(cls, point_1: Point, point_2: Point) -> Line:
        if point_1.x == point_2.x:
            raise ValueError(f"Vertical line not supported")
        
        slope = (point_2.y - point_1.y) / (point_2.x - point_1.x)
        y_intercept = point_1.y - slope * point_1.x

        return cls(slope=slope, y_intercept=y_intercept)
    
    def get_y_value(self, x = float) -> float:
        return self.y_intercept + (x * self.slope)
    
    def get_x_value(self, y = float) -> float:
        return (y - self.y_intercept) / self.slope
    
Triangle: TypeAlias = tuple[Point, Point, Point]