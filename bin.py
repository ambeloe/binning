import cv2
import numpy as np
import time


def crop_div(factor, img):
    len_y = len(img)
    len_x = len(img[0])

    while len_y % factor != 0:
        len_y -= 1

    while len_x % factor != 0:
        len_x -= 1

    return img[:len_y, :len_x]


def remap_img(img, iS, iE, oS, oE):
    res = np.zeros((len(img), len(img[0]), 3), np.uint8)
    for y in range(0, len(img)):
        for x in range(0, len(img[0])):
            for c in range(0, len(img[0][0])):
                res[y][x][c] = int(oS + (oE - oS) * ((img[y][x][c] - iS) / (iE - iS)))
    return res

def clip_img(img, min, max):
    res = np.zeros((len(img), len(img[0]), 3), np.uint8)
    for y in range(0, len(img)):
        for x in range(0, len(img[0])):
            for c in range(0, len(img[0][0])):
                if c > max:
                    res[y][x][c] = max
                elif c < min:
                    res[y][x][c] = min
                else:
                    res[y][x][c] = img[y][x][c]
    return res

def add_pix(img):
    bgr = [0, 0, 0]
    for y in range(0, len(img)):
        for x in range(0, len(img[0])):
            bgr += img[y][x]
    return bgr

def bad_binning(factor, img):
    res = np.zeros((int(len(img) / factor), int(len(img[0]) / factor), 3), np.uint16)
    for y in range(0, len(res)):
        for x in range(0, len(res[0])):
            region = img[(factor * y):(factor * y) + factor, (factor * x):(factor * x) + factor]
            res[y][x] = add_pix(region)
            cv2.imwrite("regions/" + str(x) + "X" + str(y) + ".bmp", region)
    return res


factor = 100

image = cv2.imread("img.png")
image = crop_div(factor, image)
print(str(len(image[0])) + "x" + str(len(image)))
cv2.imwrite("resized.png", image)
binned = bad_binning(factor, image)
# binned = remap_img(binned, 0, (256 * (factor * factor)) - 1, 0, 255)
# binned = clip_img(binned, 0, 255)
# binned = cv2.convertScaleAbs(binned)
# binned = cv2.normalize(binned, 127, 255)
cv2.imwrite("binned.png", binned)

dark_image = cv2.imread("dark.png")
dark_image = crop_div(factor, dark_image)
print(str(len(dark_image[0])) + "x" + str(len(dark_image)))
cv2.imwrite("resized_dark.png", dark_image)
dark_binned = bad_binning(factor, dark_image)
cv2.imwrite("dark_binned.png", dark_binned)

final = binned - dark_binned
cv2.imwrite("final.png", final)
