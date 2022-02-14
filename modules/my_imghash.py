#!/usr/bin/python

"""
Created on Fri Jul 13 15:16:13 2018

@author: yongsongzhu
"""

#import os
#import sys

import cv2
import numpy as np
from PIL import Image
from functools import reduce


class ImageMatch(object):
    def __init__(self):        
        print("Currently only ahash, phash and dhash are supported\n")
        
    def ahash(self,im, win_size=32):
        if not isinstance(im, Image.Image):
            im = Image.open(im)
            print("debug1")
        im = im.resize((win_size, win_size), Image.ANTIALIAS).convert('L')
        print("debug2")
        avg = reduce(lambda x, y: x + y, im.getdata()) / (win_size*win_size)   
        mat = ['0' if i<avg else '1' for i in im.getdata()]
        #return reduce(lambda x, y, z: x | (z << y),
                  #enumerate([0 if i < avg else 1 for i in im.getdata()]),
                  #0)
        return int(''.join(['%x' % int(''.join(mat[x:x+4]),2) for x in range (0,win_size*win_size,4)]),16)
                
    def phash(self, im, win_size=16):            
        if not isinstance(im, Image.Image):
            im = Image.open(im)
        im = im.resize((win_size*2, win_size*2), Image.ANTIALIAS).convert('L')        
        m_img = np.float32(im)
        img_dct = cv2.dct(m_img)
        img_mean = cv2.mean(img_dct[0:win_size, 0:win_size])
        mat = []
        for i in range(win_size):
            mat = mat + ['0' if x < img_mean[0] else '1' for x in img_dct[i, 0:win_size]]
            #print (mat)
        #return reduce(lambda x, y, z: x | (z << y), enumerate(mat), 0)
        return int(''.join(['%x' % int(''.join(mat[x:x+4]),2) for x in range(0,32*32,4)]),16)
        
    def dhash(self, im, win_size=8):
        img = cv2.imread(im)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)        
        # dsize=(width, height)
        m_img = cv2.resize(gray, dsize=(win_size+1, win_size))
        m_img = np.int8(m_img)        
        m_img_diff = m_img[:, :-1] - m_img[:, 1:]        
        mat = []
        for i in range(win_size):
            mat = mat + [0 if x < 0 else 1 for x in m_img_diff[i, :]]
        return reduce(lambda x, y, z: x | (z << y), enumerate(mat), 0)
         

    def hamming(self, h1, h2):
        h, d = 0, h1 ^ h2
        #print d, h1, h2
        while d:
            h += 1            
            d &= d - 1
        return h
    
    def match(self, src_img_file, dst_img_file, mode='ahash', win_size=32):
        print("match method: %s" % mode)
        if mode == "ahash":
            ref_hash = self.ahash(src_img_file, win_size)
            dst_hash = self.ahash(dst_img_file, win_size)
        elif mode == "phash":
            ref_hash = self.phash(src_img_file, win_size)
            dst_hash = self.phash(dst_img_file, win_size) 
        elif mode == "dhash":
            ref_hash = self.dhash(src_img_file, win_size)
            dst_hash = self.dhash(dst_img_file, win_size) 
        else:
            print("Match method is not specified")
            return -1
            
        return self.hamming(ref_hash, dst_hash)
      
if __name__ == '__main__':
    #ref_img = '480i_1.jpg'
    ref_img = 'INPUT_002_ref.jpg'
    dst_img = 'INPUT_002.jpg'
    #dst_img = '20180706104719.jpg'
    
    myMatchImage = ImageMatch()
    result = myMatchImage.match(ref_img, dst_img, mode="ahash", win_size=32)
    print("Result: ham %d\t%s\t%s" % (result, ref_img, dst_img))
    
    #result = myMatchImage.match(ref_img, dst_img, mode="phash", win_size=32)
    #print("Result: ham %d\t%s\t%s" % (result, ref_img, dst_img))
    
    #result = myMatchImage.match(ref_img, dst_img, mode="dhash", win_size=32)
    #print("Result: ham %d\t%s\t%s" % (result, ref_img, dst_img))
    


