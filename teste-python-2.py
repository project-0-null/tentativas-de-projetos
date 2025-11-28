import cv2

img = cv2.imread('cadeira.jpeg')

if img is None:
    print("Image not found or could not be loaded.")
else:
    cv2.imshow('cadeira', img)
    cv2.waitKey(0)
    cv2.destroyALLWindows()