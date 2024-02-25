import cv2
import pytesseract
import numpy as np


pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


def getContours(img, kernel_size):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    dilated = cv2.dilate(thresh, kernel, iterations=4)
    cv2.imshow("Dilated", cv2.resize(dilated, (0, 0), fx=0.2, fy=0.2))
    cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours


def groupText(img):
    file = open("recognized.txt", "w+")
    file.write("")
    file.close()
    height, width, _ = img.shape

    contours = getContours(img, 30)
    file = open("recognized.txt", "a")
    sections_num = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if abs(width-w) < 50 or w < 600:
            continue
        rect = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cropped = img[y:y + h, x:x + w]
        inner_contours = getContours(cropped, 10)
        sections = []
        for cntr in inner_contours:
            x1, y1, w1, h1 = cv2.boundingRect(cntr)
            if w1 < 100:
                continue
            rect = cv2.rectangle(cropped, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
            sections.append([x1, y1, w1, h1])

        sections.reverse()
        for i in range(len(sections)):
            x1, y1, _, _ = sections[i]
            cv2.putText(cropped, str(i), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)

        cv2.imshow("Cropped", cv2.resize(cropped, (0, 0), fx=0.3, fy=0.3))
        key = cv2.waitKey(0)
        if key == 27:
            cv2.destroyAllWindows()

        if sections_num != len(sections):
            meanings = {}
            sections_num = len(sections)
            for i in range(len(sections)):
                meaning = input(f"What is in section {i}?")
                meanings[i] = meaning

        parsed_info = {}
        for i in range(len(sections)):
            meaning = meanings.get(i)
            x1, y1, w1, h1 = sections[i]
            area = img[y + y1:y + y1 + h1, x + x1:x + x1 + w1]
            text = pytesseract.image_to_string(area)
            if meaning in parsed_info.keys():
                parsed_info[meaning] = parsed_info.get(meaning) + text
            else:
                parsed_info[meaning] = text

        print(parsed_info)
        text = pytesseract.image_to_string(cropped)
        if len(text) > 0:
            file.write(text)
            file.write("\n")

    file.close()

    cv2.imshow("Image", cv2.resize(img, (0, 0), fx=0.3, fy=0.3))
    cv2.waitKey(0)
