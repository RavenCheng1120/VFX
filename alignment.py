import cv2
import numpy as np
import glob

def readImages(folder):
	imageFormat = ['png', 'JPG']
	files = []
	[files.extend(glob.glob(folder + '*.' + e)) for e in imageFormat]
	imageList = [cv2.imread(file) for file in sorted(files)]
	grayscaleList = turnGrayscale(imageList)
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
		count += 1
	return grayscaleList


# def binaryThreshold(imageList):
# 	binaryImageList = []
# 	count = 0
# 	for img in imageList:
# 		threshold = np.median(img)
# 		''' Restrict the threshold value to prevent noise '''
# 		if threshold < 20.0:
# 			threshold = 20.0
# 		binaryImage = np.zeros(imageList[0].shape, np.uint8)
# 		for row in range(len(img)):
# 			for column in range(len(img[0])):
# 				if img[row][column] > threshold:
# 					binaryImage[row][column] = 255
# 				else:
# 					binaryImage[row][column] = 0
# 		binaryImageList.append(binaryImage)
# 		print("Binary image " + str(count) + " processing...")
# 		print(threshold)
# 		# cv2.imwrite('./binary/'+str(count)+'.png', binaryImage)
# 		count += 1
# 	return binaryImageList


# def excludeMask(imageList):
# 	maskImageList = []
# 	for img in imageList:
# 		mask_img = cv2.inRange(img, np.median(img) - 4, np.median(img) + 4)
# 		maskImageList.append(mask_img)
# 	return maskImageList


# -------------- Median Threshold Bitmap ------------------
def ComputeBitmaps(img):
	threshold_bitmap = np.zeros(img.shape, np.uint8)
	threshold = np.median(img)
	if threshold < 20.0:
			threshold = 20.0
	for row in range(len(img)):
		for column in range(len(img[0])):
			if img[row][column] > threshold:
				threshold_bitmap[row][column] = 255

	exclusion_bitmap = cv2.inRange(img, np.median(img) - 4, np.median(img) + 4)
	np.invert(exclusion_bitmap)

	return threshold_bitmap, exclusion_bitmap


def imageShrink(img):
	return cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)


def GetExpShift(img1, img2, shift_bits):
	cur_shift = np.zeros(2)
	if shift_bits > 0:
		sml_img1 = imageShrink(img1)
		sml_img2 = imageShrink(img2)
		cur_shift = GetExpShift(sml_img1, sml_img2, shift_bits - 1)
		cur_shift[0] *= 2
		cur_shift[1] *= 2
	else:
		cur_shift[0] = cur_shift[1] = 0
	tb1, eb1 = ComputeBitmaps(img1)
	tb2, eb2 = ComputeBitmaps(img2)
	min_err = len(img1) * len(img1[0])
	shift_ret = np.zeros(2)
	for i in range(-1,2):
		for j in range(-1,2):
			xs = cur_shift[0] + i
			ys = cur_shift[1] + j
			M = np.float32([[1, 0, xs], [0, 1, ys]])
			shifted_tb2 = np.zeros(tb2.shape)
			shifted_eb2 = np.zeros(eb2.shape)
			tb_rows, tb_cols = tb2.shape[:2]
			shifted_tb2 = cv2.warpAffine(tb2, M, (tb_cols, tb_rows))
			shifted_eb2 = cv2.warpAffine(eb2, M, (tb_cols, tb_rows))
			diff_b = np.logical_xor(tb1, shifted_tb2)
			diff_b = np.logical_and(diff_b, eb1)
			diff_b = np.logical_and(diff_b, shifted_eb2)
			err = np.sum(diff_b == 255)
			if (err < min_err):
				shift_ret[0] = xs
				shift_ret[1] = ys
				min_err = err
	return shift_ret


def MedianThreshold(sourceImages, imageList):
	alignedImageList = []
	img_rows, img_cols = imageList[0].shape[:2]
	count = 0
	for img, sourceimg in zip(imageList, sourceImages):
		shift_step = GetExpShift(imageList[0], img, 3)
		M = np.float32([[1, 0, shift_step[0]], [0, 1, shift_step[1]]])
		tempImage = cv2.warpAffine(sourceimg, M, (img_cols, img_rows))
		alignedImageList.append(tempImage)

		cv2.imwrite('./MTB result/'+str(count)+'.png', tempImage)
		count += 1
		print('Image'+str(count)+' complete')
	return alignedImageList


if __name__ == '__main__':
	sourceImages, grayImages = readImages('SocialScienceLibrary/')
	MedianThreshold(sourceImages, grayImages)
	# binaryImages = binaryThreshold(grayImages)
	# maskImages = excludeMask(grayImages)