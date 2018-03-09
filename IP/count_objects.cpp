#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"

#include <iostream>

using namespace cv;
using namespace std;

Mat src,gray,dst,bin,cnv,mbord;
int threshold_slider,threshold_slider1;

Mat joint, segmented;

void my_contours();

static void on_trackbar( int, void* )
{
    dst.copyTo(segmented);
    dst.copyTo(bin);

	//threshold(dst,bin,threshold_slider,255,ADAPTIVE_THRESH_GAUSSIAN_C);

    for( int i = 1; i < (dst.rows - 1); i++ ){
      for( int j = 1; j < (dst.cols - 1); j++ ){
        if( dst.at<uchar>(i,j) < threshold_slider || dst.at<uchar>(i,j) > threshold_slider1 ){
            bin.at<uchar>(i,j) = 0;
        }
        else{
            bin.at<uchar>(i,j) = 255;    
        }
      }
    }

    // for(int i = 0; i < src.rows; i++){
    // 	for(int j = 0; j < src.cols; j++){
    // 		segmented.at<uchar>(i,j) = 0;
    // 	}
    // }

    for(int i = 0; i < src.rows; i++){
    	for(int j = 0; j < src.cols; j++){
    		if(bin.at<uchar>(i,j) == 0){
    			segmented.at<uchar>(i,j) = 0;
    		}
    	}
    }

    // // hconcat(segmented, dst, joint); // horizontal
    // // imshow( "Processing", joint );

    // segmented.copyTo(dst);
    
    imshow( "Threshold_Mask", bin );
    imshow( "Processing", segmented );
    // cout << threshold_slider << endl;

    my_contours();
}

/*
* The algorithm is by Werner D. Streidt
* (http://visca.com/ffactory/archives/5-99/msg00021.html)
*/

// int _brightness = 100;
// int _contrast = 100;

// static void updateBrightnessContrast( int /*arg*/, void* )
// {
//     // int brightness = _brightness - 100;
//     // int contrast = _contrast - 100;
    
//     double a, b;
//     if( _contrast > 0 )
//     {
//       double delta = 127.*_contrast/100;
//       a = 255./(255. - delta*2);
//       b = a*(_brightness - delta);
//     }
//     else
//     {
//       double delta = -128.*_contrast/100;
//       a = (256.-delta*2)/255.;
//       b = a*_brightness + delta;
//     }

//     src.convertTo(dst, CV_8U, a, b);
//     imshow("Processing", dst);
// }

void my_filter(){

    int kernel_size, ind = 0;

    Point anchor;
    double delta;
    int ddepth;

    /// Initialize arguments for the filter
    anchor = Point( -1, -1 );
    delta = 0;
    ddepth = -1;

    kernel_size = 3 + 2*( ind%5 );

    float k[9] = { -1.0, 0.0, 1.0,
             -2.0, 2.0, 2.0,
             -1.0, 0.0, 1.0};

    Mat kernel(kernel_size,kernel_size,CV_32F,k);

    filter2D(dst, cnv, ddepth , kernel, anchor, delta, BORDER_DEFAULT );
}

RNG rng(12345);
int thresh = 100;

void my_contours(){

    segmented.copyTo(mbord);
    Mat threshold_output;
    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;

    blur( mbord, mbord, Size(3,3) );

    /// Detect edges using Threshold
    threshold( mbord, threshold_output, thresh, 255, THRESH_BINARY );
    /// Find contours
    findContours( threshold_output, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

    /// Find the rotated rectangles and ellipses for each contour
    vector<RotatedRect> minRect( contours.size() );
    vector<RotatedRect> minEllipse( contours.size() );

    for( int i = 0; i < contours.size(); i++ )
       { minRect[i] = minAreaRect( Mat(contours[i]) );
         if( contours[i].size() > 5 )
         { minEllipse[i] = fitEllipse( Mat(contours[i]) ); }
       }

    /// Draw contours + rotated rects + ellipses
    Mat drawing = Mat::zeros( threshold_output.size(), CV_8UC3 );
    for( int i = 0; i< contours.size(); i++ ){
        //BGR
         Scalar color = Scalar( 0,255,0 );
         // contour
         drawContours( src, contours, i, color, 1, 8, vector<Vec4i>(), 0, Point() );
         // ellipse
         ellipse( src, minEllipse[i], color, 2, 8 );
         // rotated rectangle
         Point2f rect_points[4]; minRect[i].points( rect_points );
         for( int j = 0; j < 4; j++ )
          line( src, rect_points[j], rect_points[(j+1)%4], color, 1, 8 );
       }

    /// Show in a window

   
    imshow( "Contours", src );
}


int main(int argc, char const *argv[]){

	src = imread(argv[1], CV_LOAD_IMAGE_COLOR); // reads image from file

	cvtColor(src,dst,CV_BGR2GRAY);  // converts image from rgb(src) to gray level (dst) 
	dst.copyTo(segmented);
    dst.copyTo(cnv);
    dst.copyTo(gray);

	threshold_slider = 90;
    threshold_slider1 = 100;

    my_filter();

    namedWindow("Original",CV_WINDOW_NORMAL); imshow("Original",dst);
    namedWindow("Filt",CV_WINDOW_NORMAL); imshow("Filt",cnv);

	namedWindow("Processing",CV_WINDOW_NORMAL);
    namedWindow("Threshold_Mask",CV_WINDOW_NORMAL);

    namedWindow( "Contours", CV_WINDOW_NORMAL );

	
    // createTrackbar( "brightness", "Processing", &_brightness, 200, updateBrightnessContrast );
	// createTrackbar( "contrast", "Processing", &_contrast, 256, updateBrightnessContrast );
	createTrackbar( "Threshold", "Processing", &threshold_slider, 256, on_trackbar );
    createTrackbar( "Threshold1", "Processing", &threshold_slider1, 256, on_trackbar );

	// updateBrightnessContrast(0,0);
	on_trackbar( threshold_slider, 0 );

    cout << "Run\n";

    waitKey(0);

	return 0;
}