function [ spline_img ] = generate_scribble_stroke(x,y,width,height,brush_radius)

%Default value for brush_radius if not specified
if nargin == 4; brush_radius = 3; end

%Define sampling points
x_spline = []; y_spline = [];
for i = 1:numel(x) - 1
    x_spline = [x_spline; linspace(x(i),x(i+1),500)'];
    y_spline = [y_spline; linspace(y(i),y(i+1),500)'];
end
%Clip to fit matrix
x_spline(x_spline > width) = width; x_spline(x_spline < 0) = 0;
y_spline(y_spline > height) = height; y_spline(y_spline < 0) = 0;
x_spline = floor(x_spline); y_spline = floor(y_spline);

mask = zeros(width+2*brush_radius,height+2*brush_radius); %pad by brush radius amount
m = numel(x_spline);
size(mask)
for i = 1:m
    %taper edge
    s = min(floor(i/3),floor((m - i)/3));
    if s < brush_radius
        b_r = s;
        brush = strel('diamond',b_r).Neighborhood;
        
    else 
        b_r = brush_radius;
        if size(brush,1) ~= (2*brush_radius + 1); brush = strel('diamond',brush_radius).Neighborhood; end;
    end
    
    %coordinates of brush centre
    y_c = x_spline(i) + brush_radius; x_c =y_spline(i) + brush_radius;
    
    [x_c, y_c]
    mask((x_c - b_r):(x_c + b_r), (y_c - b_r):(y_c + b_r)) = mask((x_c - b_r):(x_c + b_r), (y_c - b_r):(y_c + b_r)) + brush;
end
mask = mask((brush_radius + 1):(width + brush_radius),(brush_radius + 1):(height + brush_radius));
spline_img = mask > 0; %rot90((mask > 0),3);
end