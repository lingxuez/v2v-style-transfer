import numpy as np
import cv2
import argparse
import os
import re


def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis


def naive_smooth(frames, styled_frames):
    """

    :param frames: a list strings. each is a frame path
    :return: none
    """

    # read the first frame
    prevgray = cv2.imread(frames[0], 0)
    prevstyled = cv2.imread(styled_frames[0])

    for i in range(1, len(frames)):
        # the next image
        gray = cv2.imread(frames[i], 0)
        styled = cv2.imread(styled_frames[i])

        # forward flow
        flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 4, 3, 7, 1.5, 0)
        v, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        neg_indexes = np.asarray(v) < 0.1
        #print len(neg_indexes)
        newstyled = 1 * styled + 0.0 * prevstyled
        newstyled[neg_indexes] = 0.0 * styled[neg_indexes] + 1 * prevstyled[neg_indexes]

        cv2.imwrite("optic_{0}.png".format(i), newstyled)
        prevgray = gray
        prevstyled = newstyled

        #v[neg_indexes] = 0

        #v = np.power(fx, 2) + np.power(fy, 2)
        #v = cv2.normalize(v, None, 0, 255, cv2.NORM_MINMAX)
        #print np.max(v), np.mean(v)
        #cv2.imwrite('test_flow_{0}.png'.format(i), v)

    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--org_frame_dir", default="../data/frames/")
    parser.add_argument("--styled_frame_dir", default="../data/frames_styled/")
    args = parser.parse_args()

    # original frame file paths
    frames = [args.org_frame_dir + '/' + imageName for imageName in os.listdir(args.org_frame_dir)
              if imageName != ".DS_Store"]

    styled_frames = [args.styled_frame_dir + '/' + imageName for imageName in os.listdir(args.styled_frame_dir)
                     if imageName != ".DS_Store"]

    # sort frame files according to frame number
    frames.sort(key=lambda name: int(re.sub("\D", "", name)))
    styled_frames.sort(key=lambda name: int(re.sub("\D", "", name)))

    naive_smooth(frames, styled_frames)


if __name__ == '__main__':
    main()

