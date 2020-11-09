[toc]

# py-utils

## Function
1. Convert coco annotations (i.e. json) to voc format for [`YOLOv3-tensorflow`](https://github.com/YunYang1994/tensorflow-yolov3) (i.e. txt file and each line representing an image.)

## Usage
### 1. Convert COCO annotations to VOC format
```bash
python coco2pascal.py
```

Analysis:
1. `coco.imgToAnns` is a dictionary, with key the `img_id` and value the `anns` for that image. Only images in this key set has annotations.
2. `coco.anns` is annotations in all images, and each annotation is an object.



## Explanation

> As written in the [original research paper](https://arxiv.org/abs/1405.0312), there are 91 object categories in COCO. However, only 80 object  categories of labeled and segmented images were released in the first  publication in 2014. Currently there are two releases of COCO dataset  for labeled and segmented images. After the 2014 release, the subsequent release was in 2017. The COCO dataset is available for download from  the [download page](http://cocodataset.org/#download).

```
dataset/
	|--> coco-labels-paper.txt		# 91 classes in the original paper
	|--> coco-labels-2014-2017.txt	# 80 classes labeled in the COCO dataset, name with space
```




## [Data Format](https://cocodataset.org/#format-data)
COCO 有几种不同的标记类型，分别对应 object detection, keypoint detection, stuff segmentation,
panoptic segmentation, densepose, and image captioning.
标记都保存在 JSON 文件中。
All annotations share the same basic data structure below:
![The basic data structure](./assets/images/coco_annotation_basic.png)
* Annotations file 的基本结构类似与 python 中的 dict 结构，包括四个 key-value 对，如下所示：
```
# annotations
"info": info,
"images": [image],
"annotations": [annotation],
"licenses": [license]
```
    * 其中 "info" 定义一些数据库信息，比如本版，年份等等。
    * 其中 "images" 定义了一个 list，每个 element 对应一张 image 的信息，包括 id, width, height,
    file_name, coco_url 等等。
    * 其中 "annotations" 定义了一个 list，每个 element 对应一张 image 的标注信息，对于每种 task，
    标注信息又有些区别。

The data structure specific to the various annotation types are described below:

### 1. Object Detection
* Each object instance `annotation` contains a series of fields, including the category id and 
segmentation mask of the object. 每个 `annotation` (注意，不加 `s`，说明这是对应一张 image 的标注)
包含了一些列 fields，比如 类别 ID 等等。
* In addition, an `enclosing bounding box` is provided for **each object** (box coordinates are 
measured from the top left image corner and are 0-indexed).
* The categories field of the annotation structure stores the mapping of category id to category 
and supercategory names.

```
annotation {
    "id" : int,                         # Category ID
    "image_id" : int,                   # Useful for object detection.
    "category_id" : int,
    "segmentation" : RLE or [polygon],
    "area" : float,
    "bbox" : [x,y,width,height],        # A list of `x,y,width,height`, corresponding to each object. 
    "iscrowd" : 0 or 1,
}

categories[{
    "id" : int,
    "name" : str,
    "supercategory" : str,
}]
```

对于 `val2017`，有 5000 image，但是却有 36781 anno。所以 一个 anno 对应的是 5000 image 中的一个 object。
image 与 anno 的对应信息通过 `imgToAnns` 定义。

### 2. 关于几个 `id` 的理解
* 每个 anno 都有两个 id，一个是 `"id"`, 另一个是 `"image_id"`;
    * 其中 `"id"` 用于标记每个 object 的 anno。
    * 其中 `"image_id"` 用于标记这个 anno 属于哪一张 image。 
* 每张 image 都由自身的 `"id"` 标记， `coco.imgs[img[id]] = img`

## VOC
annotation
    folder
    filename: 000005.jpg
    source
    owner
    size: 
        width:
        height:
        depth:
    segmented:
    object:
        name:
        bndbox:
            xmin
            ymin
            xmax
            ymax
    object:
    object:

YOLOv3 need:
image_path x_min, y_min, x_max, y_max, class_id  x_min, y_min ,..., class_id 
- [x] image_path
- [x] x_min, y_min, x_max, y_max
- [ ] class_id

### 关于 class id
* [What Object Categories / Labels Are In COCO Dataset?](https://tech.amikelive.com/node-718/what-object-categories-labels-are-in-coco-dataset/)
* [amikelive/coco-labels](https://github.com/amikelive/coco-labels)
* [JackLongKing](https://github.com/cocodataset/cocoapi/issues/59#issuecomment-315663672)
* [kenrobio](https://github.com/cocodataset/cocoapi/issues/272#issuecomment-628393716)
* [Data format](https://cocodataset.org/#format-data)
* [cocodataset](https://github.com/cocodataset)/**[cocoapi](https://github.com/cocodataset/cocoapi)** 



## Statistic and choose the top 20

- [ ] 统计 COCO 数据库中，80 个 classes 中出现频率最高的 20 classes。在生成的训练需要的 VOC format
  annotations 的时候，只寻则出现频率最高的 20 classes。

```
`dict = {class_id: [class_name, freq]}`
```