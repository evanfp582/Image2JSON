import cv2
import pytesseract
import json

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


def getContours(img, kernel_size):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    dilated = cv2.dilate(thresh, kernel, iterations=4)
    # cv2.imshow("Dilated", cv2.resize(dilated, (0,0), fx=0.2, fy=0.2))
    # cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours


def groupText(imgs):
    file = open("recognized.txt", "w+")
    file.write("")
    file.close()
    history = {}
    prev_sections = 100
    for img in imgs:
        height, width, _ = img.shape

        contours = getContours(img, 30)
        file = open("recognized.txt", "a")
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if abs(width - w) < 50 or w < 600:
                continue
            rect = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cropped = img[y:y + h, x:x + w]
            test = pytesseract.image_to_string(cropped)
            if test == "":
                continue

            inner_contours = getContours(cropped, 10)
            sections = []
            for cntr in inner_contours:
                x1, y1, w1, h1 = cv2.boundingRect(cntr)
                if w1 < 100:
                    continue
                rect = cv2.rectangle(cropped, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
                sections.append([x1, y1, w1, h1])

            sections.reverse()
            print(len(sections))
            imageIndex = findIngIndex(sections)
            for i in range(len(sections)):
                x1, y1, _, _ = sections[i]
                cv2.putText(cropped, str(i), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)

            if (len(sections), imageIndex) not in history.keys():
                tmp = cropped.copy()
                cv2.imshow("Cropped", cv2.resize(tmp, (0, 0), fx=0.3, fy=0.3))
                key = cv2.waitKey(0)
                if key == 27:
                    cv2.destroyAllWindows()
                meanings = {}
                types = {}
                for i in range(len(sections)):
                    meaning = input(f"What is in section {i}?")
                    store_type = input(f"How do you want to store the {meaning} section? ([string], array): ")
                    if store_type == "":
                        store_type = "string"
                    while store_type != "string" and store_type != "array":
                        store_type = input("Invalid Choice.\nHow do you want to store the text? ([string], array): ")
                        if store_type == "":
                            store_type = "string"

                    types[i] = store_type
                    meanings[i] = meaning

                history[(len(sections), imageIndex)] = [meanings, types]

            file_write = True
            if len(sections) < 4 and prev_sections > 3:
                file_write = False
                parsed_info = {}
            elif len(sections) < 4:
                file_write = False
            elif len(sections) > 3 and prev_sections < 4:
                text = json.dumps(parsed_info)
                file.write(text)
                file.write("\n")
                parsed_info = {}
            else:
                parsed_info = {}
            prev_sections = len(sections)
            meanings = history.get((len(sections), imageIndex))[0]
            types = history.get((len(sections), imageIndex))[1]
            for i in range(len(sections)):
                meaning = meanings.get(i)
                store_type = types.get(i)
                x1, y1, w1, h1 = sections[i]
                area = img[y + y1:y + y1 + h1, x + x1:x + x1 + w1]

                text = pytesseract.image_to_string(area)
                if store_type == "array":
                    parsed_info[meaning] = text.strip().split("\n")
                elif meaning in parsed_info.keys():
                    text = text.strip().replace("\n", " ") \
                        .replace("@", "1/2").replace("^", "2/3").replace("*", "1/3") \
                        .replace("$", "1/4").replace("_", "3/4")
                    parsed_info[meaning] = parsed_info.get(meaning) + text
                else:
                    text = text.strip().replace("\n", " ") \
                        .replace("@", "1/2").replace("^", "2/3").replace("*", "1/3") \
                        .replace("$", "1/4").replace("_", "3/4")
                    parsed_info[meaning] = text

            for sects in parsed_info.keys():
                print(sects + ":\n")
                print(parsed_info.get(sects))

            text = json.dumps(parsed_info)
            if len(text) > 0 and file_write:
                file.write(text)
                file.write("\n")

    file.close()


def findIngIndex(sections):
    if len(sections) < 3:
        return 0
    # print(sections)
    img = sorted(sections, key=lambda x: x[2])[2]
    # print(img)
    for i, section in enumerate(sections):
        # print("Section: ", section)
        if section == img:
            # print("Hello? ", i)
            return i
