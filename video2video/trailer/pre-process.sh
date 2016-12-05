############
## Download trailer
############
## Installation: 
## $ brew install youtube-dl

# youtube-dl -o life_of_pi.mp4 "https://www.youtube.com/watch?v=9BzowSv5CrU"


##################
## Cut and merge on
## http://online-video-cutter.com/
## http://www.aconvert.com/video/merge/
###################


#############
## Extract key frames
#############
## Installation:
## $ brew install ffmpeg

ffmpeg -i life_of_pi_merge_cut.mp4 -vf select='eq(pict_type\,I)' \
	 -vsync 2 -f image2 frames_lof/frame-%02d.jpeg
