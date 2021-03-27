# project #1: High Dynamic Range Imaging
## Image Alignment:  Median Threshold Bitmap (MTB)
參考文件：http://www.anyhere.com/gward/papers/jgtpap2.pdf  

- Read in all the images

- Turn them into grayscale images

- Use median value to make them binary images  
Median value 過低或過高可能會導致影像雜訊很多，所以要限制 median value 的上下限。此處限制 median 不可低於 20。  

- Deal with Threshold Noise  
Our exclusion bitmap consists of 0’s wherever the grayscale value is within some specified distance of the threshold, and 1’s elsewhere. The effect is to disregard differences that are less than the noise tolerance in our images.  
在 median 的正負4 以內的 pixel 值設為0 (黑色)，作為 exclusion bitmap。  
> excludeMask  
> 用法cv2.inRange(img,low,high)，函式會將位於兩個區域間的值置為255，位於區間外的值置為0。 

- Align the threshold bitmap  
方法一：One brute force approach is to test every offset within the allowed range, computing the XOR difference at each offset and taking the coordinate pair corresponding to the minimum difference.  
方法二：A more efficient approach might follow a gradient descent to a local minimum, computing only local bitmaps differences between the starting offset (0,0) and the nearest minimum.  
方法三：A third method based on an image pyramid that is as fast as gradient descent in most cases, but is more likely to find the global minimum within the allowed offset range.  
1. computing an image pyramid
Image pyramid for each grayscale image exposure, with log2(max_offset) levels past the base resolution.
2. 計算影像差異 = img1 XOR img2 AND mask
 