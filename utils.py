import numpy as np
from PIL import Image


def to_image(image_array: np.ndarray):
    img = Image.fromarray(image_array, mode="RGB")
    return img
