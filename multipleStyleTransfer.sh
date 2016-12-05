## Usage: sh rawTransferVideo.sh
## Note: need to download neural-style code first:
## git clone git@github.com:lingxuez/neural-style.git

style_dir="../video2video/trailer/frames_lof"

## try 1 frame, 2 styles
cd neural-style
th neural_style.lua -content_image ../data/frames/frame0.jpg \
	-style_image ${style_dir}/frame-01.jpeg,${style_dir}/frame-02.jpeg \
	-gpu -1 ## cpu mode
	