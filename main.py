# See the context for this code at https://steampunc.github.io//post/2018/01/07/chladni.html
# Generates approximations of Chladni patterns using some fun math
import glob
import math
import os
import shutil
import statistics as stat

import imageio
import numpy as np
import cv2
from PIL import Image


OUT_DIR_PATH = r'C:\Users\Jamie Davies\Documents\git\chladni\out'
OUT_GIF_NAME = 'sand_shapes.gif'


x_screen_size = 16 #100
y_screen_size = 16 #100
emitter_matrix_size = 7 # can't modify this value yet
velocity = 300
#frequency = 15

def GetDistance(x, y, emitter_x, emitter_y):
    x_length = (3 - emitter_x) * x_screen_size - ((x_screen_size / 2.0) - x)
    y_length = (3 - emitter_y) * y_screen_size - ((y_screen_size / 2.0) - y)

    crosses = abs(3 - emitter_x) + abs(3 - emitter_y)

    return math.sqrt(x_length * x_length + y_length * y_length), crosses


# if os.path.isdir(OUT_DIR_PATH):
#     shutil.rmtree(OUT_DIR_PATH)
#     print('removed:', OUT_DIR_PATH)
# os.makedirs(OUT_DIR_PATH)
# if os.path.isfile(OUT_GIF_NAME):
#     os.remove(OUT_GIF_NAME)
#     print('removed:', OUT_GIF_NAME)
#
#
# i = 0
# frequency = 10.0
# counter = 0
# while frequency <= 20:
#     counter += 1
#     wavelength = (velocity / frequency)
#     main_image = np.zeros((y_screen_size, x_screen_size, 3), np.uint8)
    for x in range(x_screen_size):
        for y in range(y_screen_size):
            distances = []
            for emitter_x in range(emitter_matrix_size):
                for emitter_y in range(emitter_matrix_size):
                    point_distance = GetDistance(x, y, emitter_x, emitter_y)
                    effective_distance = math.fmod(point_distance[0], wavelength)
                    if point_distance[1] % 2 == 1:
                        effective_distance = wavelength - effective_distance
                    distances.append(effective_distance)
#
#             brightness = 255 - stat.stdev(distances) * 100
#             main_image[y, x] = (brightness, brightness, brightness)
#
#     main_image = cv2.resize(main_image, (0, 0), fx = 4, fy = 4)
#     cv2.imwrite(os.path.join(OUT_DIR_PATH, f'chladni-imageschladni_c{i:03}.png'), main_image)
#     frequency += 0.025
#     i += 1
#
#     if i > 200:
#         break


def make_gif(frame_folder):
    frames = [Image.open(image) for image in sorted(glob.glob(f"{frame_folder}/*.png"))]
    frame_one = frames[0]
    frame_one.save(
        "sand_shapes.gif",
        format="GIF",
        append_images=frames,
        save_all=True,
        duration=40,
        loop=0
    )


def make_gif2(dir_path):
    frames = []
    for file_name in os.listdir(dir_path):
        image = imageio.v2.imread(os.path.join(dir_path, file_name))
        frames.append(image)
    imageio.mimsave(OUT_GIF_NAME,  # output gif
                    frames,  # array of input frames
                    duration=100)  # optional: frames per second


print('DONE!')
make_gif(OUT_DIR_PATH)