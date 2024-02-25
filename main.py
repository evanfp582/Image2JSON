import textGroupIsolation
import cv2
import os


def main():
    dir = "./testImages"
    imgs = []
    for path in os.listdir(dir):
        imgs.append(cv2.imread(dir + "/" + path))
    textGroupIsolation.groupText(imgs)
  

if __name__ == "__main__":
    main()
