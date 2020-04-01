#!/usr/bin/env python
# coding: utf-8

# In[2]:


import cv2 as cv
import numpy as np


# In[58]:


def find_pattern(bkg_img, img_tmpl, thrd=0.9, draw_out_img=False):
    #pth_img = '/home/brian/Desktop/REWE/opencv/img/'
    #bkg_img = pth_img+'Sc.png'
    #img_tmpl = pth_img+'folder'+'.png'#'looper.png'
    #thrd = 0.9 #0.8 
    
    img_rgb = cv.imread(bkg_img)
    img_bw  = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    #print(img_bgr.shape) #height,width,color
    template = cv.imread(img_tmpl, 0)
    
    res = cv.matchTemplate(img_bw, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= thrd)
    
    if draw_out_img:
        h, w = template.shape
        
        for pt in zip(*loc[::-1]):
            #print(pt)
            cv.rectangle(img_rgb, pt, (pt[0]+w,pt[1]+h), (0,255,255), 2)
            
        #cv.imshow('detected', img_bgr)
        cv.imwrite(pth_img+'detected.png', img_rgb)
        
    if len(loc) != 0:     
        return loc[0][0], loc[1][0] #first x, y
    else:
        return -1




if __name__ == "__main__":
    pth_img = '/home/brian/Desktop/REWE/opencv/img/'
    bkg_img = pth_img+'Sc.png'
    img_tmpl = pth_img+'folder'+'.png'#'looper.png'

    print(find_pattern(bkg_img, img_tmpl, 0.8))

