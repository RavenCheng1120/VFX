import cv2
import numpy as np
import glob
from Robertson import Robertson
from PIL import Image

def readImages(folder):
	imageFormat = ['png', 'JPG']
	files = []
	[files.extend(glob.glob(folder + '*.' + e)) for e in imageFormat]
	imageList = [cv2.imread(file) for file in sorted(files)]

	exposureTimeList = []
	images = glob.glob(folder+"*.JPG")
	for image in sorted(images):
		with open(image, 'rb') as file:
			tempImage = Image.open(file)
			exifdata = tempImage.getexif()
			#  0x829A: "ExposureTime"
			data = exifdata.get(0x829A)
			if isinstance(data, bytes):
				data = data.decode()
			dataValue = data[0] / data[1]
			exposureTimeList.append(dataValue)

	return imageList, exposureTimeList


if __name__ == '__main__':
	sourceImages, ExposureTimes = readImages('SocialScienceLibrary/')
	myhdrPic = Robertson().process(sourceImages, ExposureTimes)