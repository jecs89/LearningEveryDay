function [r, g, b] = rgbconv2(a, c)
    r = im2uint8(mat2gray(conv2(a(:,:,1), c)));
    g = im2uint8(mat2gray(conv2(a(:,:,2), c)));
    b = im2uint8(mat2gray(conv2(a(:,:,3), c)));
endfunction