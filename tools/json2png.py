# -*- coding: utf-8 -*-
"""
Created on Wed May  8 12:16:51 2019

@author: Administrator
"""

import base64
import json
import os
import os.path as osp

import PIL.Image
import yaml

from labelme.logger import logger
from labelme import utils

import numpy as np

def json2png(json_file,lab2val = {'_background_': 0}):


#    json_file = args.json_file

    label_name_to_value=lab2val
    out_dir = osp.basename(json_file).replace('.', '_')
    out_dir = osp.join(osp.dirname(json_file), out_dir)
    out_png = osp.join(osp.dirname(json_file),'png')
    out_pngviz=osp.join(osp.dirname(json_file),'png_viz')
    out_pic=osp.join(osp.dirname(json_file),'pic')

    if not osp.exists(out_dir):
        os.mkdir(out_dir)
    
    if not osp.exists(out_png):
        os.mkdir(out_png)
        
    if not osp.exists(out_pngviz):
        os.mkdir(out_pngviz)

    if not osp.exists(out_pic):
        os.mkdir(out_pic)
        
    data = json.load(open(json_file))

    if data['imageData']:
        imageData = data['imageData']
    else:
        imagePath = os.path.join(os.path.dirname(json_file), data['imagePath'])
        with open(imagePath, 'rb') as f:
            imageData = f.read()
            imageData = base64.b64encode(imageData).decode('utf-8')
    img = utils.img_b64_to_arr(imageData)

    for shape in sorted(data['shapes'], key=lambda x: x['label']):
        label_name = shape['label']
        if label_name in label_name_to_value:
            label_value = label_name_to_value[label_name]
        else:
            label_value = len(label_name_to_value)
            label_name_to_value[label_name] = label_value
    lbl = utils.shapes_to_label(img.shape, data['shapes'], label_name_to_value)
    label_names = [None] * (max(label_name_to_value.values()) + 1)
    for name, value in label_name_to_value.items():
        label_names[value] = name
    lbl_viz = utils.draw_label(lbl, img, label_names)
    
    
    
    
    PIL.Image.fromarray(img).save(osp.join(out_pic, osp.basename(json_file).replace('.json', '')+'.jpg'))
    PIL.Image.fromarray(img).save(osp.join(out_dir, 'img.png'))
    PIL.Image.fromarray(lbl).save(osp.join(out_png, osp.basename(json_file).replace('.json', '')+'.png'))
    
    
    
#    utils.lblsave(osp.join(out_png, osp.basename(json_file).replace('.json', '')+'.png'), lbl)
    utils.lblsave(osp.join(out_dir, 'label.png'), lbl)
    PIL.Image.fromarray(lbl_viz).save(osp.join(out_pngviz,osp.basename(json_file).replace('.json', '')+'.png'))
    PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, 'label_viz.png'))

    with open(osp.join(out_dir, 'label_names.txt'), 'w') as f:
        for lbl_name in label_names:
            f.write(lbl_name + '\n')

    logger.warning('info.yaml is being replaced by label_names.txt')
    info = dict(label_names=label_names)
    with open(osp.join(out_dir, 'info.yaml'), 'w') as f:
        yaml.safe_dump(info, f, default_flow_style=False)

    logger.info('Saved to: {}'.format(out_dir))


if __name__ == '__main__':
    
    json_path=r"E:\work\01-Myproject\imag_division\all\resize\json_file"
    
    lab2val = {'_background_': 0,'M':1,'O':2}
    
    json_list=os.listdir(json_path)
    for json_file in json_list:
        json_p=osp.join(json_path,json_file)
        if os.path.isfile(json_p):
            json2png(json_p,lab2val)
