import numpy as np
import cv2

def detectColorSquares(image, color_ranges, min_size=500):
  contour_list=[]
  for lower,upper in color_ranges:  
  
    mask = cv2.inRange(image, lower, upper)
    cnts,hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
      epsilon = 0.01*cv2.arcLength(c, True)
      approx = cv2.approxPolyDP(c,epsilon,True)
      
      if len(approx)==4 and cv2.contourArea(approx) > min_size:
        contour_list.append([approx])
  return contour_list

if __name__ == "__main__":
  image = cv2.imread('sample.jpg')
  orig = image.copy()
  image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

  line_size = 5
  mask_count=5000

  mask_ranges = np.random.randint(0,255,(mask_count,2,3))
  detected = detectColorSquares(image, mask_ranges)

  for shape in detected:
    cv2.drawContours(orig, shape, -1, (255,0,0), line_size)
  cv2.imwrite('out.png',orig)
