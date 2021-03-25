import cv2
import numpy as np
import glob

def readImages(folder):
	imageFormat = ['png', 'jpg']
	files = []
	[files.extend(glob.glob(folder + '*.' + e)) for e in imageFormat]
	imageList = [cv2.imread(file) for file in sorted(files)]
	grayscaleList = turnGrayscale(imageList)
	# print(len(imageList))
	return imageList, grayscaleList

def showImage(img):
	cv2.imshow('image', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return

def turnGrayscale(imageList):
	grayscaleList = []
	count = 0
	for img in imageList:
		grayscaleList.append(np.dot(img[...,:3], [19/256, 183/256, 54/256]).astype(np.uint8))
		# grayscaleList.append(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
		# cv2.imwrite('./grayscale/'+str(count)+'.png', grayscaleList[count])
		count += 1
	return grayscaleList


def binaryThreshold(imageList):
	binaryImageList = []
	count = 0
	for img in imageList:
		threshold = np.median(img)
		if threshold < 20.0:
			threshold = 20.0
		binaryImage = np.zeros(imageList[0].shape, np.uint8)
		for row in range(len(img)):
			for column in range(len(img[0])):
				if img[row][column] > threshold:
					binaryImage[row][column] = 255
				else:
					binaryImage[row][column] = 0
		binaryImageList.append(binaryImage)
		print("Binary image " + str(count) + " processing...")
		print(threshold)
		# cv2.imwrite('./binary/'+str(count)+'.png', binaryImage)
		count += 1
	return binaryImageList


def excludeMask(imageList):
	maskImageList = []
	for img in imageList:
		mask_img = cv2.inRange(img, np.median(img) - 4, np.median(img) + 4)
		maskImageList.append(mask_img)
	return maskImageList


# def MedianThresholdBitmap():



if __name__ == '__main__':
	sourceImages, grayImages = readImages('Memorial_SourceImages/')
	binaryImages = binaryThreshold(grayImages)
	maskImages = excludeMask(grayImages)