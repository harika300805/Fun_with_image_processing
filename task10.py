import cv2
path = "rgb.jpg"
image = cv2.imread(path)
edges = cv2.Canny(image,200,300)
cv2.imshow("Output",image)
cv2.imshow("Edges",edges)
cv2.waitKey()
cv2.destroyAllWindows()
