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

def read_class_names(file_name, write_file=None):
    """ Loads class name from a txt file. """
    names = {}
    with open(file_name, 'r') as file:
        for ID, name in enumerate(file):
            names[ID] = name.strip('\n')
    if write_file:
        with open(write_file, 'w') as file:
            file.truncate(0)
            for ID in names.keys():
                print(ID, names[ID])
                file.writelines((names[ID] + ("" if ID == len(names) - 1 else '\n')))
    return names


if __name__ == '__main__':
    read_class_names('./dataset/coco-labels-paper.txt', write_file='./dataset/coco-labels-paper.names')
    read_class_names('./dataset/coco-labels-2014_2017.txt', write_file='./dataset/coco-labels-2014_2017.names')