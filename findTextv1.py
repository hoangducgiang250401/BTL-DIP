import cv2
import numpy as ny
import array as arr


def xu_ly_mo_rong(img,shape,withKernel,heightKernel):
    (height, width, depth) = img.shape
    if shape[1] != heightKernel:
        shape[0] = shape[0] + heightKernel//2
        shape[1] = shape[1] + heightKernel//2
        shape[2] = shape[2] - heightKernel//2
        shape[3] = shape[3] - heightKernel//2
    return shape

def detectTheLargestArea(thresh,withKernel,heightKernel):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (withKernel,heightKernel))
    dilate = cv2.dilate(thresh, kernel, iterations=1)
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    maxArea = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if area > maxArea:
            maxArea = area
            a = [x,y,w,h] = cv2.boundingRect(c)
    print(a)
    cv2.imshow('dilate', dilate)
    cv2.waitKey()
    return a

def findText(cell):
    # Load image, grayscale, Gaussian blur, adaptive threshold
    image = cv2.imread(cell)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)
    # Dilate to combine adjacent text contours
    withKernel = 2
    heightKernel = 2
    heightKernel = withKernel = detectTheLargestArea(thresh,withKernel,heightKernel)[3]
    a = [x,y,w,h] = detectTheLargestArea(thresh,withKernel,heightKernel)
    # a = xu_ly_mo_rong(image,a,withKernel,heightKernel)
    denta = heightKernel//2
    cv2.rectangle(image, (x + denta , y + denta), (x + w - denta, y + h - denta), (36,255,12), 2)
    cv2.imshow('thresh', thresh)
    cv2.imshow('image', image)
    cv2.imshow('thresh', thresh)
    # cv2.imshow('dilate', dilate)
    cv2.imshow('image', image)
    cv2.waitKey()
    return a

def cropImg(img, parameter):
    x = parameter[0]
    y = parameter[1]
    w = parameter[2]
    h = parameter[3]
    roi = img[x:y , (x + w):(y + h)]
    return roi



print(findText('test.png'))
