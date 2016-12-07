# neural-style

Mostly forked from [jcjohnson/neural-style](https://github.com/jcjohnson/neural-style), with an extra functionality of smooth style transitioning from video-frames to video-frames. 

## Setup:

Dependencies:
* [torch7](https://github.com/torch/torch7)
* [loadcaffe](https://github.com/szagoruyko/loadcaffe)

Optional dependencies:
* For CUDA backend:
  * CUDA 6.5+
  * [cunn](https://github.com/torch/cunn)
* For cuDNN backend:
  * [cudnn.torch](https://github.com/soumith/cudnn.torch)
* For OpenCL backend:
  * [cltorch](https://github.com/hughperkins/cltorch)
  * [clnn](https://github.com/hughperkins/clnn)

After installing dependencies, you'll need to run the following script to download the VGG model:
```
sh models/download_models.sh
```
This will download the original [VGG-19 model](https://gist.github.com/ksimonyan/3785162f95cd2d5fee77#file-readme-md).
Leon Gatys has graciously provided the modified version of the VGG-19 model that was used in their paper;
this will also be downloaded. By default the original VGG-19 model is used.

If you have a smaller memory GPU then using NIN Imagenet model will be better and gives slightly worse yet comparable results. You can get the details on the model from [BVLC Caffe ModelZoo](https://github.com/BVLC/caffe/wiki/Model-Zoo) and can download the files from [NIN-Imagenet Download Link](https://drive.google.com/folderview?id=0B0IedYUunOQINEFtUi1QNWVhVVU&usp=drive_web)

You can find detailed installation instructions for Ubuntu in the [installation guide](INSTALL.md).

## Usage
Basic usage:
```
python merge_style_transfer_sw.py <input_dir> <style_dir> <output_dir> <gpu>
```
Note that paths to images should not contain the `~` character to represent your home directory; you should instead use a relative
path or a full absolute path.

**Options**:
* `-input_dir`: Path to the directory containing frames (`.jpg` images) of the source video.
* `-style_dir`: Path to the directory containing multiple `.jpg` style images. These are usually the keyframes of the style video (e.g. a movie trailer).
* `-style_dir`: Path to the output directory, which will contain stylized frames (`.jpg` images).
* `-gpu`: Zero-indexed ID of the GPU to use; for CPU mode set `-gpu` to -1.

**More Options**
Please refer to the [original repository](https://github.com/jcjohnson/neural-style) for more advanced usage and options.

