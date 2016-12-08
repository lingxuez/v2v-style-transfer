import numpy as np
import os, re
import argparse
from PIL import Image

def load_image(path, size=None):
    """
    If size is None: no re-sizing is performed.
    Otherwise it is a tuple (h, w), 
    and the output is forced to be the same width and height.
    """

    #coppied from Github, Feifei's method
    #size and crop are not used for now
    image = Image.open(path).convert('RGB')
    
    ## re-sizing
    if size is not None:
        image = image.resize((size[1], size[0]), Image.ANTIALIAS)

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

        ## style image 
        styimgnew = load_image(styimage)
        styimgnew.flags.writeable = True 

        ## source image
        ## down-size if style image is compressed
        imgnew = load_image(image, size=styimgnew.shape[:2])
        imgnew.flags.writeable = True 

        if i > 0:
            diff = abs(imgnew - imgold)
            diff = np.sum(diff,axis = 2)           
            styimgnew[diff < threshold] = styimgold[diff < threshold] 
        im = Image.fromarray(styimgnew)      
        im.save("%s/%s%d.jpg" % (outdir, outprefix, i))          
        imgold = imgnew
        styimgold = styimgnew
        
            

if __name__ == "__main__":  
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--org_frame_dir", default="../data/pig/frames/")
    parser.add_argument("-s", "--styled_frame_dir", default="../data/pig/frames_styled/")
    parser.add_argument("-o", "--output_dir", default="../data/pig/")
    args = parser.parse_args()

    images = [args.org_frame_dir + "/" + imageName 
            for imageName in os.listdir(args.org_frame_dir) if imageName != '.DS_Store']
    images.sort(key=lambda name: int(re.sub("\D", "", name))) 

    sty_images = [args.styled_frame_dir + "/" + imageName 
            for imageName in os.listdir(args.styled_frame_dir) if imageName != '.DS_Store']
    sty_images.sort(key=lambda name: int(re.sub("\D", "", name)))

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    smooth_naive(images, sty_images, 100, 1024, args.output_dir)

