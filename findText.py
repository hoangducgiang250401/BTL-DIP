import cv2
import numpy as ny
import array as arr


def xu_ly_mo_rong(img,shape,withKernel,heightKernel):
    (height, width, depth) = img.shape
    print("width={}, height={}, depth={}".format(width, height, depth))
    # if shape[1] =
    
    return shape

def findheight(thresh,withKernel,heightKernel):
    withKernel = 9
    heightKernel = 21
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (withKernel,heightKernel))
    dilate = cv2.dilate(thresh, kernel, iterations=1)
    # Find contours, highlight text areas
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    maxArea = 0
    x = y = w = h = 0
    denta = 0
    for c in cnts:
        area = cv2.contourArea(c)
        # print(area)
        if area > maxArea:
            maxArea = area
            a = [] = cv2.boundingRect(c)
    # cv2.imshow('thresh', thresh)
    # cv2.imshow('dilate', dilate)
    # cv2.waitKey()
    return a

def findText(cell):
    # Load image, grayscale, Gaussian blur, adaptive threshold
    image = cv2.imread(cell)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)
    # Dilate to combine adjacent text contours
    withKernel = 15
    heightKernel = 1
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (withKernel,heightKernel))
    dilate = cv2.dilate(thresh, kernel, iterations=1)
    # Find contours, highlight text areas
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    maxArea = 0
    x = y = w = h = 0
    denta = heightKernel//2
    for c in cnts:
        area = cv2.contourArea(c)
        # print(area)
        if area > 1000:
            # maxArea = area
            a = [x,y,w,h] = cv2.boundingRect(c)
            cv2.rectangle(image, (x + denta, y + denta), (x + w - denta, y + h - denta), (36,255,12), 3)
    # a = xu_ly_mo_rong(image,a)
    
    print("giá trị lớn nhấT : ",maxArea)
    cv2.imshow('thresh', thresh)
    cv2.imshow('dilate', dilate)
    cv2.imshow('image', image)
    cv2.imshow('gray', gray)
    cv2.imshow('blur', blur)
    cv2.waitKey()
    return a


# findText('test3.png')
print(findText('data/33.png'))
