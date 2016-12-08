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

video="bigfish/bigfish.mp4"
outdir="bigfish/frames_bigfish" ## output folder
digits="%03d" ## pad zeros before frame numbers to make it 3 digits
prefix="frame" ## prefix for extracted frames

## extract key frames
ffmpeg -i $video -vf select='eq(pict_type\,I)' \
	 -vsync 2 -f image2 ${outdir}/${prefix}${digits}.jpg

## original indices of key frames
ffprobe -select_streams v -show_frames -show_entries frame=pict_type \
	-of csv $video \
	| grep -n "frame,I" | cut -d ":" -f 1 > ${outdir}/index.txt 

## re-name key frames using their original indices
cd $outdir
ls -1 *.jpg > list.txt

paste list.txt index.txt | \
while read -r old_name index
do
	newIndex=$(printf ${digits} $(echo $index - 1 | bc))
	mv ${old_name} ${prefix}${newIndex}.jpg
done 

## remove temporary files
rm *.txt