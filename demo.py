import os
import sys

import cv2
import numpy as np

import equirec2perspec


if __name__ == '__main__':
    import time

    frame = cv2.imread('src/image.jpg')
    out = np.zeros((720, 1080, 3), dtype='uint8')

    x_axis = np.array([1.0, 0.0, 0.0], np.float32)
    y_axis = np.array([0.0, 1.0, 0.0], np.float32)
    R1, _ = cv2.Rodrigues(y_axis * np.radians(-90))
    R2, _ = cv2.Rodrigues(np.dot(R1, x_axis) * np.radians(30))
    R = R2 @ R1

    n = 100
    t = time.time()
    for _ in range(100):
        equirec2perspec.get_perspective(frame, out, R, 60)
    print(n / (time.time() - t))

    cv2.imshow('a', out)
    cv2.waitKey()
