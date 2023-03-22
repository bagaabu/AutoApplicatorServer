import cv2
import os
import sys

import torch

from app.detector import detector_checker, chart_checker


def detect_test(img):
    liness, ptss, ptss_curve, _, zx_scale, zx_rotate, zx_rotate_score = detector_checker.inference(img, True)
    return liness, ptss, ptss_curve, zx_scale, zx_rotate, zx_rotate_score


if __name__ == '__main__':
    img = cv2.imread('../zlt0708.jpg', 1)
    detect_test(img)