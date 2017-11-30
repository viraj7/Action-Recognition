from __future__ import division
import math, cv2, sys, os, time, scipy, sklearn
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import random as rn
from sklearn import svm
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix


def read_image(path):
	imlist  = []
	labels = []
	c = 0
	im_path = os.listdir(path)
	for i in im_path:
		if i != '.DS_Store':
			dire = os.path.join(path, i)
			im2 = os.listdir(dire)
			for j in im2:
				if j != '.DS_Store':
					dir1 = os.path.join(dire, j)
					im3 = os.listdir(dir1)
					for k in im3:
						if (k != '.DS_Store') and (k.endswith('jpg')):
							imlist.append(os.path.join(dir1, k))
	imlist = np.array(imlist)
	for imfile in imlist:
		labels.append(imfile.split('/')[8])
        #print(t)
	labels = np.array(labels)
	return imlist, labels

def read_data(imlist, labels):
	DivingSide, WalkFront, GolfSwing, Kicking, Lifting, RidingHorse, Run, SkateBoarding, Swing = [], [], [], [], [], [], [], [], []
	DivingSide_label, WalkFront_label, GolfSwing_label, Kicking_label, Lifting_label, RidingHorse_label, Run_label, SkateBoarding_label, Swing_label = [], [], [], [], [], [], [], [], []

	for t in imlist:
		j = t.split('/')[-3]
		if j == 'Diving-Side':
			DivingSide.append(t)
			DivingSide_label.append('DivingSide')
			#print t
		if j == 'Golf-Swing-Back' or j == 'Golf-Swing-Front' or j == 'Golf-Swing-Side':
			GolfSwing.append(t)
			GolfSwing_label.append('GolfSwing')
		if j == 'Kicking-Side' or j == 'Kicking-Front':
			Kicking.append(t)
			Kicking_label.append('Kicking')
		if j == 'Lifting':
			Lifting.append(t)
			Lifting_label.append('Lifting')
		if j == 'Riding-Horse':
			RidingHorse.append(t)
			RidingHorse_label.append('RidingHorse')
		if j == 'Run-Side':
			Run.append(t)
			Run_label.append('Run')
		if j == 'SkateBoarding-Front':
			SkateBoarding.append(t)
			SkateBoarding_label.append('SkateBoarding')
		if j == 'Swing-Bench' or j == 'Swing-SideAngle':
			Swing.append(t)
			Swing_label.append('Swing')
		if j == 'Walk-Front':
			WalkFront.append(t)
			WalkFront_label.append('WalkFront')
	print len(WalkFront_label)+ len(DivingSide_label)+  len(GolfSwing_label)+ len(Kicking_label)+ len(Lifting_label)+  len(RidingHorse_label)+  len(Run_label) +  len(Swing_label) +  len(SkateBoarding_label)
	return WalkFront, DivingSide, GolfSwing, Kicking, Lifting, RidingHorse, Run, Swing, SkateBoarding, WalkFront_label, DivingSide_label, GolfSwing_label, Kicking_label,  Lifting_label,   RidingHorse_label, Run_label , Swing_label, SkateBoarding_label


def image_process(image):
	I = np.array(Image.open(image))
	size = cv2.resize(I, (300, 300), interpolation = cv2.INTER_AREA)
	gray = cv2.cvtColor(size, cv2.COLOR_BGR2GRAY)
	return gray

def hog(image):
	gx = cv2.Sobel(image, cv2.CV_32F, 1, 0)
	gy = cv2.Sobel(image, cv2.CV_32F, 0, 1)
	mag, ang = cv2.cartToPolar(gx, gy)
    # quantizing binvalues in (0...16)
	bins = np.int32(bin_n*ang/(2*np.pi))

	# Divide to 4 sub-squares
	bin_cells = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
	mag_cells = mag[:10,:10], mag[10:,:10], mag[:10,10:], mag[10:,10:]
	hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
	hist = np.hstack(hists)
	return hist

