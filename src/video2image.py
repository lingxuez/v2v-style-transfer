import cv2

def video2image(videoFile, outdir, extractGap, outprefix="frame"):

	vidcap = cv2.VideoCapture(videoFile)
	success,image = vidcap.read()
	count = 0
	success = True
	while success:
		success,image = vidcap.read()
		if count % extractGap == 0:
			print 'Read a new frame: ', success
			cv2.imwrite(("%s%s%d.jpg" % (outdir, outprefix, count)), image) 
		count += 1


if __name__ == "__main__":
	video2image(videoFile='../data/test.MOV', outdir="../data/frames/", extractGap=10)
