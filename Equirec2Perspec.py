import os
import sys

import cv2
import numpy as np


def get_perspective(im, FOV, THETA, PHI, height, width):
    #
    # THETA is left/right angle, PHI is up/down angle, both in degree
    #
    equ_h, equ_w, _ = im.shape
    equ_cx = (equ_w - 1) / 2.0
    equ_cy = (equ_h - 1) / 2.0

    wFOV = FOV
    w_len = np.tan(np.radians(wFOV / 2.0))      # 默认半径为1
    h_len = height / width * w_len

    x_map = np.linspace(-w_len, w_len, width).reshape((1, -1))
    y_map = np.linspace(-h_len, h_len, height).reshape((-1, 1))
    z_map = 1                                   # 默认半径为1
    D = np.sqrt(x_map**2 + y_map**2 + z_map**2)
    xyz = np.zeros([height, width, 3], np.float)
    xyz[:, :, 0] = x_map / D
    xyz[:, :, 1] = y_map / D
    xyz[:, :, 2] = z_map / D

    x_axis = np.array([1.0, 0.0, 0.0], np.float32)
    y_axis = np.array([0.0, 1.0, 0.0], np.float32)
    R1, _ = cv2.Rodrigues(y_axis * np.radians(THETA))
    R2, _ = cv2.Rodrigues(np.dot(R1, x_axis) * np.radians(PHI))
    R = R2 @ R1

    xyz = xyz @ R.T
    lat = np.arcsin(xyz[..., 1])
    lon = np.arctan2(xyz[..., 0], xyz[..., 2])

    lon = lon / np.pi * 180
    lat = lat / np.pi * 180
    lon = lon / 180 * equ_cx + equ_cx
    lat = lat / 90 * equ_cy + equ_cy

    persp = cv2.remap(im, lon.astype(np.float32), lat.astype(np.float32), cv2.INTER_CUBIC, borderMode=cv2.BORDER_WRAP)
    return persp


if __name__ == '__main__':
    import time
    frame = cv2.imread('src/image.jpg')
    n = 100
    s = time.time()
    for i in range(n):
        result = get_perspective(frame, 100, i % 360, 0, 720, 1080)
        cv2.imshow('a', result)
        if cv2.waitKey(1) == ord(' '):
            break
    print(n / (time.time() - s))
    frame = get_perspective(frame, 60, -200, 30, 720, 1080)
