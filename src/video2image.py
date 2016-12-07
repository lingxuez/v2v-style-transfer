import cv2

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
	video2image(videoFile='../data/pig/pig.MOV', 
		outdir="../data/pig/frames/", 
		extractGap=1, maxSize=512)
