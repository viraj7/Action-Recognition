# Computer Vision Action Recognition
Action recognition using Histogram of Gradients and support vector machines 

1) Histogram of Gradients

   Applying the following masks to compute gradients:
    [-1, 0, 1], [-1,
                  0,
                  1]
                  
   Calculate the magnitude and orientation
     sqrt(x**2 + y**2)
     atan2(y / x)
     
     
   Compute histogram:
    For each class 0, 20, 40, ..., 160,
     Adding values coresponding to the orientation.
     if orientation = 20, add the magnitude to second bin.
     if orientation = 10 add 50% to 0 and 50% to 20
     
   Now with histogram for each block of the image, concatenate the histograms.
    
    
    
    
2) SVM classifier from sklearn
 
 training all the data using clf.fit(train_data, train_label)
 get accuracy using clf.score(test_data, test_label)
 or 
 test on untrained data using clf.predict(test_data)
 and get True positives, False positives, False negatives, and True negatives using confusion matrix
