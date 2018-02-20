#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"

#include <iostream>

using namespace cv;
using namespace std;

Mat src,dst,bin;
int threshold_slider;

Mat joint, segmented;

static void on_trackbar( int, void* )
{
	threshold(dst,bin,threshold_slider,255,THRESH_BINARY);

    for(int i = 0; i < src.rows; i++){
    	for(int j = 0; j < src.cols; j++){
    		segmented.at<uchar>(i,j) = 0;
    	}
    }

    for(int i = 0; i < src.rows; i++){
    	for(int j = 0; j < src.cols; j++){
    		if(bin.at<uchar>(i,j) == 0){
    			segmented.at<uchar>(i,j) = dst.at<uchar>(i,j);
    		}
    	}
    }

    hconcat(segmented, dst, joint); // horizontal

    imshow( "Test", joint );
    cout << threshold_slider << endl;
}

int main(int argc, char const *argv[])
{
	src = imread(argv[1], CV_LOAD_IMAGE_COLOR); // reads image from file
	// src.copyTo(segmented);

	cvtColor(src,dst,CV_BGR2GRAY);  // converts image from rgb(src) to gray level (dst) 
	dst.copyTo(segmented);

	threshold_slider = 0;

	namedWindow("Test",CV_WINDOW_NORMAL);
	createTrackbar( "Threshold", "Test", &threshold_slider, 256, on_trackbar );

	on_trackbar( threshold_slider, 0 );
	
    // createTrackbar("brightness", "image", &_brightness, 200, updateBrightnessContrast);
    // createTrackbar("contrast", "image", &_contrast, 200, updateBrightnessContrast);


    waitKey(0);

	return 0;
}