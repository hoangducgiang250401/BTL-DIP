import cv2
import numpy as ny
import array as arr
import xml.etree.ElementTree as ET
 


a  = [(1,2,3),(4,5,6),(7,8,9)]

b = a[1]
c = a[2]
a.remove(b,c)

print(a)
# tree = ET.parse('data/public/32.xml')

# root = tree.getroot()

# a = []
# print(root.tag)
 
# for child in root:
#     b = []
#     if child.tag == 'object':
#         for con in child:
#             if con.tag == 'bndbox':
#                 for con2 in con:
#                     b.append(con2.text)
#         a.append(b)

# a = ny.array(a, dtype=ny.int32)

# print(a)
# image = cv2.imread('data/pubic/32.png')
# for x in a:
#     cv2.rectangle(image, (x[0], x[1]), (x[2], x[3]), (36,255,12), 2)
    
# cv2.imshow('image', image)
# cv2.waitKey()





