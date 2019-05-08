# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:02:21 2019

@author: Administrator
"""

import cv2
import os.path as osp
import os

def resize(file_path,size=None,out_dir=None):
    
    if out_dir is None:
        out_dir=osp.join(file_path,'resize')
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
    
    for file_name in os.listdir(file_path):
        img_p=osp.join(file_path,file_name)
        if os.path.isfile(img_p):
#            print('正在处理：{}'.format(file_name))
            img_o=cv2.imread(img_p)
            if size is not None:            
                img_n=cv2.resize(img_o,size)
            else:
                img_n=img_o
#            print('原图大小{};现大小{}'.format(img_o.shape,img_n.shape))
            cv2.imwrite(osp.join(out_dir,'{}.jpg'.format(file_name.replace('.tif',''))),img_n)
            
            
if __name__ == '__main__':
    resize(r"E:\work\01-Myproject\imag_division\all2\pic",)