def get_features(WalkFront, DivingSide, GolfSwing, Kicking, Lifting, RidingHorse, Run, Swing, SkateBoarding):
	DivingSide_data, WalkFront_data, GolfSwing_data, Kicking_data, Lifting_data, RidingHorse_data, Run_data, SkateBoarding_data, Swing_data = [], [], [], [], [], [], [], [], []

	for i in range(len(DivingSide)):
		frame = image_process(DivingSide[i])
		data = hog(frame)
		DivingSide_data.append(data)
		#print 1, i
	print "DivingSide", np.shape(np.array(DivingSide_data))

	for i in range(len(WalkFront)):
		frame = image_process(WalkFront[i])
		data = hog(frame)
		WalkFront_data.append(data)
		#print 2, i
	print "Walkfront", np.shape(np.array(WalkFront_data))

	for i in range(len(GolfSwing)):
		frame = image_process(GolfSwing[i])
		data = hog(frame)
		GolfSwing_data.append(data)
		#print 3, i
	print "GolfSwing", np.shape(np.array(GolfSwing_data))

	for i in range(len(Kicking)):
		frame = image_process(Kicking[i])
		data = hog(frame)
		Kicking_data.append(data)
		#print 4, i
	print "Kicking", np.shape(np.array(Kicking_data))

	for i in range(len(Lifting)):
		frame = image_process(Lifting[i])
		data = hog(frame)
		Lifting_data.append(data)
		#print 5, i
	print "Lifting", np.shape(np.array(Lifting_data))

	for i in range(len(RidingHorse)):
		frame = image_process(RidingHorse[i])
		data = hog(frame)
		RidingHorse_data.append(data)
		#print 6, i
	print "HorseRiding", np.shape(np.array(RidingHorse_data))

	for i in range(len(Run)):
		frame = image_process(Run[i])
		data = hog(frame)
		Run_data.append(data)
		#print 7, i
	print "Run", np.shape(np.array(Run_data))

	for i in range(len(SkateBoarding)):
		frame = image_process(SkateBoarding[i])
		data = hog(frame)
		SkateBoarding_data.append(data)
		#print 8, i
	print "SkateBoarding", np.shape(np.array(SkateBoarding_data))

	for i in range(len(Swing)):
		frame = image_process(Swing[i])
		data = hog(frame)
		Swing_data.append(data)
		#print 9, i
	print "Swing", np.shape(np.array(Swing_data))
	return WalkFront_data, DivingSide_data, GolfSwing_data, Kicking_data, Lifting_data, RidingHorse_data, Run_data, Swing_data, SkateBoarding_data


def Leave_One_Out(i, subset_size, data, label):
    return data[i*subset_size:][:subset_size], data[:i*subset_size] + data[(i+1)*subset_size:], label[i*subset_size:][:subset_size], label[:i*subset_size] + label[(i+1)*subset_size:]

def eval(arr):
 	TP, TN, FP, FN, sensitivity, specificity = [], [], [], [], [], []
 	for i in range(9):
 		for j in range(9):
 			if i == j:
 				TP.append(arr[i][j])
 	sum_cols = arr.sum(axis = 1)
 	sum_rows = arr.sum(axis = 0)
 	for i in range(9):
 		FN.append(sum_cols[i] - TP[i])
 		FP.append(sum_rows[i] - TP[i])
 		TN.append(arr.sum()-sum_rows[i] - sum_cols[i])
 	print TP, TN, FP, FN
 	for i in range(9):
 		sense = (TP[i]/(TP[i] + FN[i]))
 		spec = (TN[i]/(FP[i] + TN[i]))
 		sensitivity.append(sense)
 		specificity.append(spec)
 	return sensitivity, specificity


def Evaluation(data_train, data_test, label_train, label_test, i):
	clf = svm.SVC( kernel = 'linear', C = 1, gamma = 0.0000001)
	clf.fit(data_train, label_train)
	predicted = clf.predict(data_test)
	error = (label_test == predicted).mean()
	label = [ 'DivingSide', 'WalkFront','GolfSwing', 'Kicking', 'Lifting', 'RidingHorse', 'Run', 'SkateBoarding' , 'Swing']
	arr = confusion_matrix(label_test, predicted, label)
	print arr
	print 'for', i, 'iteration the accuracy of svm is %.2f %%' %(error*100)
	return error, arr


