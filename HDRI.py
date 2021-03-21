import cv2
import numpy as np
import glob

def readImages(folder):
	imageFormat = ['png', 'jpg']
	files = []
	[files.extend(glob.glob(folder + '*.' + e)) for e in imageFormat]
	imageList = [cv2.imread(file) for file in files]
	grayscaleList = turnGrayscale(imageList)
	# print(len(imageList))
	return imageList, grayscaleList


def turnGrayscale(imageList):
	grayscaleList = []
	for img in imageList:
		grayscaleList.append(np.dot(img[...,:3], [19/256, 183/256, 54/256]).astype(np.uint8))
	# cv2.imshow('grayscaleImage', grayscaleList[0])
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	return grayscaleList


def binaryThreshold(imageList):
	binaryImageList = []
	count = 0
	for img in imageList:
		threshold = np.median(img)
		binaryImage = np.zeros(imageList[0].shape, np.uint8)
		for row in range(len(img)):
			for column in range(len(img[0])):
				if img[row][column] > threshold:
					binaryImage[row][column] = 255
				else:
					binaryImage[row][column] = 0
		binaryImageList.append(binaryImage)
		print("Binary image " + str(count) + " processing...")
		count += 1
	return binaryImageList




if __name__ == '__main__':
	sourceImages, grayImages = readImages('Memorial_SourceImages/')
	binaryImages = binaryThreshold(grayImages)