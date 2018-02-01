%Example of reading, writing and manipulation of images
im1 = imread('lenna.png');
size(im1)
im2 = im1(1:100,1:50);
imwrite(im2,'lenna_segmented.png')

hist = zeros(256,3);
size(hist)

for i=1:size(im1,1)
	for j=1:size(im1,2)
		for k=1:3
			hist(im1(i,j,k),k) = hist(im1(i,j,k)) + 1;
		end
	end
end

mx = max([max(hist(:,1)) max(hist(:,2)) max(hist(:,3))])

figure;
subplot(1,3,1)
plot(hist(:,1),'r');
axis([0 300,0 mx])
subplot(1,3,2)
plot(hist(:,2),'g');
axis([0 300,0 mx])
subplot(1,3,3)
plot(hist(:,3),'b');
axis([0 300,0 mx])