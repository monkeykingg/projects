import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image

def stereo_match(left_img, right_img, patch_size):

    car, top_left, bottom_right = get_car(left_img, left_car_top_left, left_car_bottom_right)

    x0 = top_left[0]
    y0 = top_left[1]
    x1 = bottom_right[0]
    y1 = bottom_right[1]

    patch_center = top_left
    scanline = y0
    right_row = right_img.shape[0]
    right_col = right_img.shape[1]

    for y in range(y0, y1):
        for x_left in range(x0, x1):

            patch_left_center = (x_left, y)

            patch_left_x0 = x_left - math.floor(patch_size / 2)
            patch_left_y0 = y - math.floor(patch_size / 2)
            patch_left_x1 = x_left + math.ceil(patch_size / 2)
            patch_left_y1 = y + math.ceil(patch_size / 2)

            patch_left = left_img[patch_left_y0:patch_left_y1, patch_left_x0:patch_left_x1]

            for x_right in range(math.floor(patch_size / 2), right_col - math.ceil(patch_size / 2)):

                patch_right_center = (x_right, y)

                patch_right_x0 = x_right - math.floor(patch_size / 2)
                patch_right_y0 = y - math.floor(patch_size / 2)
                patch_right_x1 = x_right + math.ceil(patch_size / 2)
                patch_right_y1 = y + math.ceil(patch_size / 2)

                patch_right = right_img[patch_right_y0:patch_right_y1, patch_right_x0:patch_right_x1]

def nc(patch_l, patch_r):
    product = np.dot(patch_l, patch_r)
    norm_l = np.linalg.norm(patch_l)
    norm_r = np.linalg.norm(patch_r)
    numerator = product
    denominator = norm_l * norm_r
    return numerator / denominator

def depth(f, T, xl, xr):
    Z = f * T / (xl - xr)
    return Z

def get_car(car, top_left, bottom_right):
    x0 = int(top_left[0])
    x1 = int(bottom_right[0])
    y0 = int(top_left[1])
    y1 = int(bottom_right[1])
    cropped = car[y0:y1, x0:x1]
    top_left = (x0, y0)
    bottom_right = (x1, y1)
    return cropped, top_left, bottom_right
