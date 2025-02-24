import cv2
path = "picture1.jpg"
image = cv2.imread(path)
cv2.imshow("Output",image)
cv2.waitKey()
cv2.destroyAllWindows()
