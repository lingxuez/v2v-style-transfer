

cd neural-style

input_dir="../data/pig/frames"
style_dir="../5m"
output_dir="../data/pig/5m_frames"
gpu=0

mkdir -p $output_dir

python merge_style_transfer_sw.py $input_dir $style_dir $output_dir $gpu

