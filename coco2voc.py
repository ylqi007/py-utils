#!/usr/bin/env python
# -*- coding:utf-8 -*-
# ================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : PyCharm
#   Project name: py-utils
#   File name   : coco2voc.py
#   Author      : ylqi007
#   Created date: 2020-12-23 12:40 PM
#
# ================================================================

"""
Convert COCO json file to xml file for each image.

xml:
    <annotation>
        <folder>VOC2007</folder>
        <filename>000005.jpg</filename>
        <size>
            <width>500</width>
            <height>375</height>
            <depth>3</depth>
        </size>
        <object>
            <name>chair</name>
            <bndbox>
                <xmin>263</xmin>
                <ymin>211</ymin>
                <xmax>324</xmax>
                <ymax>339</ymax>
            </bndbox>
        </object>
    </annotation>
"""

import os
import re
import argparse
import xml.etree.ElementTree as ET
from scripts import utils

from pycocotools.coco import COCO


parser = argparse.ArgumentParser()
parser.add_argument('--coco_json', help='The path of coco json file.')
parser.add_argument('--voc_dir', help='The output directory of VOC XML files.')

args = parser.parse_args()


def json_to_xml(src_json, xml_dir):
    if not os.path.exists(src_json):
        raise ValueError("COCO image dir `{}` does not exist.".format(src_json))

    # Read the total 91 classes
    classes91 = utils.read_class_names('./DATA/COCO/classes_paper.txt') # id -> class name
    # Read the 80 classes need to keep
    classes80 = utils.read_class_names('./DATA/COCO/classes_2017.txt')  # id --> class name
    reversed_classes80 = utils.reverse_dict(classes80)  # class name --> id

    coco = COCO(src_json)

    print('=======================')
    print(coco.cats)
    for img_id in coco.imgToAnns:
        img_anns = get_img_anno(coco.imgs[img_id], coco.imgToAnns[img_id], classes91, reversed_classes80, coco.cats)
        create_xml(xml_dir, img_anns)


def get_img_anno(img, anns, classes91, reversed_classes80, cats):
    """
    Get annotation for an image in COCO.
    # TODO: Specify which info or tags will be saved.
    :param img:
    :param anns:
    :param classes91:
    :param reversed_classes80:
    :param cats:
    :return:
    """
    img_anns = {}
    img_anns['folder'] = "train2017"    # TODO: Need to change manually
    img_anns['filename'] = img['file_name']
    img_anns['size'] = {}
    img_anns['size']['height'] = img['height']
    img_anns['size']['width'] = img['width']
    img_anns['size']['depth'] = 3
    img_anns['objects'] = []
    for ann in anns:
        name = re.sub('\W', "", cats[ann['category_id']]['name'])
        if name not in reversed_classes80:  # TODO: which classes will be kept or discard
            print(ann['category_id'], classes91[ann['category_id']])
            continue
        obj = {}
        obj['name'] = name
        obj['bndbox'] = {}
        obj['bndbox']['xmin'] = int(ann['bbox'][0])
        obj['bndbox']['ymin'] = int(ann['bbox'][1])
        obj['bndbox']['xmax'] = int(ann['bbox'][0] + ann['bbox'][2])
        obj['bndbox']['ymax'] = int(ann['bbox'][1] + ann['bbox'][3])

        img_anns['objects'].append(obj)
    return img_anns


def create_xml(dir=None, ann=None):
    """
    Create an XML file for a specific image. The tags are specified.
    # TODO: The tags are specified. If you need other tags, you need change this function.
    :param dir: The directory where the xmls will be saved in.
    :param ann: The annotation for an image.
    :return:
    """
    if ann is None:
        return
    root = ET.Element('annotation')
    for k in ann:
        if k is 'folder':
            folder = ET.SubElement(root, 'folder')
            folder.text = ann['folder']
        if k is 'filename':
            filename = ET.SubElement(root, 'filename')
            filename.text = ann['filename']
        if k is 'size':
            size = ET.SubElement(root, 'size')
            width = ET.SubElement(size, 'width')
            width.text = str(ann['size']['width'])
            height = ET.SubElement(size, 'height')
            height.text = str(ann['size']['height'])
            depth = ET.SubElement(size, 'depth')
            depth.text = str(ann['size']['depth'])
        if k is 'objects':
            for obj in ann[k]:
                object = ET.SubElement(root, 'object')
                name = ET.SubElement(object, 'name')
                name.text = obj['name']
                bndbox = ET.SubElement(object, 'bndbox')
                xmin = ET.SubElement(bndbox, 'xmin')
                xmin.text = str(obj['bndbox']['xmin'])
                ymin = ET.SubElement(bndbox, 'ymin')
                ymin.text = str(obj['bndbox']['ymin'])
                xmax = ET.SubElement(bndbox, 'xmax')
                xmax.text = str(obj['bndbox']['xmax'])
                ymax = ET.SubElement(bndbox, 'ymax')
                ymax.text = str(obj['bndbox']['ymax'])
    tree = ET.ElementTree(root)
    if not os.path.exists(dir):
        os.mkdir(dir)
    xml_file = os.path.join(dir, ann['filename'][:-4] + '.xml')
    with open(xml_file, 'wb') as file:
        tree.write(file)


def get_details(coco):
    print('coco', coco)
    print('coco.dataset:\t', type(coco.dataset), len(coco.dataset), coco.dataset.keys())
    print("coco.anns:\t", type(coco.anns), len(coco.anns))
    print("coco.cats:\t", type(coco.cats), len(coco.cats))  # Only 80 classes, but class ids are not continuous.
    print("coco.imgs:\t", type(coco.imgs), len(coco.imgs))
    print("coco.imgToAnns:\t", type(coco.imgToAnns), len(coco.imgToAnns))
    print("coco.catToImgs:\t", type(coco.catToImgs), len(coco.catToImgs))
    print(type(coco))
    print(type(coco.dataset), len(coco.dataset))
    print("=========================================================================")
    print("coco.imgs:\t", len(coco.imgs))
    print("coco.imgToAnns:\t", len(coco.imgToAnns))


if __name__ == '__main__':
    json_to_xml(args.coco_json, args.voc_dir)
