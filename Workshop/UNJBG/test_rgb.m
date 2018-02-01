im = imread('lenna.png');
emboss = [-2, -1,  0; 
	      -1,  1,  1;
	       0,  1,  2 ];
sobel = [-1., -2., -1.;
	 	 0.,  0.,  0.;
	 	 1.,  2.,  1. ];
sharpen =   [ -1.0, -1.0, -1.0;
	     	  -1.0,  9.0, -1.0;
	     	  -1.0, -1.0, -1.0 ];

new1 = 1/16*[1 2 1; 2 4 2; 1 2 1];

new2 = [0 1 0; 1 -4 1; 0 1 0]
 
[r, g, b] = rgbconv2(im, emboss);
imconv = cat(3, r,g,b);
imwrite(imconv,'LennaEmboss.png');

[r, g, b] = rgbconv2(im, sobel);
imconv = cat(3, r,g,b);
imwrite(imconv,'LennaSobel.png');

[r, g, b] = rgbconv2(im, sharpen);
imconv = cat(3, r,g,b);
imwrite(imconv,'LennaSharpen.png');

[r, g, b] = rgbconv2(im, new2);
imconv = cat(3, r,g,b);
imwrite(imconv,'LennaNew2.png');