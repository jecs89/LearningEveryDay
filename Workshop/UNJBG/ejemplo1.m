
im1 = imread('lenna.png',1);

%%RGB TO GRAYSCALE

%%LIGHTNESS (max(R, G, B) + min(R, G, B)) / 2
im2gray1 = zeros(size(im1,1),size(im1,2));
for i=1:size(im1,1)
	for j=2:size(im1,2)
		im2gray1(i,j) = (max(im1(i,j,1:3)) + min(im1(i,j,1:3)))/2;
	end
end

%%AVERAGE (R + G + B) / 3
im2gray2 = zeros(size(im1,1),size(im1,2));
for i=1:size(im1,1)
	for j=2:size(im1,2)
		im2gray2(i,j) = mean(im1(i,j,1:3));
	end
end

%%LUMINOSITY 0.21 R + 0.72 G + 0.07 B
im2gray3 = zeros(size(im1,1),size(im1,2));
for i=1:size(im1,1)
	for j=1:size(im1,2)
		im2gray3(i,j) = im1(i,j,1)*0.21 + im1(i,j,2)*0.71 + im1(i,j,3)*0.07;
	end
end

figure;
subplot(1,3,1)
imshow(mat2gray(im2gray1))
title('LIGHTNESS')
subplot(1,3,2)
imshow(mat2gray(im2gray2))
title('AVERAGE')
subplot(1,3,3)
imshow(mat2gray(im2gray3))
title('LUMINOSITY')

%%RGB TO GRAYSCALE
im2 = rgb2gray(im1);
figure;
imshow(im2)

%%RGB TO BINARY
im3 = im2bw(im1);
figure;
imshow(im3)