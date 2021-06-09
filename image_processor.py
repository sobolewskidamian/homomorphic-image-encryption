import PIL
import numpy as np
from datetime import datetime
from Pyfhel import PyCtxt, PyPtxt
from typing import List
from os import mkdir, path


class ImageProcessor:
    def __init__(self, name: str) -> None:
        self.name: str = name
        image = np.array(PIL.Image.open("images/" + self.name).convert("RGB"))
        self.x_size: int = image.shape[0]
        self.y_size: int = image.shape[1]
        self.image: np.array = image

    def save_processed_image(self, result_image: List[List[List]]) -> None:
        print("Saving image...")
        result_image = np.uint8(result_image)
        result_image = PIL.Image.fromarray(result_image)
        dir_name = "processed_images"
        if not path.isdir(dir_name):
            mkdir(dir_name)
        result_image.save(
            f"{dir_name}/{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}_{self.name}"
        )


class EncryptedImageProcessor:
    def __init__(self, image: List[List[List[PyPtxt]]], x: int, y: int) -> None:
        self.image: List[List[List[PyPtxt]]] = image
        self.x: int = x
        self.y: int = y

    def make_grey_scale(self) -> List[List[List[PyPtxt]]]:
        result: List[List[np.array]] = []
        for i, x_vector in enumerate(self.image):
            processed_x_vector = []
            for pixel in x_vector:
                processed_pixel = np.empty(len(pixel), dtype=PyCtxt)
                grey_scale = pixel[0] * 0.299 + pixel[1] * 0.587 + pixel[2] * 0.114
                processed_pixel[0] = grey_scale
                processed_pixel[1] = grey_scale
                processed_pixel[2] = grey_scale
                processed_x_vector.append(processed_pixel)
            result.append(processed_x_vector)
        return result

    def make_blur(self, blur_level) -> List[List[List[PyPtxt]]]:
        result = self.image.copy()
        for y in range(self.y):
            for x in range(self.x):
                for pixel_num in range(3):
                    p_sum = None
                    amount_of_elems = 0
                    for y_num in range(y, y + blur_level):
                        for x_num in range(x, x + blur_level):
                            if y_num < 0 or y_num > self.y - 1 or x_num < 0 or x_num > self.x - 1:
                                continue
                            elem = self.image[y_num][x_num][pixel_num]
                            if p_sum is None:
                                p_sum = elem
                            else:
                                p_sum += elem
                            amount_of_elems += 1
                    result[y][x][pixel_num] = p_sum / amount_of_elems
        return result
