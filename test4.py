import glob
import math
import os
import random
import shutil
from dataclasses import dataclass

from PIL import Image
import numpy as np


OUT_DIR_PATH = r'C:\Users\Jamie Davies\Documents\git\chladni\out'
OUT_GIF_NAME = 'sand_shapes.gif'
IMAGE_SIZE = 256

L1 = 0.04 #* 10.0
L2 = 0.02 #* 10.0
L3 = 0.018 #* 10.0


if os.path.isdir(OUT_DIR_PATH):
    shutil.rmtree(OUT_DIR_PATH)
    print('removed:', OUT_DIR_PATH)
os.makedirs(OUT_DIR_PATH)
if os.path.isfile(OUT_GIF_NAME):
    os.remove(OUT_GIF_NAME)
    print('removed:', OUT_GIF_NAME)


@dataclass
class ChladniParams:
    m: int
    n: int
    l: float


#CHLADNI_PARAMS = [
    # ChladniParams(1, 2, L2),
    # ChladniParams(1, 3, L2),

    # ChladniParams(0, 4, L2),
    # ChladniParams(1, 4, L2),
    # ChladniParams(2, 4, L2),
    # ChladniParams(3, 4, L2),


    # ChladniParams(0, 6, L2),
    # ChladniParams(1, 6, L2),
    # ChladniParams(2, 6, L2),
    # ChladniParams(3, 6, L2),
    # ChladniParams(3, 7, L2),
    # ChladniParams(2, 7, L2),
    # ChladniParams(2, 7, L2),
    # ChladniParams(1, 7, L2),

    #ChladniParams(1, 10, 0.0075),
    #ChladniParams(1, 5, 0.0150),


    # ChladniParams(1, 10, 0.0075),
    # ChladniParams(8, 10, 0.0075),
    # ChladniParams(3, 5, 0.0175),

    # ChladniParams(8, 1, 0.0075),


    # ChladniParams(2, 3, L2),
    # ChladniParams(2, 2, L2),
    # ChladniParams(3, 2, L2),
    # ChladniParams(3, 3, L2),
    # ChladniParams(3, 2, L2),
    # ChladniParams(1, 5, L2),
    # ChladniParams(2, 3, L2),
    # ChladniParams(2, 5, L2),
    # ChladniParams(3, 4, L2),
    # ChladniParams(3, 5, L2),
    # ChladniParams(3, 7, L2),
    # ChladniParams(2, 7, L1),
    # ChladniParams(2, 6, L2),
    # ChladniParams(2, 5, L3),
    # ChladniParams(4, 4, L2),
    # ChladniParams(4, 5, L2),
    # ChladniParams(4, 7, L2),
    # ChladniParams(5, 4, L2),
    # ChladniParams(5, 5, L3),
    # ChladniParams(5, 7, L2),
#]
CHLADNI_PARAMS = [
    ChladniParams(1, 2, L1),
    ChladniParams(1, 3, L3),
    ChladniParams(1, 4, L2),
    ChladniParams(1, 5, L2),
    ChladniParams(2, 3, L2),
    ChladniParams(2, 5, L2),
    ChladniParams(3, 4, L2),
    ChladniParams(3, 5, L2),
    ChladniParams(3, 7, L2),
]


def lerp(a, b, t):
    return a * (1.0 - t) + (b * t)


def chladni_eqn_square2(x, y, m, n, l, width=1):
    r = 0
    tx = random.random() * width
    ty = random.random() * width
    scaled_x = x * l + tx
    scaled_y = y * l + ty
    mx = m * scaled_x + r
    my = m * scaled_y + r
    nx = n * scaled_x + r
    ny = n * scaled_y + r
    return np.cos(nx) * np.cos(my) - np.cos(mx) * np.cos(ny)


def make_gif(frame_folder, duration=10):
    frames = [Image.open(image) for image in sorted(glob.glob(f"{frame_folder}/*.png"))]
    frame_one = frames[0]
    frame_one.save(
        "sand_shapes.gif",
        format="GIF",
        append_images=frames,
        save_all=True,
        duration=duration,
        loop=0
    )


last_param = None
i = 0
for param in CHLADNI_PARAMS:

    if last_param is not None:
        subparams = [
            ChladniParams(
                lerp(last_param.m, param.m, t / 40.0),
                lerp(last_param.n, param.n, t / 40.0),
                lerp(last_param.l, param.l, t / 40.0),
            )
            for t in range(40)
        ]
    else:
        subparams = [param]

    #print(len(subparams), subparams)

    for subparam in subparams:

        # First part of vectorisation. Construct a grid which contains x and y values.
        grid = np.mgrid[0:IMAGE_SIZE, 0:IMAGE_SIZE]
        y = grid[0, :, :]
        x = grid[1, :, :]

        # Now pass them into the chladni equation as normal.
        m = subparam.m
        n = subparam.n
        l = subparam.l
        array = chladni_eqn_square2(x, y, m, n, l, 0)

        # Some fixups to remove banding and make a more pleasant image.
        array /= 2
        array = np.abs(array)

        # Invert.
        array = 1 - array

        # IMAGERIZE.
        img = Image.fromarray(np.uint8(array * 255))
        file_path = os.path.join(OUT_DIR_PATH, f'chladni-imageschladni_c{i:03}.png')
        with open(file_path, 'wb') as f:
            img.save(f)

        #print(file_path, '->', subparam)

        i += 1

    last_param = param


make_gif(OUT_DIR_PATH, duration=40)
print('DONE!')