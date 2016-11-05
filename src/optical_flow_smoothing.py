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


def naive_smooth(frames):
    """

    :param frames: a list strings. each is a frame path
    :return: none
    """

    # read the first frame
    prev = cv2.imread(frames[0])
    prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    for i in range(1, len(frames)):
        # the next image
        new = cv2.imread(frames[i])
        newgray = cv2.cvtColor(new, cv2.COLOR_BGR2GRAY)

        # forward flow
        flow = cv2.calcOpticalFlowFarneback(prevgray, newgray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        v = flow[..., 0]

        #v = np.power(fx, 2) + np.power(fy, 2)
        v = cv2.normalize(v, None, 0, 255, cv2.NORM_MINMAX)
        print np.max(v), np.mean(v)
        cv2.imwrite('test_flow_{0}.png'.format(i), v)

        #print flow[0][0][0], flow[0][0][1]
        #cv2.imshow('Optical flow', draw_flow(newgray, flow))
        #ch = 0xFF & cv2.waitKey(5)
        #if ch == 27:
        #    break
        if i > 20:
            break

    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--org_frame_dir", default="../data/frames/")
    parser.add_argument("--styled_frame_dir", default="../data/styled_frames/")
    args = parser.parse_args()

    # original frame file paths
    frames = [args.org_frame_dir + '/' + imageName for imageName in os.listdir(args.org_frame_dir)]

    # sort frame files according to frame number
    frames.sort(key=lambda name: int(re.sub("\D", "", name)))

    naive_smooth(frames)


if __name__ == '__main__':
    main()

