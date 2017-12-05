# CV-PA3
Assignment 3

Histogram of Gradients

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
     
    now with histogram for each block of the image, concatenate the histograms.
    
    
