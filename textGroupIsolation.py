import cv2
import pytesseract


pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


def groupText(img):
    file = open("recognized.txt", "w+")
    file.write("")
    file.close()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    dilated = cv2.dilate(thresh, kernel)
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    file = open("recognized.txt", "a")
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        rect = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cropped = img[y:y+h, x:x+w]

        text = pytesseract.image_to_string(cropped)
        if len(text) > 0:
            file.write(text)
            file.write("\n")

    file.close()

    cv2.imshow("Image", cv2.resize(img, (0, 0), fx=0.3, fy=0.3))
    cv2.waitKey(0)
