import os
import cv2
import imutils

# This only works if there's only one table on a page
# Important parameters:
#  - morph_size
#  - min_text_height_limit
#  - max_text_height_limit
#  - cell_threshold
#  -arrin_columns


def pre_process_image(img, save_in_file, morph_size=(3, 1)):

    # # get rid of the color
    # pre = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # # Otsu threshold
    # pre = cv2.threshold(pre, 2, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # # dilate the text to make it solid spot
    # cpy = pre.copy()
    # struct = cv2.getStructuringElement(cv2.MORPH_RECT, morph_size)
    # cpy = cv2.dilate(~cpy, struct, anchor=(-1, -1), iterations=1)
    # pre = ~cpy

    # if save_in_file is not None:
    #     cv2.imwrite(save_in_file, pre)
    # return pre
    ############    NEW
    # image = cv2.imread(cell)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, morph_size)
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    if save_in_file is not None:
        cv2.imwrite(save_in_file, thresh)
    return thresh


def find_text_boxes(pre, min_text_height_limit=3, max_text_height_limit=20):
    # Looking for the text spots contours
    # OpenCV 3
    # img, contours, hierarchy = cv2.findContours(pre, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # OpenCV 4
    contours, hierarchy = cv2.findContours(pre, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Getting the texts bounding boxes based on the text size assumptions
    boxes = []
    i = 0
    htb = 0
    for contour in contours:
        box = cv2.boundingRect(contour)
        h = box[3]
        w = box[2]
        area = cv2.contourArea(contour)
        
        
        if min_text_height_limit < h < max_text_height_limit and 3 < w < 500 and 20 < area < 2000:
            i += 1
            htb = box[3] + htb
            # print(cvarrcontourArea(contour),cv2.boundingRect(contour))
            boxes.append(box)
    # print(htb/i )
    return boxes


def find_table_in_boxes(boxes, cell_threshold=30, min_columns=0):
    cols = {}
    rows = {} 

    # Clustering the bounding boxes by their positions
    for box in boxes:
        (x, y, w, h) = box
        col_key = x // cell_threshold
        row_key = y // cell_threshold
        
        cols[col_key] = [box] if col_key not in cols else cols[col_key] + [box]
        rows[row_key] = [box] if row_key not in rows else rows[row_key] + [box]
    #print(rows.values())
    # Filtering out the clusters having less than 2 cols
    table_cells = list(filter(lambda r: len(r) >= min_columns, rows.values()))
    # Sorting the row cells by x coord
    table_cells = [list(sorted(tb)) for tb in table_cells]
    # Sorting rows by the y coord
    table_cells = list(sorted(table_cells, key=lambda r: r[0][1]))
    #print(rows[0])
    last = 0
    arr = []
    i = 0
    while i < len(rows):
        if(abs(rows[i][0][1] - rows[i+1][0][1]) < 30):
            #rows[i+1].append(rows[i])
            # print("nho hon 30")
            # print(rows[i][0])
            # print(rows[i+1][0])
            # print("-----------------------------------")
            arr.append((rows[i]+rows[i+1]))
            i+=1
        else:
            arr.append((rows[i]))
        i += 1
    print(arr)
    #parrnt(rows.values())
    return table_cells


def build_lines(table_cells):
    if table_cells is None or len(table_cells) <= 0:
        return [], []

    max_last_col_width_row = max(table_cells, key=lambda b: b[-1][2])
    max_x = max_last_col_width_row[-1][0] + max_last_col_width_row[-1][2]

    max_last_row_height_box = max(table_cells[-1], key=lambda b: b[3])
    max_y = max_last_row_height_box[1] + max_last_row_height_box[3]

    hor_lines = []
    ver_lines = []

    for box in table_cells:
        x = box[0][0]
        y = box[0][1]
        hor_lines.append((x, y, max_x, y))

    for box in table_cells[0]:
        x = box[0]
        y = box[1]
        ver_lines.append((x, y, x, max_y))

    (x, y, w, h) = table_cells[0][-1]
    ver_lines.append((max_x, y, max_x, max_y))
    (x, y, w, h) = table_cells[0][0]
    hor_lines.append((x, max_y, max_x, max_y))

    return hor_lines, ver_lines


if "_main_" == "_main_":
    in_file = os.path.join("data/public", "32.png")
    pre_file = os.path.join("data", "pre.png")
    out_file = os.path.join("data", "out.png")

    img = cv2.imread(os.path.join(in_file))

    pre_processed = pre_process_image(img, pre_file)
    text_boxes = find_text_boxes(pre_processed)
    cells = find_table_in_boxes(text_boxes)
    hor_lines, ver_lines = build_lines(cells)

    # Visualize the result
    vis = img.copy()

    for box in text_boxes:
        (x, y, w, h) = box
        cv2.rectangle(vis, (x, y), (x + w - 2, y + h - 2), (0, 255, 0), 1)
    
    # print(cells)
    cv2.rectangle(vis, (212, 18), (212 + 71, 18 + 17 ), (255, 255, 0), 1)
    for line in hor_lines:
        [x1, y1, x2, y2] = line
        cv2.line(vis, (x1, y1), (x2, y2), (0, 0, 255), 1)

    for line in ver_lines:
        [x1, y1, x2, y2] = line
        cv2.line(vis, (x1, y1), (x2, y2), (0, 0, 255), 1)

    cv2.imwrite(out_file, vis)