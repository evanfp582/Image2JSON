import textGroupIsolation
import cv2


def main():
    img = cv2.imread("testImages/20240224_122308.jpg")
    textGroupIsolation.groupText(img)
  

if __name__ == "__main__":
    main()
