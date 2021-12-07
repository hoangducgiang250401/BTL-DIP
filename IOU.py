import cv2
import numpy as ny
import array as arr
import xml.etree.ElementTree as ET
#import findText.py as textHandler
#import itertools as IT

tree = ET.parse('data/public/32.xml')

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

#b = textHandler.findText(cell)

ex = ET.parse('data/public/61803.xml')

ex_root = ex.getroot()

c = []
for one in ex_root:
    d = []
    if one.tag == 'object':
        for low in one:
            if low.tag == 'bndbox':
                for add in low:
                    d.append(add.text)
        c.append(d)

a = ny.array(a, dtype=ny.int32)
c = ny.array(c, dtype=ny.int32)



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

resultArray = result(a,c)

resultValue = 0
print(resultArray)
for ite in resultArray:
    resultValue += ite   

resultValue /= len(resultArray)

print(resultValue)
