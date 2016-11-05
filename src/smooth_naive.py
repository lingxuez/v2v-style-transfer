import numpy as np
import os, re
import argparse
from PIL import Image

def load_image(path, size):
    #coppied from Github, Feifei's method
    #size and crop are not used for now
    image = Image.open(path).convert('RGB')
    
    #w,h = image.size
    #if w < h:
    #    if w < size:
    #        image = image.resize((size, size*h/w))
    #        w, h = image.size
    #else:
    #    if h < size:
    #        image = image.resize((size*w/h, size))
    #        w, h = image.size
    #image = image.crop(((w-size)*0.5, (h-size)*0.5, (w+size)*0.5, (h+size)*0.5))
    return np.asarray(image)


def smooth_naive(images, styledim, threshold, size, outdir, outprefix = "frame"):
    # a naive way to find the difference part of connective frames
    # for the different part, keep yhat
    # for similar part, use yhat_{-1}
    imgold = None
    styimgold = None
    for i in range(len(images)):
        image = images[i]
        styimage = sty_images[i]
        if not os.path.exists(image):
            raise IOError(image)
        if not os.path.exists(styimage):
            raise IOError(styimage)
        imgnew = load_image(image, size)
        imgnew.flags.writeable = True  
        styimgnew = load_image(styimage, size)
        styimgnew.flags.writeable = True  
        if i > 0:
            diff = abs(imgnew - imgold)
            styimgnew[diff < threshold] = styimgold[diff < threshold]  
        im = Image.fromarray(styimgnew)      
        im.save("%s%s%d.jpg" % (outdir, outprefix, i*10))          
        imgold = imgnew
        styimgold = styimgnew
        
            

if __name__ == "__main__":    
     imageDir = "../data/frames/"
     images = [imageDir + imageName for imageName in os.listdir(imageDir)]
     images.sort(key=lambda name: int(re.sub("\D", "", name))) 
   
     sty_imageDir = "../data/frames_styled/"
     sty_images = [sty_imageDir + imageName for imageName in os.listdir(sty_imageDir)]
     sty_images.sort(key=lambda name: int(re.sub("\D", "", name)))
     
     outDir = "../data/frames_naive/"
     
     smooth_naive(images, sty_images, 10, 1024, outDir)

