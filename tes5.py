import cv2
import numpy as np
import poly_point_isect as bot


img = cv2.imread('./data/public/32.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

kernel_size = 3
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

low_threshold = 50
high_threshold = 150
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 10  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 15  # minimum number of pixels making up a line
max_line_gap = 3  # maximum gap in pixels between connectable line segments
line_image = np.copy(img) * 0  # creating a blank to draw lines on

# Run Hough on edge detected image
# Output "lines" is an array containing endpoints of detected line segments
lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                    min_line_length, max_line_gap)


print(lines)
points = []
for line in lines:
    for x1, y1, x2, y2 in line:
        points.append(((x1 + 0.0, y1 + 0.0), (x2 + 0.0, y2 + 0.0)))
        cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
print(lines_edges.shape)
cv2.imwrite('line_parking.png', lines_edges)

print (points)
intersections = bot.isect_segments(points)
print (intersections)

for idx, inter in enumerate(intersections):
    a, b = inter
    match = 0
    for other_inter in intersections[idx:]:
        if other_inter == inter:
            continue
        c, d = other_inter
        if abs(c-a) < 15 and abs(d-b) < 15:
            match = 1
            intersections[idx] = ((c+a)/2, (d+b)/2)
            intersections.remove(other_inter)

    if match == 0:
        intersections.remove(inter)

for inter in intersections:
    a, b = inter
    for i in range(3):
        for j in range(3):
            lines_edges[int(b) + i, int(a) + j] = [0, 255, 0]



cv2.imwrite('line_parking.png', lines_edges)

cv2.imshow("blur ",blur_gray)
cv2.imshow("edges",edges)
cv2.imshow("line_image",line_image)
cv2.imshow("lines_edges",lines_edges)
cv2.waitKey(0)

# for idx, inter in enumerate(intersections):
#     a, b = inter
#     match = 0
#     for other_inter in intersections[idx:]:
#         if other_inter == inter:
#             continue
#         c, d = other_inter
#         if abs(c-a) < 15 and abs(d-b) < 15:
#             match = 1
#             intersections[idx] = ((c+a)/2, (d+b)/2)
#             intersections.remove(other_inter)

#     if match == 0:
#         intersections.remove(inter)