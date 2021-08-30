import cv2
import numpy as np
from PIL import Image
from PalmLandMarkDetection import HandDetector

cap = cv2.VideoCapture("http://192.168.0.102:8080/shot.jpg")
cap.set(3, 1280)
cap.set(4, 720)

Loader_Image = cv2.imread('static/image-5.jpg')
FullCOmbinedImage = Loader_Image
def OpenCam_StartGesture_Recog(openCam_command):
    try:
        if openCam_command:
            global FullCOmbinedImage
            FullCOmbinedImage = Loader_Image
            detector = HandDetector(detectionCon=0.8)
            # colorR = (255,0,255)
            colorR = (0, 0, 255)

            overlay_img = Image.open("images/p1.jpg")
            width, height = overlay_img.size
            pil_overlayimg = overlay_img.copy()
            cx, cy, w, h = 200, 100, width, height
            if width > 200  or height > 112:
                ratio = height / width
                width = 200
                height = int(ratio * width)
                print(height)
                pil_overlayimg = overlay_img.resize((int(width), int(height)))
                cx, cy, w, h = 200, 100, width, height



            def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
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
                resized = cv2.resize(image, dim, interpolation=inter)

                # return the resized image
                return resized

            change_inSize = 0
            global cap
            cap = cv2.VideoCapture(0)
            cap.set(3, 1280)
            cap.set(4, 720)

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
                                    # resized_overlay_img = cv2.resize(overlay_org, (updated_width, updated_height),
                                    #                                  interpolation=cv2.INTER_NEAREST)
                                    resized_overlay_img = image_resize(overlay_org, width=updated_width, height=None,
                                                                       inter=cv2.INTER_AREA)
                                    pil_overlayimg = Image.fromarray(resized_overlay_img)

                        elif dist_index_to_thumb < 50:
                            if cx - w // 2 < tip1x < cx + w // 2 and cy - h // 2 < tip1y < cy + h // 2:
                                change_inSize -= 3
                                overlay_org = np.array(overlay_img.copy())
                                updated_width = int(width) + change_inSize
                                updated_height = int((height) + (change_inSize))
                                if updated_width >= int(width):
                                    # resized_overlay_img = image_resize(overlay_org, width=updated_width, height=None,
                                    #                                    inter=cv2.INTER_AREA)
                                    resized_overlay_img = image_resize(overlay_org, width=updated_width, height=None,
                                                                       inter=cv2.INTER_AREA)
                                    pil_overlayimg = Image.fromarray(resized_overlay_img)


                    # rectColor = (0, 0, 255)
                    # if cx - w // 2 < tip1x < cx + w // 2 and cy - h // 2 < tip1y < cy + h // 2:
                    #     if dist_index_to_thumb < index_to_thumb_distance_List[-1]:
                    #         continue
                    #         # scale_image(scale_type="decrease")
                    #     elif dist_index_to_thumb > index_to_thumb_distance_List[-1]:
                    #         # change_inSize += 3
                    #         continue

                    # scale_image(scale_type="increase")




                    # index_to_thumb_distance_List.append(dist_index_to_thumb)

                bg_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                bg_pill_img = Image.fromarray(bg_img)

                bg_pill_img.paste(pil_overlayimg, (cx - w // 2, cy - h // 2))
                CombinedImage = np.array(bg_pill_img)


                FullCOmbinedImage = CombinedImage[:, :, ::-1].copy()
                # Find the hand and its landmarks
                # imageontop = np.array(pil_overlayimg)
                # cv2.imshow("Overlay_image", imageontop)
                # cv2.waitKey(1)
                # print(detector.handType())
                # print(lmList)
                # x1, y1, x2, y2  = cx-w//2, cy-h//2, cx+w//2, cy+h//2

                # cx, cy = 100,100
                # Display
                # cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), rectColor, cv2.FILLED)
                # cv2.imshow("Equations Work | Drag and Rize Images using Hand Gesture", FullCOmbinedImage)
                # k = cv2.waitKey(1)
                # if k == 27:
                #     break

            # cap.release()
            # cv2.destroyAllWindows()

        elif not openCam_command:
            FullCOmbinedImage = Loader_Image
            try:

                cap.release()
                # cv2.destroyAllWindows()
            except:
                print("Could not close Camera")
            return "ProcessCompleted"
    except Exception as e:
        print("Process Terminated")
        print(e)
    # return



def PassImages():
    global FullCOmbinedImage
    ImagesDetected1 = FullCOmbinedImage
    return ImagesDetected1
