import cv2
import numpy as np
import random

def defineColorX(L, U):
    colorLower = np.array([L, 0, 0], dtype='uint8')
    colorUpper = np.array([U, 255, 255], dtype='uint8')
    
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        if (cv2.contourArea(c)>5000):
            (curr_x, curr_y), radii = cv2.minEnclosingCircle(c)
            if radii > 10:
                cv2.circle(frame, (int(curr_x), int(curr_y)), int(radii), (0, 255, 255), 2)
                return curr_x
    
    return -1

cam = cv2.VideoCapture(0)
cv2.namedWindow('camera', cv2.WINDOW_KEEPRATIO)

balls_coords = {}
order = ["red", "green", "yellow"]
random.shuffle(order)


  
while cam.isOpened():
    ret, frame = cam.read()

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    custom_order = []
    
    balls_coords['yellow'] = defineColorX(21, 26)
    balls_coords['green'] = defineColorX(61, 76)
    balls_coords['red'] = defineColorX(1, 3)
    
    if (balls_coords['yellow']!=-1 and balls_coords['green']!=-1 and balls_coords['red']!=-1):
        balls_coords = {key: balls_coords[key] for key in sorted(balls_coords, key = lambda x: balls_coords[x])}
        for color in balls_coords:
            custom_order.append(color)
        if (custom_order == order):
            break


    cv2.imshow('camera', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()