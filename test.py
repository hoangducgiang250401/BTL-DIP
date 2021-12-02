import cv2
import numpy as ny
import xml.etree.ElementTree as ET

def pre_process_image(img,morph_size):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, morph_size)
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    return thresh

def find_Contours(thresh):
    min_text_height_limit=1
    max_text_height_limit=20

    min_text_width_limit=1
    max_text_width_limit=500

    min_text_area_limit=50
    max_text_area_limit=2000

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for contour in contours:
        box = cv2.boundingRect(contour)
        h = box[3]
        w = box[2]
        area = cv2.contourArea(contour)
        if min_text_height_limit < h < max_text_height_limit and min_text_width_limit < w < max_text_width_limit and min_text_area_limit < area < max_text_area_limit:
            boxes.append(box)
    return boxes

def get_htb(boxes):
    sum_height = 0
    lenboxes = len(boxes)
    for box in boxes:
        sum_height = sum_height + box[3]
    return sum_height/lenboxes

def height_text(thresh,with_ = 3,height_ = 1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (with_, height_))
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    boxes = find_Contours(thresh)
    chieucaotb = get_htb(boxes)
    return chieucaotb

def testDNA(box1,box2,r):
    (x, y, w, h) = box1
    (x1, y1, w1, h1) = box2
    if (x+w >= x1) and (x1+w1 >= x) and (y+h >= y1) and (y1+h1 >= y):
        return True
    if abs(x1 - (x + w)) < r or abs(x - (x1 + w1)) < r:
        return True
    return False

def max(a,b):
    if a > b:
        return a
    return b

def min(a,b):
    if a < b:
        return a
    return b

def makeFriend(box1,box2):
    (x, y, w, h) = box1
    (x1, y1, w1, h1) = box2
    x0 = min(x,x1)
    y0 = min(y,y1)
    w0 = max(x + w,x1 + w1) - min(x,x1)
    h0 = max(y + h,y1 + h1) - min(y,y1)
    newBox = (x0,y0,w0,h0)
    # print("new box ",newBox)
    return newBox

def clearBoxes(boxes,r):
    for i in range(len(boxes)-1):
        if i == (len(boxes)-1):
            return boxes
        if testDNA(boxes[i],boxes[i + 1],r):
            newBox = makeFriend(boxes[i],boxes[i + 1])
            boxes[i] = newBox
            boxes.remove(boxes[i + 1])
            # i = i -1
    return boxes

def readXml(pathXml):
    tree = ET.parse(pathXml)
    root = tree.getroot()
    a = []
    for child in root:
        b = []
        if child.tag == 'object':
            for con in child:
                if con.tag == 'bndbox':
                    for con2 in con:
                        b.append(con2.text)
            a.append(b)
    a = ny.array(a, dtype=ny.int32)
    return a

if "BTL-DIP" == "BTL-DIP":
    imgname = "49436"
    img = cv2.imread("data/public/" + imgname +".png")
    thresh = pre_process_image(img,(4,1))
    height_text = height_text(thresh)
    thresh2 = pre_process_image(img,(round(height_text/2) + 1 ,1))
    boxes = find_Contours(thresh)
    arr = boxes
    results = clearBoxes(arr,height_text)
    print(results)

    for box in results:
        (x, y, w, h) = box
        cv2.rectangle(img, (x, y), (x + w -1 , y + h -1), (0, 0, 255), 1)

    pathXml = 'data/public/' + imgname+'.xml'
    a = readXml(pathXml)

    # for x in a:
    #     cv2.rectangle(img, (x[0], x[1]), (x[2], x[3]), (36,255,12), 1)

    cv2.imshow("thresh2",thresh2)
    cv2.imshow("thresh",thresh)
    cv2.imshow("img",img)
    cv2.waitKey()