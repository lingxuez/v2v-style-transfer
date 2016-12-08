import cv2, argparse

def video2image(videoFile, outdir, extractGap, maxSize=512, outprefix="frame"):

	vidcap = cv2.VideoCapture(videoFile)
	success,image = vidcap.read()
	count = 0
	success = True
	while success:
		success,image = vidcap.read()
		if count % extractGap == 0 and image:
			print 'Read a new frame: ', success

			## re-size if too large
			size = image.shape[1], image.shape[0]
			ratio = min(1, float(maxSize)/size[0], float(maxSize)/size[1])
			image = cv2.resize(image, (int(size[0]*ratio), int(size[1]*ratio)))
			cv2.imwrite(("%s%s%d.jpg" % (outdir, outprefix, count)), image) 
		count += 1


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input_video", default="../data/pig/pig.MOV")
	parser.add_argument("-o", "--output_dir", default="../data/pig/frames")
	parser.add_argument("-g", "--gap", default=3)
	parser.add_argument("-s", "--max_size", default=512)
	args = parser.parse_args()

	video2image(videoFile=args.input_video, outdir=args.output_dir, 
			extractGap=args.gap, maxSize=args.max_size)
