#!/usr/bin/env bash

# Val2017
#COCO_JSON="/home/ylqi007/work/DATA/COCO/annotations_trainval2017/annotations/instances_val2017.json"
#VOC_DIR="/home/ylqi007/work/DATA/COCO/val2017_Annotations/"

# Train2017
COCO_JSON="/home/ylqi007/work/DATA/COCO/annotations_trainval2017/annotations/instances_train2017.json"
VOC_DIR="/home/ylqi007/work/DATA/COCO/train2017_Annotations/"

python coco2voc.py  \
  --coco_json ${COCO_JSON}  \
  --voc_dir ${VOC_DIR}