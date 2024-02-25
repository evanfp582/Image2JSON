import cv2

img = cv2.imread("./testImages/Clicker.jpg")

total = 0


def score(event, x, y, flags, param):
    global total
    global img
    if event == cv2.EVENT_LBUTTONDOWN:
        total += 1
        cv2.imshow("COOKIE CLICKER", original)
        tmp = original.copy()
        tmp = cv2.putText(tmp, str(total), (0, 225), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3, cv2.LINE_AA)
        cv2.imshow("COOKIE CLICKER", tmp)


img = cv2.resize(img, (0,0), fx=0.3, fy=0.3, interpolation=cv2.INTER_LINEAR)
original = img.copy()
cv2.imshow("COOKIE CLICKER", img)
cv2.setMouseCallback("COOKIE CLICKER", score)
cv2.waitKey(0)
cv2.destroyAllWindows()
