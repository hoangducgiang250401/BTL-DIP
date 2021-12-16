import cv2
import numpy as ny
import xml.etree.ElementTree as ET

import os


def processImage(img,morph_size):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 10)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, morph_size)
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    return thresh

def find_Contours(thresh):
    min_text_height_limit=3
    max_text_height_limit=18

    min_text_width_limit=5
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

def lineSpacing(boxes):
    boxes.sort(key=lambda x: x[1], reverse=False)
    MaxLine = 0
    a = 0
    for i in range(len(boxes)-1):
        if MaxLine < (boxes[i + 1][1] - boxes[i][1]) and (boxes[i + 1][1] - boxes[i][1]) > 10:
            MaxLine = MaxLine + (boxes[i + 1][1] - boxes[i][1])
            a += 1
    if a == 0:
        return 10
    MaxLine /= a
    return MaxLine
        

def getCorrection(thresh,with_ = 3,height_ = 1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (with_, height_))
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    boxes = find_Contours(thresh)
    line_spacing = lineSpacing(boxes)
    averageHeight = get_htb(boxes)
    return [averageHeight,line_spacing]

def testDNA(box1,box2):
    (x, y, w, h) = box1
    (x1, y1, w1, h1) = box2
    if (x+w >= x1) and (x1+w1 >= x) and (y+h >= y1) and (y1+h1 >= y):
        return True
    return False

def iou(results,resultsXml):
    lenArrXml = len(resultsXml)
    lenArrRs = len(results)
    lenArrMax = max(lenArrRs,lenArrXml)
    sum = 0
    boxTrue = 0
    for i in range(lenArrRs):
        accuracy = 0
        for j in range(lenArrXml):
            if testDNA(results[i],resultsXml[j]):
                (x, y, x1, y1) = resultsXml[j]
                (x2, y2, x3, y3) = results[i]
                areaXml = (x1 - x)*(y1 - y)
                areaRs = (x3 - x2)*(y3 - y2)
                w = min(x1,x3) - max(x,x2)
                h = min(y1,y3) - max(y,y2)
                areaOverlap = w*h
                if accuracy < areaOverlap/(areaXml + areaRs - areaOverlap) <=1:#
                    accuracy = areaOverlap/(areaXml + areaRs - areaOverlap)
        print("độ chính xác của box ",i," là :",accuracy)
        if 0.5 < accuracy <= 1:
            boxTrue += 1
    # print("tổng số box là : ",lenArrRs)
    return boxTrue/lenArrXml
    # return sum/lenArrXml

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

        index = len(boxes)-1
        while index >=0:
            (x, y, w, h) = boxes[index]
            x -= r
            y -= d
            w += 2*r
            h += 2*d
            overlaps = getAllOverlaps(boxes,(x, y, w, h),index)
            con = []
            for box in overlaps:
                (x1,y1,w1,h1) = box
                tl = [x1,y1]
                br = [x1 + w1, y1 + h1]
                con.append(tl)
                con.append(br)
            con = ny.array(con)
            (x2,y2,w2,h2) = cv2.boundingRect(con)
            for ind in overlaps:
                    if ind in boxes:
                        boxes.remove(ind)
            boxes.append((x2,y2,w2-1,h2-1))
            if len(overlaps) > 1:
                finished = False;
                break
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
    folderName = "train"
    sumIou = 0
    i = 0
    for filename in os.listdir(("data/" + folderName)): ##truyen vao duong dan chua thu muc
        
        imgname,extension = os.path.splitext(filename)
        
        if extension == ".xml":
            continue
        i += 1
        img = cv2.imread("data/" + folderName + "/" + imgname +".png")

        thresh = processImage(img,(1,1))
        correction = getCorrection(thresh)
        height_text = correction[0]
        lineToLine = correction[1]
        letter_spacing = round(height_text*0.75)
        line_spacing =  lineToLine - round(height_text*1.55)
        thresh2 = processImage(img,(round(height_text/2.3),1))
        boxes = find_Contours(thresh2)
        results = clearBoxes(boxes,letter_spacing,line_spacing)
        for box in results:
            (x, y, w, h) = box
            cv2.rectangle(img, (x, y), (x + w -1, y + h -1), (0, 0, 255), 1)
        #### BEGIN : SHOW XML
        pathXml = 'data/' + folderName + '/' + imgname +'.xml'
        resultsXml = readXml(pathXml)
        for x in resultsXml:
            cv2.rectangle(img, (x[0], x[1]), (x[2], x[3]), (36,255,12), 1)
        results = [(box[0], box[1], box[2] + box[0], box[3] + box[1]) for box in results]
        results.sort(key=lambda x: x[0], reverse=True)
        results.sort(key=lambda x: x[1], reverse=True)
        rs = []
        for r in resultsXml:
            (a,b,c,d) = r
            rs.append((a,b,c,d))
        rs.sort(key=lambda x: x[0], reverse=True)
        rs.sort(key=lambda x: x[1], reverse=True)
        a = iou(results,rs)
        sumIou += a
        print("IOU " + imgname + ": " , a)
        #### END : SHOW XML
        # cv2.imshow("thresh2",thresh2)
        # cv2.imshow("thresh",thresh)
        cv2.imwrite("data/output/" + imgname + ".png", img)
        cv2.imshow(imgname,img)
        cv2.waitKey()
        # cv2.destroyAllWindows()
    print("Rank : " , (sumIou/i))