## Usage: python image2video.py input_dir output_video
## WARNING: the only digits in the filename must be the frame number

from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
import os, sys, exceptions, re

def image2video(images, outvid=None, fps=15, size=None,
               is_color=True, format="mp4v"):
    """
    Create a video from a list of images.
 
    @param      outvid      output video
    @param      images      list of images to use in the video
    @param      fps         frame per second
    @param      size        size of each frame
    @param      is_color    color
    @param      format      see http://www.fourcc.org/codecs.php
    @return                 see http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
 
    The function relies on http://opencv-python-tutroals.readthedocs.org/en/latest/.
    By default, the video will have the size of the first image.
    It will resize every image to this size before adding them to the video.
    """
    fourcc = VideoWriter_fourcc(*format)
    vid = None
    for image in images:
        if not os.path.exists(image):
            raise IOError(image)
        img = imread(image)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = VideoWriter(outvid, fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = resize(img, size)
        vid.write(img)

    vid.release()
    return vid


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: python image2video.py <input_dir> <output_video>"

    imageDir = sys.argv[1]
    output = sys.argv[2]

    ## the only digits in the filename must be the frame number
    images = [imageDir + "/" + imageName for imageName in os.listdir(imageDir) 
                        if imageName != ".DS_Store"]
    # sort image files according to frame number
    images.sort(key=lambda name: int(re.sub("\D", "", name)))

    ## convert to video
    image2video(images, outvid=output)

