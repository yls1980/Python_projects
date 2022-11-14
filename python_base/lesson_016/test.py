import cv2
import numpy as np
import os
from PIL import Image

import sys

print(sys.executable)

def draw_gradient_alpha_rectangle(frame, BGR_Channel, rectangle_position, rotate):
    (xMin, yMin), (xMax, yMax) = rectangle_position
    color = np.array(BGR_Channel, np.uint8)[np.newaxis, :]

    mask1 = np.rot90(np.repeat(np.tile(np.linspace(1, 0, (rectangle_position[1][1]-rectangle_position[0][1])), ((rectangle_position[1][0]-rectangle_position[0][0]), 1))[:, :, np.newaxis], 3, axis=2), rotate)
    frame[yMin:yMax, xMin:xMax, :] = mask1 * frame[yMin:yMax, xMin:xMax, :] + (1-mask1) * color

    return frame

def main():
    #frame = np.zeros((300, 300, 3), np.uint8)
    #frame[:,:,:] = 255

    #frame = draw_gradient_alpha_rectangle(frame, (17, 239, 239), ((0, 0), (200, 200)), 2)
    #frame = draw_gradient_alpha_rectangle(frame, (239, 47, 17), ((0, 0), (200, 200)), 2)
    #frame = draw_gradient_alpha_rectangle(frame, (239, 150,17 ), ((0, 0), (200, 200)), 2)
    #frame = draw_gradient_alpha_rectangle(frame, (160, 164, 155), ((0, 0), (300, 300)), 2)

    spath = os.path.abspath(os.getcwd()) + os.sep + 'python_snippets' + os.sep + 'external_data' + os.sep
    im2 = Image.open(spath + 'weather_img/rain.jpg')
    im1 = Image.open(spath + 'probe.jpg')
    width2, height2 = im2.size
    width1, height1 = im1.size
    im1.paste(im2,(round((width1-width2)/2), height1-height2))
    im1.save(spath+'test.jpg', quality=95)
    #print (paste.shape)
    #print(frame.shape)
    #vis = np.concatenate((frame, paste), axis=0)
    #dst = cv2.addWeighted(frame, 0.5, paste, 0.5, 0.0)
    #dst = cv2.addWeighted(frame, 0.5, paste, 0.5, 0.0)
    #width = frame.shape[1]
    #height = frame.shape[0]  # keep original height
    #dim = (width, height)
    # resize image
    #resized = cv2.resize(paste, dim, interpolation=cv2.INTER_LINEAR)
    #img4 = cv2.addWeighted(frame[0:paste.shape[0], 0:paste.shape[1]], 0.8, paste, 0.2, 0)
    #img4 = cv2.addWeighted(frame, 0.5, resized, 0.5, 0.0)
    #m_v = cv2.vconcat([frame, paste])

    #cv2.imshow('frame', im_v)
    #cv2.waitKey(0)

if __name__ == '__main__':
    print(len(' Погода на 2022-02-10 '))