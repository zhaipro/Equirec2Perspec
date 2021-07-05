import os
import sys

import cv2
import numpy as np
from scipy.spatial.transform import Rotation as R

import equirec2perspec


if __name__ == '__main__':
    import time

    frame = cv2.imread('src/image.jpg')
    out = np.zeros((720, 1080, 3), dtype='uint8')
    mat = R.from_euler('xyz', [30, -90, 0], degrees=True).as_matrix()

    n = 1
    t = time.time()
    for _ in range(n):
        equirec2perspec.get_perspective(frame, out, mat, 60)
    print(n / (time.time() - t))

    cv2.imshow('a', out)
    cv2.waitKey()
