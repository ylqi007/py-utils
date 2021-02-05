#! /usr/bin/env python3
# coding=utf-8
# ================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Author      : ylqi007
#   Editor      : PyCharm
#   Project name: PyCharm
#   File name   : get_coefficient.py
#   Created date: 2020-12-29 12:43 AM
#
# ================================================================
"""
Get the coefficient for different layer from the frequences of different scale objects.
For YOLOv3 and SSD
"""

import numpy as np


def get_coefficient(freqs):
    """
    Get coefficients from the frequencies of different scales.
    :param freqs:
    :return:
    """
    if type(freqs) is not np.ndarray:
        freqs = np.array(freqs)

    if freqs.ndim == 2:
        freqs = np.sum(freqs, axis=0)
    sum = np.sum(freqs)
    scale1 = freqs / sum
    scale2 = scale1 / scale1[0]
    scale3 = scale1 / scale1[-1]
    scale4 = scale1 * len(scale1)
    # Print in numpy array, i.e. without comma, like [1.9478e+04 2.2380e+03 1.1100e+02 8.0000e+00 1.0000e+00 1.0000e+00]
    # print("Original Scale: ", freqs)
    # print("Scale 1: ", scale1)
    # print("Scale 2: ", scale2)
    # print("Scale 3: ", scale3)
    # print("Scale 4: ", scale4)
    # Print in python list, i.e. with comma, like [19478.0, 2238.0, 111.0, 8.0, 1.0, 1.0]
    print("Original Scale: ", list(freqs))
    print("Scale 1: ", list(scale1))
    print("Scale 2: ", list(scale2))
    print("Scale 3: ", list(scale3))
    print("Scale 4: ", list(scale4))


if __name__ == '__main__':
    # YOLO + COCO
    # get_coefficient([464854, 465661, 240038])
    # SSD with 6 layers, Pascal VOC 2007
    # print("========== Pascal VOC 2007 ==========")
    # get_coefficient([5643, 3730, 2704, 1835, 1215, 535])
    # # SSD with 6 layers, COCO 2017
    # print("========== MS COCO 2017 ==========")
    # get_coefficient([551728, 151421, 78860, 42490, 22397, 13105])
    # SSD with 6 layers, UNT
    # Since the last two is 0, therefore we change 0 to 1
    # print("========== UNT ==========")
    # get_coefficient([19478, 2238, 111, 8, 1, 1])
    # print("========== Pascal VOC ==========")
    # get_coefficient([[2985, 8567, 13028, 8599, 5284, 2357],
    #                  [2932, 8485, 13266, 8756, 5384, 2339],
    #                  [3121, 8823, 13278, 8923, 5478, 2498],
    #                  [3148, 8938, 13529, 8815, 5280, 2484],
    #                  [2769, 8128, 13316, 8649, 5418, 2320]])

    # print("========== UNT ==========")
    # get_coefficient([[16217, 20811, 10471, 1959, 316, 24],
    #                  [16516, 21611, 10130, 1786, 355, 25],
    #                  [16623, 21116, 10456, 2065, 346, 28],
    #                  [16470, 21337, 10337, 1849, 296, 31],
    #                  [16059, 21570, 10057, 2044, 400, 40]])

    print("========== COCO ==========")
    get_coefficient([[137921, 209808, 229169, 135909, 75054, 29097],
                     [137858, 207081, 226878, 135791, 74539, 29162],
                     [137269, 208252, 228463, 136842, 74826, 29251],
                     [135432, 207732, 228334, 136850, 74951, 28827],
                     [137197, 209381, 227438, 136258, 74437, 28929],])

