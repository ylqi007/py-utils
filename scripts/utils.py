#! /usr/bin/env python
# coding=utf-8
# ================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : pycharm
#   File name   : utils.py
#   Author      : ylqi007
#   Created date: 2020-11-09 11:49 AM
#   Description :
#
# ================================================================

import os
import re
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import xml.etree.ElementTree as ET


COCO_DIR = '/home/ylqi007/work/DATA/COCO'


def read_class_names(file_name, write_file=None, w=False):
    """ Loads class name from a txt file. """
    names = {}
    with open(file_name, 'r') as file:
        for ID, name in enumerate(file):
            names[ID] = name.strip('\n')
    if write_file and w:
        with open(write_file, 'w') as file:
            file.truncate(0)
            for ID in names.keys():
                print(ID, names[ID])
                file.writelines((names[ID] + ("" if ID == len(names) - 1 else '\n')))
    return names


def classes_to_keep():
    # Read the total 91 classes
    classes91 = read_class_names('./dataset/coco-labels-paper.txt',
                                 write_file='./dataset/coco-labels-paper.names')
    # Read the 80 classes need to keep
    classes80 = read_class_names('./dataset/coco-labels-2014_2017.txt',
                                 write_file='./dataset/coco-labels-2014_2017.names')
    return classes91, classes80


def reverse_dict(dictionary):
    reversed_dict = {v: k for k, v in dictionary.items()}
    return reversed_dict


def draw_bounding_box(img, xml):
    """
    For testing the correctness of xml files.

    :param img: The image will be read.
    :param xml: The corresponding xml for the image.
    :return:
    """
    if not os.path.exists(img):
        raise ValueError("Image file does not exist.")
    if not os.path.exists(xml):
        raise ValueError("XML file does not exist.")
    im = Image.open(img)
    fig, ax = plt.subplots()
    anns = []
    ax.imshow(im)
    root = ET.parse(xml)
    for obj in root.findall('object'):
        xmin = int(obj.find('bndbox').find('xmin').text)
        ymin = int(obj.find('bndbox').find('ymin').text)
        xmax = int(obj.find('bndbox').find('xmax').text)
        ymax = int(obj.find('bndbox').find('ymax').text)
        name = obj.find('name').text
        ann = [xmin, ymin, xmax, ymax, name]
        anns.append(ann)
        ax.add_patch(patches.Rectangle((xmin, ymin), xmax-xmin, ymax-ymin, linewidth=1, edgecolor='r', facecolor='none'))
        ax.text(xmin, ymin, name, color='red')
    plt.show()


def write_labels():
    """
    What Object Categories / Labels Are In COCO Dataset?
    https://tech.amikelive.com/node-718/what-object-categories-labels-are-in-coco-dataset/

    Read COCO classes of all versions(COCO/classes_coco_labels.txt), including COCO paper,
    COCO 2014 and COCo 2017, and then write class names to separate files,
    i.e. COCO/classes_paper.txt, COCO/classes_2014.txt, COCO/classes_2017.txt.

    :return: None
    """
    label_file = '/home/ylqi007/work/DATA/COCO/classes_coco_labels.txt'
    classes_paper = os.path.join(COCO_DIR, 'classes_paper.txt')
    classes_2014 = os.path.join(COCO_DIR, 'classes_2014.txt')
    classes_2017 = os.path.join(COCO_DIR, 'classes_2017.txt')
    with open(label_file, 'r') as flabel, open(classes_paper, 'w') as fpaper, \
            open(classes_2014, 'w') as f2014, open(classes_2017, 'w') as f2017:
        lines = flabel.readlines()
        for line in lines:
            line1 = line.split('\t')
            line2 = [re.sub(r'\W', "", item) for item in line1]
            if line2[1] is not '':
                fpaper.write(line2[1] + '\n')
            if line2[2] is not '':
                f2014.write(line2[2] + '\n')
            if line2[3] is not '':
                f2017.write(line2[3] + '\n')


if __name__ == '__main__':
    # read_class_names('./dataset/coco-labels-paper.txt', write_file='./dataset/coco-labels-paper.names')
    # read_class_names('./dataset/coco-labels-2014_2017.txt', write_file='./dataset/coco-labels-2014_2017.names')
    # classes_to_keep()

    # Test correctness of XML files
    # TODO: Test example for Pascal VOC 2007
    # img = '/home/ylqi007/work/DATA/VOC2007/train/JPEGImages/000104.jpg'
    # ann = '/home/ylqi007/work/DATA/VOC2007/train/Annotations/000104.xml'
    # TODO: Test example for COCO2017 val
    # img = '/home/ylqi007/work/DATA/COCO/val2017/000000001503.jpg'
    # ann = '/home/ylqi007/work/DATA/COCO/val2017_Annotations/000000001503.xml'
    # TODO: Test example for COCO2017 train
    img = '/home/ylqi007/work/DATA/COCO/train2017/000000000813.jpg'
    ann = '/home/ylqi007/work/DATA/COCO/train2017_Annotations/000000000813.xml'
    draw_bounding_box(img, ann)

    # Read acn write classes file for COCO
    # write_labels()
