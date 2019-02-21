#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
//#include "opencv2/tracking.hpp"
#include "opencv2/opencv.hpp"

#include <iostream>
#include <fstream>
#include <string>

using namespace cv;
using namespace std;

int main(int argc, char const *argv[]){
    //Mat src = imread(argv[1], CV_LOAD_IMAGE_COLOR); // reads image from file
    Mat src= Mat::zeros(400,500, CV_8UC1);
    ifstream infile("thefile.txt");

    string a = ""; int count = 0;

	while (infile >> a){
	    //cout << a << endl;
	    for( int i = 0 ; i < a.length(); i++){
	    	src.at<uchar>(int(count/src.cols), int(count%src.cols)) = 255 - a[i];
	    	//cout << int(count%src.cols) << " " << int(count/src.cols) << endl;
	    	//cout << a[i] << " ";
	    }
	    //cout << endl;
	    count++;
	}
	cout << "count " << count << endl;

    imwrite( "result.png", src);

    namedWindow("Test",CV_WINDOW_NORMAL);
    imshow( "Test", src);

    waitKey(0);

 	return 0;
}