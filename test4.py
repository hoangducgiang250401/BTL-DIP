import cv2
import numpy as ny
import xml.etree.ElementTree as ET



def processImage(img,morph_size):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, morph_size)
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    return thresh

def find_Contours(thresh):
    min_text_height_limit=3
    max_text_height_limit=18

    min_text_width_limit=3
    max_text_width_limit=500

    min_text_area_limit=1
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

# def lineSpacing(boxes):
#     boxes.sort(key=lambda x: x[1], reverse=False)
#     MaxLine = 0
#     for i in range(len(boxes)-1):
        



def height_text(thresh,with_ = 3,height_ = 1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (with_, height_))
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    boxes = find_Contours(thresh)
    print(boxes)
    # line_spacing = lineSpacing(boxes)
    chieucaotb = get_htb(boxes)
    return chieucaotb

def testDNA(box1,box2):
    (x, y, w, h) = box1
    (x1, y1, w1, h1) = box2
    if (x+w >= x1) and (x1+w1 >= x) and (y+h >= y1) and (y1+h1 >= y):
        return True
    return False

def getAllOverlaps(boxes,bounds, index):
    overlaps = []
    for i in range(len(boxes)):
            if testDNA(bounds, boxes[i]):
                overlaps.append(boxes[i])
    return overlaps


def clearBoxes(boxes,r,d):
    finished = False
    while not finished:
        finished = True

        index = len(boxes)-1 ## lấy độ dài vong lặp
        while index >=0:
            # print(len(boxes))
            # print(index)
            # print("befor:",boxes[index])
            (x, y, w, h) = boxes[index]
            x -= r
            y -= d
            w += 2*r
            h += 2*d
            # print("after : ",boxes[index])
            overlaps = getAllOverlaps(boxes,(x, y, w, h),index)
            # print("box overlaps: ",overlaps)
            con = []
            for box in overlaps:
                (x1,y1,w1,h1) = box
                # print("box",box)
                tl = [x1,y1]
                br = [x1 + w1, y1 + h1]
                # print(tl,br)
                con.append(tl)
                con.append(br)
            con = ny.array(con)
            (x2,y2,w2,h2) = cv2.boundingRect(con)
            # print("box merged: ",cv2.boundingRect(con))
            for ind in overlaps:
                    if ind in boxes:
                        boxes.remove(ind)
            boxes.append((x2,y2,w2-1,h2-1))
            if len(overlaps) > 1:
                finished = False;
                break
            # print(overlaps)
            index -= 1

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
    imgname = "34"
    img = cv2.imread("data/public/" + imgname +".png")
    thresh = processImage(img,(1,1))
    height_text = height_text(thresh)
    letter_spacing = round(height_text*0.7)
    line_spacing =  round(height_text*0.6)
    thresh2 = processImage(img,(round(height_text/2.5),1))
    boxes = find_Contours(thresh2)
    results = clearBoxes(boxes,letter_spacing,line_spacing)
    # print(boxes)
    for box in results:
        (x, y, w, h) = box
        cv2.rectangle(img, (x, y), (x + w -1, y + h -1), (0, 0, 255), 1)

    # pathXml = 'data/public/' + imgname+'.xml'
    # a = readXml(pathXml)
    # for x in a:
    #     cv2.rectangle(img, (x[0], x[1]), (x[2], x[3]), (36,255,12), 1)

    cv2.imshow("thresh2",thresh2)
    cv2.imshow("thresh",thresh)
    cv2.imshow("img",img)
    cv2.waitKey()