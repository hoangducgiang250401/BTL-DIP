import cv2
import numpy as ny
import xml.etree.ElementTree as ET

def moreThanZero(int1, int2):
    if ((int1 - int2) > 0):
        return int1 - int2
    return int2 - int1

def result(array1,array2):
    
    resultArray = []
    #(0,3) (2,1)
    for solution, answer in zip(array1, array2):
        left_x = max(solution[0], answer[0])
        top_y = min(solution[1], answer[1])
        right_x = min(solution[2], answer[2])
        bottom_y = max(solution[3], answer[3])

        intersectionArea = moreThanZero(left_x, right_x) * moreThanZero(top_y, bottom_y)

        solutionArea = moreThanZero(solution[0], solution[3]) * moreThanZero(solution[1], solution[2])

        answerArea = moreThanZero(answer[0], answer[3]) * moreThanZero(answer[1], answer[2])
        
        resultArray.append(intersectionArea / float(solutionArea + answerArea- intersectionArea))

    return resultArray

def final(a,c):
    # a.sort(key=lambda x: x[1], reverse=False)
    # c.sort(key=lambda x: x[1], reverse=False)
    resultArray = result(a,c)

    resultValue = 0
    
    for ite in resultArray:
        resultValue += ite   

    resultValue /= len(resultArray)

    return resultValue

def processImage(img,morph_size):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 10)
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

def lineSpacing(boxes):
    boxes.sort(key=lambda x: x[1], reverse=False)
    # print(boxes)
    MaxLine = 1000
    for i in range(len(boxes)-1):
        print(MaxLine)
        # print((boxes[i + 1][1] - boxes[i][1]))
        if MaxLine > (boxes[i + 1][1] - boxes[i][1]) > 10:
            MaxLine = (boxes[i + 1][1] - boxes[i][1])
    return MaxLine
        

def getCorrection(thresh,with_ = 3,height_ = 1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (with_, height_))
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    boxes = find_Contours(thresh)
    line_spacing = lineSpacing(boxes)
    chieucaotb = get_htb(boxes)
    return [chieucaotb,line_spacing]

def testDNA(box1,box2,boxes):
    (x, y, w, h) = box1
    (x1, y1, w1, h1) = box2
    if (x+w >= x1) and (x1+w1 >= x) and (y+h >= y1) and (y1+h1 >= y):
        return True
    return False

def getAllOverlaps(boxes,bounds, index):
    overlaps = []
    for i in range(len(boxes)):
            if testDNA(bounds, boxes[i],boxes):
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
    # imgname = "32"
    imgname = "75094"
    # imgname = "34"
    img = cv2.imread("data/public/" + imgname +".png")
    pathXml = 'data/public/' + imgname+'.xml'
    
    thresh = processImage(img,(1,1))
    correction = getCorrection(thresh)
    # lấy thông số text
    height_text = correction[0]
    lineToLine = correction[1]
    letter_spacing = round(height_text*1.5)
    line_spacing =  lineToLine - round(height_text*1.6)
    # xử lý theo thông số lấy được
    thresh2 = processImage(img,(round(height_text/2.5),1))
    boxes = find_Contours(thresh2)
    results = clearBoxes(boxes,letter_spacing,line_spacing)
    # print(boxes)
    for box in results:
        (x, y, w, h) = box
        cv2.rectangle(img, (x, y), (x + w -1, y + h -1), (0, 0, 255), 1)

    resultsXml = readXml(pathXml)
    for x in resultsXml:
        cv2.rectangle(img, (x[0], x[1]), (x[2], x[3]), (36,255,12), 1)
    # for box in results:
    #     print(box[2])
    #     box[2] = box[0] + box[2]
    #     box[3] = box[1] + box[3]
    results = [(box[0], box[1], box[2] + box[0], box[3] + box[1]) for box in results]
    print(final(results,resultsXml))
    cv2.imshow("thresh2",thresh2)
    cv2.imshow("thresh",thresh)
    cv2.imshow("img",img)
    cv2.waitKey()