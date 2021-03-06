# !/usr/bin/env python
# -*- coding:utf-8 -*-
# ================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : PyCharm
#   Project name: py-utils
#   File name   : scale_statistic.py
#   Author      : ylqi007
#   Created date: 2020-12-22 11:21 AM
#
# ================================================================

# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('--database', help='The database need to be statistic.')
#
# args = parser.parse_args()
#

import os
import numpy as np
import xml.etree.ElementTree as ET


def anchor_scales():
    anchor_sizes = [[0.0627878, 0.09495271],
                    [0.11484864, 0.23439993],
                    [0.86874759, 0.87105803]]
    # img_size = [300, 300]
    img_size = [1, 1]
    scale = []
    for size in anchor_sizes:
        scale.append(size[0] * size[1] / (img_size[0] * img_size[1]))
    scales = {}
    for i in np.arange(len(scale) - 1):
        s = (scale[i] + scale[i+1]) / 2
        scales[s] = 0
    print(scale)
    print(scales)
    return scales


def statistic(database):
    scales = anchor_scales()
    scales['1'] = 0
    keys = list(scales)
    for i in np.arange(len(keys)):
        print(keys[i])

    VOC2007_TRAIN = "/home/ylqi007/work/DATA/VOC2007/train/Annotations"
    annos = os.listdir(VOC2007_TRAIN)
    # UNT_TRAIN = "/home/ylqi007/work/DATA/UNT_Aerial_Dataset/train/Annotations"
    # annos = os.listdir(UNT_TRAIN)
    for anno in annos:
        anno = os.path.join(VOC2007_TRAIN, anno)
        root = ET.parse(anno).getroot()
        size = root.find('size')
        shape = [int(size.find('height').text),
                 int(size.find('width').text),
                 int(size.find('depth').text)]

        for obj in root.findall('object'):
            bndbox = obj.find('bndbox')
            bbox = [float(bndbox.find('ymin').text) / shape[0],
                    float(bndbox.find('xmin').text) / shape[1],
                    float(bndbox.find('ymax').text) / shape[0],
                    float(bndbox.find('xmax').text) / shape[1]]
            area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
            if area <= keys[0]:
                scales[keys[0]] += 1
            elif area <= keys[1]:
                scales[keys[1]] += 1
            elif area <= keys[2]:
                scales[keys[2]] += 1
            elif area <= keys[3]:
                scales[keys[3]] += 1
            elif area <= keys[4]:
                scales[keys[4]] += 1
            else:
                scales['1'] += 1
    print(scales)
    # print(annos)
    # print(database)


def statistic_COCO1():
    scales = anchor_scales()
    scales['1'] = 0
    keys = list(scales)

    COCO_train2007_with_size = os.path.join("/home/ylqi007/work/DATA/COCO", "train2017_with_size.txt")
    with open(COCO_train2007_with_size, 'r') as f:
        lines = f.readlines()
        for line in lines:
            anno = line.split()
            img_size = anno[1].split(',')
            img_size = [int(img_size[0]), int(img_size[1])]
            bboxes = np.array([list(map(lambda x: int(float(x)), box.split(','))) for box in anno[2:]])
            # print(anno)
            # print(img_size)
            # print(bboxes)
            for bbox in bboxes:
                area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) / (img_size[0] * img_size[1])
                if area <= keys[0]:
                    scales[keys[0]] += 1
                elif area <= keys[1]:
                    scales[keys[1]] += 1
                elif area <= keys[2]:
                    scales[keys[2]] += 1
                elif area <= keys[3]:
                    scales[keys[3]] += 1
                elif area <= keys[4]:
                    scales[keys[4]] += 1
                else:
                    scales['1'] += 1
    print(scales)


def statistic_COCO():
    scales = anchor_scales()
    scales['1'] = 0
    keys = list(scales)

    COCO_Train_Annos = "/home/ylqi007/work/DATA/COCO/COCO2017/train/Annotations"
    annos = os.listdir(COCO_Train_Annos)
    print(annos)
    for anno in annos:
        anno = os.path.join(COCO_Train_Annos, anno)
        root = ET.parse(anno).getroot()
        size = root.find('size')
        shape = [int(size.find('height').text),
                 int(size.find('width').text),
                 int(size.find('depth').text)]

        for obj in root.findall('object'):
            bndbox = obj.find('bndbox')
            bbox = [float(bndbox.find('ymin').text) / shape[0],
                    float(bndbox.find('xmin').text) / shape[1],
                    float(bndbox.find('ymax').text) / shape[0],
                    float(bndbox.find('xmax').text) / shape[1]]
            area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
            if area <= keys[0]:
                scales[keys[0]] += 1
            elif area <= keys[1]:
                scales[keys[1]] += 1
            else:
                scales['1'] += 1
    print(scales)


def statistic_VOC():
    scales = anchor_scales()
    scales['1'] = 0
    keys = list(scales)

    VOC2007_Train_Annos = "/home/ylqi007/work/DATA/VOC2007/train/Annotations"
    annos = os.listdir(VOC2007_Train_Annos)
    print(annos)
    for anno in annos:
        anno = os.path.join(VOC2007_Train_Annos, anno)
        root = ET.parse(anno).getroot()
        size = root.find('size')
        shape = [int(size.find('height').text),
                 int(size.find('width').text),
                 int(size.find('depth').text)]

        for obj in root.findall('object'):
            bndbox = obj.find('bndbox')
            bbox = [float(bndbox.find('ymin').text) / shape[0],
                    float(bndbox.find('xmin').text) / shape[1],
                    float(bndbox.find('ymax').text) / shape[0],
                    float(bndbox.find('xmax').text) / shape[1]]
            area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
            if area <= keys[0]:
                scales[keys[0]] += 1
            elif area <= keys[1]:
                scales[keys[1]] += 1
            else:
                scales['1'] += 1
    print(scales)


def statistic_UNT():
    scales = anchor_scales()
    scales['1'] = 0
    keys = list(scales)

    UNT_Train_Annos = "/home/ylqi007/work/DATA/UNT_Aerial_Dataset/train/Annotations"
    annos = os.listdir(UNT_Train_Annos)
    print(annos)
    for anno in annos:
        anno = os.path.join(UNT_Train_Annos, anno)
        root = ET.parse(anno).getroot()
        size = root.find('size')
        shape = [int(size.find('height').text),
                 int(size.find('width').text),
                 int(size.find('depth').text)]

        for obj in root.findall('object'):
            bndbox = obj.find('bndbox')
            bbox = [float(bndbox.find('ymin').text) / shape[0],
                    float(bndbox.find('xmin').text) / shape[1],
                    float(bndbox.find('ymax').text) / shape[0],
                    float(bndbox.find('xmax').text) / shape[1]]
            area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
            if area <= keys[0]:
                scales[keys[0]] += 1
            elif area <= keys[1]:
                scales[keys[1]] += 1
            elif area <= keys[2]:
                scales[keys[2]] += 1
            elif area <= keys[3]:
                scales[keys[3]] += 1
            elif area <= keys[4]:
                scales[keys[4]] += 1
            else:
                scales['1'] += 1
    print(scales)


if __name__ == '__main__':
    # statistic("args.database")
    anchor_scales()
    # statistic_VOC()
    # statistic_COCO()
    statistic_UNT()