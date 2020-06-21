import numpy as np
import imageio
import cv2


def crop_div(factor, img):
    len_y = len(img)
    len_x = len(img[0])
    while len_y % factor != 0:
        len_y -= 1
    while len_x % factor != 0:
        len_x -= 1
    return img[:len_y, :len_x]


def normalize(max, img):
    bimg = cv2.blur(img, (3, 3))
    fac = max/np.max(img)
    img = np.multiply(img, fac)
    img = np.clip(img, a_min=0, a_max=max)
    return img


def binn(factor, img, bright):
    channels = cv2.split(crop_div(factor, img))
    for c in range(0, len(channels)):
        temp = np.zeros((int(len(channels[c])/factor), int(len(channels[c][0])/factor)), dtype=np.float32)
        for y in range(0, factor):
            for x in range(0, factor):
                temp += channels[c][y::factor, x::factor]
                pass
        # channels[c] = np.around(normalize(255, np.multiply(temp, bright))).astype(np.uint8)
        temp = np.divide(temp, (factor**2)*255)
        if bright != 1:
            channels[c] = np.multiply(temp, bright)
    return cv2.merge((channels[2], channels[1], channels[0]))


image = imageio.imread("img.png")

img = binn(4, image, 10)
cv2.imshow("pog", img)
cv2.waitKey(0)
