## Usage: sh rawTransferVideo.sh
## Note: need to download fast-neural-style code first:
## git clone git@github.com:lingxuez/fast-neural-style.git


# input_dir="data/frames/"
# output_dir="data/frames_naive_fns/"
# out_video="data/styled_test_raw.mp4"

# ## train frame-by-frame
# cd fast-neural-style
# # th fast_neural_style.lua \
# # 	-model models/eccv16/starry_night.t7 \
# # 	-input_dir ../${input_dir} \
# # 	-output_dir ../${output_dir}

# ## combine to a video
# cd ../src
# python image2video.py ../${output_dir} ../${out_video}