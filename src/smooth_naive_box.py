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
    return np.asarray(image,float)


def smooth_naive(images, styledim, threshold, size, outdir, bsize, outprefix = "frame"):
    # a naive way to find the difference part of connective frames
    # for the different part, keep yhat
    # for similar part, use yhat_{-1}
    imgold = None
    styimgold = None
    for i in range(len(styledim)):
        image = images[i]
        styimage = sty_images[i]
        if not os.path.exists(image):
            raise IOError(image)
        if not os.path.exists(styimage):
            raise IOError(styimage)
        imgnew = load_image(image, size)
        imgnew.flags.writeable = True  
        styimgnew = np.array(Image.open(styimage).convert('RGB'))


        styimgnew.flags.writeable = True  
        imgdim = imgnew.shape
        lenth = imgdim[0]
        width = imgdim[1]
        if i > 0:
            for j in range(imgdim[0]):
                for k in range(imgdim[1]):
                    boxnew = imgnew[max(0,j - bsize):min(j + bsize, lenth),max(0,k-bsize):min(k+bsize, width),:]
                    boxold = imgold[max(0,j - bsize):min(j + bsize, lenth),max(0,k-bsize):min(k+bsize, width),:]
                    sumnew = np.sum(boxnew,axis = (0,1))
                    sumold = np.sum(boxold,axis = (0,1))
                    boxsize = (max(0,j - bsize) - min(j + bsize, lenth))*(max(0,k-bsize) - min(k+bsize, width))
                    diff = sum(abs(sumnew - sumold))/boxsize
                    if diff < threshold:
                        styimgnew[j][k] = styimgold[j][k] 
        im = Image.fromarray(styimgnew)      
        im.save("%s%s%d.jpg" % (outdir, outprefix, i*3))   
        print('%s%d' % ('frame:',i*3))      
        imgold = imgnew
        styimgold = styimgnew
        
            

if __name__ == "__main__":    
     imageDir = "../data/bear/frames/"
     images = [imageDir + imageName for imageName in os.listdir(imageDir) if imageName != '.DS_Store']
     images.sort(key=lambda name: int(re.sub("\D", "", name))) 
   
     sty_imageDir = "../data/bear/stylized_frames/"
     sty_images = [sty_imageDir + imageName for imageName in os.listdir(sty_imageDir) if imageName != '.DS_Store']
     sty_images.sort(key=lambda name: int(re.sub("\D", "", name)))
     
     outDir = "../data/bear/stylized_naive_box_20_3_frames/"
     
     smooth_naive(images, sty_images, 12, 1024, outDir, 3)

