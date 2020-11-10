#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project Name: py-utils - 当前项目的名称。 
# Author: yq0033
# Datetime: 10/19/20 7:59 PM
# Software: PyCharm

import os
import matplotlib.pyplot as plt
from pycocotools.coco import COCO
from scripts import utils


COCO_FULL = "dataset/coco_info.names"
COCO_2017 = "dataset/coco_2017.names"

# For Docker
# PRE_DIR = "/tensorflow-yolov3/"

# For Lab-207, 1080 and 2080Ti
DATA_DIR = "/home/yq0033/work/"
CUR_DIR = os.getcwd()   # /home/yq0033/work/PycharmProjects/py-utils


# COCO 2017, TRAIN
COCO_2017_TRAIN_IMG_DIR = "DATA/COCO/train2017/"
COCO_2017_TRAIN_ANNO_DIR = "DATA/COCO/annotations_trainval2017/annotations/instances_train2017.json"
COCO_2017_TRAIN_to_VOC_ANNO_DIR = "DATA/COCO/coco_train2017.txt"

# COCO 2017, VAL
COCO_2017_VAL_IMG_DIR = "DATA/COCO/val2017/"
COCO_2017_VAL_ANNO_DIR = "DATA/COCO/annotations_trainval2017/annotations/instances_val2017.json"
COCO_2017_VAL_to_VOC_ANNO_DIR = "DATA/COCO/coco_val2017.txt"

# COCO 2017, TEST
COCO_2017_TEST_IMG_DIR = "DATA/COCO/test2017/"
COCO_2017_TEST_ANNO_DIR = "DATA/COCO/annotations_trainval2017/annotations/image_info_test2017.json"
COCO_2017_TEST_to_VOC_ANNO_DIR = "DATA/COCO/test2017.txt"


def coco2voc(coco_img_dir, coco_anno_dir, voc_anno_dir):
    if not os.path.exists(coco_img_dir):
        raise ValueError("COCO image dir `{}` does not exist.".format(coco_img_dir))

    if not os.path.exists(coco_anno_dir):
        raise ValueError("COCO anno dir `{}` does not exist.".format(coco_anno_dir))

    coco_2017 = utils.read_class_names('./dataset/coco-labels-2014_2017.txt')
    coco = COCO(coco_anno_dir)

    # print('====================================================')
    # print('coco', coco)
    # print('coco.dataset: ', len(coco.dataset))
    # print("Number of images:\t", len(coco.imgs))
    # print("Number of object:\t", len(coco.anns))
    # print("Number of imgToAnnos:\t", len(coco.imgToAnns))
    # print(coco.cats)
    # print('====================================================')
    sample_image_ids = [386134, 97585, 429530, 31749, 284282]      # samples in imgToAnns
    vocFile = open(voc_anno_dir, 'a')
    for imgId in coco.imgs.keys():
        # if imgId not in sample_image_ids:    # Just samples
        #     # continue
        # print("======================= split line =============================")
        annos = coco.imgToAnns[imgId]   # anns of objects in one image
        if len(annos) == 0:
            print('image without objects: ', coco.imgs[imgId])
            continue
        image_path = os.path.join(DATA_DIR, coco_img_dir, coco.imgs[imgId]["file_name"])
        # print("## Width: ", coco.imgs[imgId]["width"])
        # print("## Height: ", coco.imgs[imgId]["height"])
        # L = imagePath + " " + "{},{} ".format(coco.imgs[imgId]["width"], coco.imgs[imgId]["height"])
        L = image_path + " "
        for anno in annos:
            _bbox = anno["bbox"]
            _bbox = [_bbox[0], _bbox[1], _bbox[0] + _bbox[2], _bbox[1] + _bbox[3]]
            bbox = [int(_bbox[0]), int(_bbox[1]), int(_bbox[2]), int(_bbox[3]), ]
            class_id = anno["category_id"]              # class id in 91 classes
            class_name = coco.cats[class_id]['name']    # class name in 91 classes
            # if class_name not in coco_2017:
            #     raise ValueError("{} : {} not found".format(class_id, class_name))
            if class_name in coco_2017:
                class_id = coco_2017[class_name]        # class id in 80 classes
                L += "{},{},{},{},{} ".format(bbox[0], bbox[1], bbox[2], bbox[3], class_id)
        vocFile.writelines((L + '\n'))
    vocFile.close()


# def coco_to_coco2017(coco_full_id, coco_full_dict, coco_2017_dict):
#     """
#     In coco 2017, there has classes which appear in coco2014 but not in coco2017.
#     For a class appears in coco2017, but it still may not appear in 80 classes.
#     dict of coco_2017: class_name -> id
#     coco_full[category_id] = class_name
#     coco_2017[class_name] = id
#
#     coco_full: id -> class
#     coco_2017: class -> id
#     :return:
#     """
#     # if coco_full_dict[coco_full_id] is '-':
#     #     print("Not a class in COCO2017", "Skip", coco_full_dict[coco_full_id])
#     #     pass
#     class_name = coco_full_dict[coco_full_id]
#     return coco_2017_dict[class_name]


def get_coco_full(file=COCO_FULL):
    id_to_name = {}
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            items = line.split('\t')
            if items[-2] is '-':    # no in 80 classes
                continue
            _id = int(items[0])
            _name = items[-2].replace(" ", "")
            id_to_name[_id] = _name
    # for id in id_to_name:
    #     print(id, id_to_name[id])
    return id_to_name


def get_coco_2017(file=COCO_2017):
    class_to_id = {}
    with open(file, 'r') as data:
        for id, name in enumerate(data):
            # print(name.strip('\n'))
            class_to_id[name.strip('\n')] = id
    # for name in class_to_id:
    #     print(name, class_to_id[name])
    return class_to_id


if __name__ == "__main__":
    # TRAIN
    # coco2voc(coco_img_dir=COCO_2017_TRAIN_IMG_DIR,
    #          coco_anno_dir=COCO_2017_TRAIN_ANNO_DIR,
    #          voc_anno_dir=COCO_2017_TRAIN_to_VOC_ANNO_DIR)
    # VAL
    coco2voc(coco_img_dir=COCO_2017_VAL_IMG_DIR,
             coco_anno_dir=COCO_2017_VAL_ANNO_DIR,
             voc_anno_dir="DATA/COCO/_coco_val2017.txt")
    # Test. Since there are no annotations for test dataset, there is no use to run the following.
    # coco2voc(coco_img_dir=COCO_2017_TEST_IMG_DIR,
    #          coco_anno_dir=COCO_2017_TEST_ANNO_DIR,
    #          voc_anno_dir=COCO_2017_TEST_to_VOC_ANNO_DIR)

    # get_coco_full()
    # get_coco_2017()