def training_testing(WalkFront_data, DivingSide_data, GolfSwing_data, Kicking_data,  Lifting_data,   RidingHorse_data, Run_data , Swing_data, SkateBoarding_data, WalkFront_label, DivingSide_label, GolfSwing_label, Kicking_label,  Lifting_label,   RidingHorse_label, Run_label , Swing_label, SkateBoarding_label):
	num_folds = 5
	label = [ 'DivingSide', 'WalkFront','GolfSwing', 'Kicking', 'Lifting', 'RidingHorse', 'Run', 'SkateBoarding' , 'Swing']
	DivingSide_train, WalkFront_train, GolfSwing_train, Kicking_train, Lifting_train, RidingHorse_train, Run_train, SkateBoarding_train, Swing_train = [], [], [], [], [], [], [], [], []

	DivingSide_test, WalkFront_test, GolfSwing_test, Kicking_test, Lifting_test, RidingHorse_test, Run_test, SkateBoarding_test, Swing_test = [], [], [], [], [], [], [], [], []

	DivingSide_label_train, WalkFront_label_train, GolfSwing_label_train, Kicking_label_train, Lifting_label_train, RidingHorse_label_train, Run_label_train, SkateBoarding_label_train, Swing_label_train = [], [], [], [], [], [], [], [], []

	DivingSide_label_test, WalkFront_label_test, GolfSwing_label_test, Kicking_label_test, Lifting_label_test, RidingHorse_label_test, Run_label_test, SkateBoarding_label_test, Swing_label_test = [], [], [], [], [], [], [], [], []

	training_data, test_data, training_label, test_label, err, sensitivity, specificity = [], [], [], [], [], [], []
	#DivingSide
	for i in range(num_folds):

		subset_size = int(len(DivingSide_data)/num_folds)
		DivingSide_test, DivingSide_train, 	DivingSide_label_test, DivingSide_label_train = Leave_One_Out(i, subset_size, DivingSide_data, DivingSide_label)

		subset_size = int(len(WalkFront_data)/num_folds)
		WalkFront_test, WalkFront_train, 	WalkFront_label_test, WalkFront_label_train = Leave_One_Out(i, subset_size, WalkFront_data, WalkFront_label)

		subset_size = int(len(GolfSwing_data)/num_folds)
		GolfSwing_test, GolfSwing_train, 	GolfSwing_label_test, GolfSwing_label_train = Leave_One_Out(i, subset_size, GolfSwing_data, GolfSwing_label)

		subset_size = int(len(Kicking_data)/num_folds)
		Kicking_test, Kicking_train, Kicking_label_test, Kicking_label_train = Leave_One_Out(i, subset_size, Kicking_data, Kicking_label)

		subset_size = int(len(Lifting_data)/num_folds)
		Lifting_test, Lifting_train, Lifting_label_test, Lifting_label_train = Leave_One_Out(i, subset_size, Lifting_data, Lifting_label)

		subset_size = int(len(RidingHorse_data)/num_folds)
		RidingHorse_test, RidingHorse_train, RidingHorse_label_test, RidingHorse_label_train = Leave_One_Out(i, subset_size, RidingHorse_data, RidingHorse_label)

		subset_size = int(len(Run_data)/num_folds)
		Run_test, Run_train, Run_label_test, Run_label_train = Leave_One_Out(i, subset_size, Run_data, Run_label)

		subset_size = int(len(SkateBoarding_data)/num_folds)
		SkateBoarding_test, SkateBoarding_train, SkateBoarding_label_test, SkateBoarding_label_train = Leave_One_Out(i, subset_size, SkateBoarding_data, SkateBoarding_label)

		subset_size = int(len(Swing_data)/num_folds)
		Swing_test, Swing_train, Swing_label_test, Swing_label_train = Leave_One_Out(i, subset_size, Swing_data, Swing_label)

		print 'Done Splitting each class into test and train', i

		training_data = DivingSide_train + WalkFront_train + GolfSwing_train + Kicking_train + Lifting_train + RidingHorse_train + Run_train + SkateBoarding_train + Swing_train
		test_data = DivingSide_test + WalkFront_test + GolfSwing_test + Kicking_test + Lifting_test + RidingHorse_test + Run_test + SkateBoarding_test + Swing_test
		training_label = DivingSide_label_train + WalkFront_label_train + GolfSwing_label_train + Kicking_label_train + Lifting_label_train + RidingHorse_label_train +	Run_label_train + SkateBoarding_label_train + Swing_label_train
		test_label = DivingSide_label_test + WalkFront_label_test + GolfSwing_label_test + Kicking_label_test + Lifting_label_test + RidingHorse_label_test + Run_label_test + SkateBoarding_label_test + Swing_label_test

		error, arr = Evaluation(training_data, test_data, training_label, test_label, i)
		err.append(error)
		print np.shape(np.array(test_data)), np.shape(np.array(training_data))
		sensitivity, specificity =  eval(arr)
	accuracy = sum(err)/len(err)
	print 'Overall accuracy is: %.2f %%' %(accuracy*100)
	for i in range(9):
		print 'Sensitivity of', label[i], 'is' , sensitivity[i]
		print 'Specificity of', label[i], 'is', specificity[i]


def start():
	imlist, labels = [], []

	DivingSide, WalkFront, GolfSwing, Kicking, Lifting, RidingHorse, Run, SkateBoarding, Swing = [], [], [], [], [], [], [], [], []

	DivingSide_label, WalkFront_label, GolfSwing_label, Kicking_label, Lifting_label, RidingHorse_label, Run_label, SkateBoarding_label, Swing_label = [], [], [], [], [], [], [], [], []

	DivingSide_data, WalkFront_data, GolfSwing_data, Kicking_data, Lifting_data, RidingHorse_data, Run_data, SkateBoarding_data, Swing_data = [], [], [], [], [], [], [], [], []

	imlist, labels = read_image('/Users/virajj/Downloads/ucf_sports_actions/ucf_action')
	WalkFront, DivingSide, GolfSwing, Kicking, Lifting, RidingHorse, Run, Swing, SkateBoarding, WalkFront_label, DivingSide_label, GolfSwing_label, Kicking_label,  Lifting_label,   RidingHorse_label, Run_label , Swing_label, SkateBoarding_label = read_data(imlist, labels)
	WalkFront_data, DivingSide_data, GolfSwing_data, Kicking_data,  Lifting_data,   RidingHorse_data, Run_data , Swing_data, SkateBoarding_data = get_features(WalkFront, DivingSide, GolfSwing, Kicking, Lifting, RidingHorse, Run, Swing, SkateBoarding)
	training_testing(WalkFront_data, DivingSide_data, GolfSwing_data, Kicking_data,  Lifting_data,   RidingHorse_data, Run_data , Swing_data, SkateBoarding_data, WalkFront_label, DivingSide_label, GolfSwing_label, Kicking_label,  Lifting_label,   RidingHorse_label, Run_label , Swing_label, SkateBoarding_label)


bin_n = 16
start()
