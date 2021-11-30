import cv2
import numpy as ny
import array as arr
import xml.etree.ElementTree as ET
 

tree = ET.parse('data/32.xml')

root = tree.getroot()

a = []
print(root.tag)
 
for child in root:
    b = []
    if child.tag == 'object':
        for con in child:
            if con.tag == 'bndbox':
                for con2 in con:
                    b.append(con2.text)
        a.append(b)


print(a)








a = ny.array(a, dtype=ny.int32)
image = cv2.imread('data/32.png')
for x in a:
    cv2.rectangle(image, (x[0], x[1]), (x[2], x[3]), (36,255,12), 2)
    
cv2.imshow('image', image)
cv2.waitKey()





