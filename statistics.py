#! /usr/bin/env python3
# coding=utf-8
# ================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Author      : ylqi007
#   Editor      : PyCharm
#   Project name: PyCharm
#   File name   : statistics.py
#   Created date: 2020-11-04 8:16 PM
#
# ================================================================
import os
import numpy as np
import collections


def read_classes_name(coco_classes="./dataset/coco_2017.names"):
    if not os.path.exists(coco_classes):
        raise ValueError("File {} does not exist.".format(coco_classes))
    id_to_class = {}
    with open(coco_classes, 'r') as data:
        for id, name in enumerate(data):
            id_to_class[id] = [name.strip('\n')]
    return id_to_class


def statistic_frequency(id_to_class=None, dir="./DATA/COCO/", file="coco_train2017.txt"):
    file = os.path.join(dir, file)
    if not os.path.exists(file):
        raise ValueError("File {} does not exist.".format(file))
    if id_to_class is None:
        id_to_class = read_classes_name()
    with open(file, 'r') as data:
        for anno in data:
            line = anno.split()
            bboxes = np.array([list(map(lambda x: int(float(x)), box.split(','))) for box in line[2:]])
            for box in bboxes:
                if len(id_to_class[box[-1]]) == 1:
                    id_to_class[box[-1]].append(1)
                else:
                    id_to_class[box[-1]][-1] += 1
    reverse_sorted_id_to_class = {k: v for k, v in sorted(id_to_class.items(), key=lambda item: item[1][-1], reverse=True)}

    keep_classes = {}
    i = 0
    for key in reverse_sorted_id_to_class:
        keep_classes[key] = reverse_sorted_id_to_class[key] + [i]
        i += 1
        if i == 20:
            break
    print(keep_classes)
    with open("dataset/coco_top20.names", "w") as file:
        for key in keep_classes:
            file.writelines(keep_classes[key][0] + "\n")
    return keep_classes


def read_class_names(class_file_name):
    '''loads class name from a file'''
    names = {}
    with open(class_file_name, 'r') as data:
        for ID, name in enumerate(data):
            names[ID] = name.strip('\n')
    return names


def select_top20_classes(dir="./DATA/COCO/", file="coco_val2017.txt"):
    keep_classes = statistic_frequency(id_to_class=None, dir="./DATA/COCO/", file="coco_train2017.txt")
    print(keep_classes.keys())
    print(keep_classes.items())
    # filter
    filtered_voc_file = open("./DATA/COCO/coco_val2017_top20.txt", 'w')
    file = os.path.join(dir, file)
    with open(file, 'r') as data:
        for anno in data:
            line = anno.split()
            tmp = line[0].split('/')
            img_path = os.path.join("/home/yq0033/work/DATA/", tmp[-3], tmp[-2], tmp[-1])
            bboxes = np.array([list(map(lambda x: int(float(x)), box.split(','))) for box in line[2:]])
            L = ""
            for bbox in bboxes:
                if bbox[-1] in keep_classes.keys():
                    L += "{},{},{},{},{} ".format(bbox[0], bbox[1], bbox[2], bbox[3], keep_classes[bbox[4]][-1])
            if len(L) > 0:
                L = img_path + " " + L
                filtered_voc_file.write((L + '\n'))
    filtered_voc_file.close()


if __name__ == '__main__':
    # statistic_frequency()

    select_top20_classes()
