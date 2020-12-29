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
    freqs = np.array(freqs)
    sum = np.sum(freqs)
    scale1 = freqs / sum
    scale2 = scale1 / scale1[0]
    scale3 = scale1 / scale1[-1]
    scale4 = scale1 * len(scale1)
    # print("Original Scale: ", freqs)
    # print("Scale 1: ", scale1)
    # print("Scale 2: ", scale2)
    # print("Scale 3: ", scale3)
    # print("Scale 4: ", scale4)
    print("Scale 1: ", list(scale1))
    print("Scale 2: ", list(scale2))
    print("Scale 3: ", list(scale3))
    print("Scale 4: ", list(scale4))


if __name__ == '__main__':
    # YOLO + COCO
    # get_coefficient([464854, 465661, 240038])
    # SSD with 6 layers, Pascal VOC 2007
    get_coefficient([5643, 3730, 2704, 1835, 1215, 535])

