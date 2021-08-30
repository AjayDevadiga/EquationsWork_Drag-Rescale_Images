import cv2
import numpy as np
from PIL import Image
from PalmLandMarkDetection import HandDetector




cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector= HandDetector(detectionCon=0.8)
# colorR = (255,0,255)
colorR = (0,0,255)


overlay_img = Image.open("images/p1.jpg")
width, height = overlay_img.size
pil_overlayimg = overlay_img.copy()
cx,cy, w, h  = 400,100,width,height
if width > 200 or height > 110:

    ratio =  height / width
    width = 200
    height = int(ratio * width)
    print(height)
    pil_overlayimg = overlay_img.resize((int(width), int(height)))
    # pil_overlayimg = overlay_img.resize((int(width/4), int(height/4)))
    # pil_overlayimg = overlay_img.thumbnail(MAX_SIZE, Image.ANTIALIAS)
    cx, cy, w, h = 800, 100, width, height


change_inSize = 0




def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

while True:
    # Get image frame
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img, draw=False)
    lmList, bboxInfo = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        tip1x, tip1y = lmList[8]
        cv2.circle(img, (tip1x, tip1y), 10, (0, 0, 255), cv2.FILLED)

        tip2x, tip2y = lmList[12]
        cv2.circle(img, (tip2x, tip2y), 10, (0, 0, 255), cv2.FILLED)

        tip3x, tip3y = lmList[4]
        cv2.circle(img, (tip3x, tip3y), 10, (0, 0, 255), cv2.FILLED)

        dist, _, _ = detector.findDistance(8, 12, img)
        dist_index_to_thumb, _, _ = detector.findDistance(4, 8, img)

        # print(dist)
        # print((cx-w//2, cy-h//2), (cx+w//2, cy+h//2))
        # print(tip1x, tip1y)

        if dist < 60:
            if cx - w // 2 < tip1x < cx + w // 2 and cy - h // 2 < tip1y < cy + h // 2:
                rectColor = (0, 255, 0)
                cx, cy = tip1x, tip1y

        else:

            if 50 < dist_index_to_thumb < 300:

                if cx - w // 2 < tip1x < cx + w // 2 and cy - h // 2 < tip1y < cy + h // 2:
                    change_inSize += 3
                    # print(inc_val)
                    # print(dist_index_to_thumb)
                    # temp_Img = overlay_img.copy()
                    # pil_overlayimg = temp_Img.resize(600, 300)
                    overlay_org = np.array(overlay_img.copy())
                    # cv2.imshow("overlayimg", overlay_org)
                    # cv2.waitKey(0)
                    updated_width = int(width) + change_inSize
                    updated_height = int((height) + (change_inSize))
                    if updated_width < 600:
                        resized_overlay_img = image_resize(overlay_org, width=updated_width, height=None,
                                                           inter=cv2.INTER_AREA)
                        # resized_overlay_img = cv2.resize(overlay_org, (updated_width, updated_height), interpolation = cv2.INTER_NEAREST)
                        pil_overlayimg = Image.fromarray(resized_overlay_img)

            elif dist_index_to_thumb < 50:
                if cx - w // 2 < tip1x < cx + w // 2 and cy - h // 2 < tip1y < cy + h // 2:
                    change_inSize -= 3
                    overlay_org = np.array(overlay_img.copy())
                    updated_width = int(width) + change_inSize
                    updated_height = int((height) + (change_inSize))
                    if updated_width >= 200:
                        resized_overlay_img = image_resize(overlay_org, width=updated_width, height=None,
                                                           inter=cv2.INTER_AREA)
                        pil_overlayimg = Image.fromarray(resized_overlay_img)








        # index_to_thumb_distance_List.append(dist_index_to_thumb)

    bg_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    bg_pill_img = Image.fromarray(bg_img)


    bg_pill_img.paste(pil_overlayimg, (cx-w//2, cy-h//2))
    CombinedImage = np.array(bg_pill_img)
    img = CombinedImage[:, :, ::-1].copy()
    # Find the hand and its landmarks

    # print(detector.handType())
    # print(lmList)
    # x1, y1, x2, y2  = cx-w//2, cy-h//2, cx+w//2, cy+h//2

                # cx, cy = 100,100
    # Display
    # cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), rectColor, cv2.FILLED)
    cv2.imshow("Equations Work | Drag and Rize Images using Hand Gesture", img)
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()