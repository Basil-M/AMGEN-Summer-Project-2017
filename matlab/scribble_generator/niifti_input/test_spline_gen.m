test_img =rand([500,500]);
imshow(test_img);
[test_x,test_y] = ginput(6);

new_img = generate_scribble_stroke(test_x,test_y,500,500);
imshow(new_img);
