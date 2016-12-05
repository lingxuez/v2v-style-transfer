## Usage: sh multipleStyleTransfer.sh
## Note: need to download neural-style code first:
## git clone git@github.com:lingxuez/neural-style.git

cd neural-style

style_dir="../video2video/trailer/frames_lof"
content="../data/frames/frame0.jpg"
output="../video2video/stylized/frame0_2style.jpg"

## try 1 frame, 2 styles
th neural_style.lua -content_image $content \
	-style_image ${style_dir}/frame-01.jpeg,${style_dir}/frame-02.jpeg \
	-output_image $output \
	-num_iterations 200 -gpu -1 ## cpu mode
