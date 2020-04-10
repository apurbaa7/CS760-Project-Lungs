import csv
import os
import numpy as np # linear algebra
import cv2
import matplotlib.pyplot as plt
#%matplotlib inline
from sklearn.model_selection import train_test_split

def getdata_seg(IMAGE_LIB, MASK_LIB, IMG_HEIGHT, IMG_WIDTH, TEST_RATIO):
    all_images = [x for x in sorted(os.listdir(IMAGE_LIB)) if x[-4:] == '.tif']

    x_data = np.empty((len(all_images), IMG_HEIGHT, IMG_WIDTH), dtype='float32')
    for i, name in enumerate(all_images):
        im = cv2.imread(IMAGE_LIB + name, cv2.IMREAD_UNCHANGED).astype("int16").astype('float32')
        im = cv2.resize(im, dsize=(IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_LANCZOS4)
        im = (im - np.min(im)) / (np.max(im) - np.min(im))
        x_data[i] = im

    y_data = np.empty((len(all_images), IMG_HEIGHT, IMG_WIDTH), dtype='float32')
    for i, name in enumerate(all_images):
        im = cv2.imread(MASK_LIB + name, cv2.IMREAD_UNCHANGED).astype('float32')/255.
        im = cv2.resize(im, dsize=(IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_NEAREST)
        y_data[i] = im

    # %% [code]
    #fig, ax = plt.subplots(1,2, figsize = (8,4))
    #ax[0].imshow(x_data[0], cmap='gray')
    #ax[1].imshow(y_data[0], cmap='gray')
	#plt.show()

    # %% [code]
    x_data = x_data[:,:,:,np.newaxis]
    y_data = y_data[:,:,:,np.newaxis]
    #x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size = 0.5)
    return train_test_split(x_data, y_data, test_size = TEST_RATIO)

def getdata_reg(MASK_LIB, IMG_HEIGHT, IMG_WIDTH, TEST_RATIO):
	with open('../input/lung_stats.csv') as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		x_data = []
		y_data = []
		for row in readCSV:
			# read mask image
			if row[0] == 'img_id':
				continue
			#print(MASK_LIB + row[0])
			im = cv2.imread(MASK_LIB + row[0], cv2.IMREAD_UNCHANGED).astype('float32')/255.0
			im = cv2.resize(im, dsize=(IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_NEAREST)
			x_data.append(im)
			y_data.append(np.float(row[3]))

	x_data = np.array(x_data)
	y_data = np.array(y_data)
	x_data = x_data[:,:,:,np.newaxis]
	y_data = y_data[:,np.newaxis]
	print(x_data.shape)
	print(y_data.shape)

	#print(y_data)
    #x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size = 0.5)
	return train_test_split(x_data, y_data, test_size = TEST_RATIO)
