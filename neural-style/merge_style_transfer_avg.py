## Video2video style transfer using merged styles with sliding window
##
## Input: multiple keyframes from style video (e.g., movie trailer)
## Output: stylized frames for target video
##       Each frame is stylized using blended multiple style keyframes;
##       The keyframes are selected such that the style-transitioning
##       is temporarilly consistent between target and style video.

import sys, os, re
from subprocess import call


def style_transfer_avg(input_frames, style_frames, 
                input_dir, style_dir, output_dir, niter=1000, gpu=0):
    """
    matched: a dictionary: key=input_frames, 
        value=(list of style frames to use for it, weights for diff styles)
    input_dir: directory for input frames
    style_dir: directory for style frames
    output_dir: directory for output stylized frames
    """

    for input_frame in input_frames:
        style_frames = map(lambda file: style_dir+"/"+file, style_frames)
        print "Style transfer for", input_dir+"/"+input_frame, \
                "from styles", ",".join(style_frames)

        call(" ".join(["th neural_style.lua", 
            "-content_image", input_dir+"/"+input_frame, 
            "-init image",
            "-style_image", ",".join(style_frames),
            "-output_image", output_dir+"/avg-stylized-"+input_frame,
            "-num_iterations", str(niter),
            "-save_iter", str(0), 
            "-gpu", str(gpu)]), shell=True)


def images_in_dir(input_dir, ext="jpg"):
    """
    List all names of the images under a directory;
    images are ordered according to frame number.
    Note: the only digits in the filename must be the frame number
    """
    images = [file for file in os.listdir(input_dir) if ext in file]
    ## sort image files according to frame number (the only digits)
    images.sort(key=lambda file: int(re.sub("\D", "", file)))
    return images


if __name__ == "__main__":
    ## Note: the only digits in the filename must be the frame number
    if len(sys.argv) != 5:
        print """
Usage: python merge_style_transfer_sw.py <input_dir> <style_dir> <output_dir> <gpu> 
       	"""

    input_dir = sys.argv[1]
    style_dir = sys.argv[2]
    output_dir = sys.argv[3]
    gpu = sys.argv[4] 

    niter = 1000

    input_frames = images_in_dir(input_dir)
    style_frames = images_in_dir(style_dir)

    ## style transfer
    style_transfer_avg(input_frames, style_frames, input_dir, style_dir, output_dir, niter, gpu)



