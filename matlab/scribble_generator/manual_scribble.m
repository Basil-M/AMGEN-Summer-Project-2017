function [ scribbles ] = manual_scribble( scan, mask_gt,varargin)
%Manual scribbles


%Inputs
erode = true;
if nargin > 2; patient_num = varargin{1}(1); else; patient_num = -1; end
if nargin > 3; frame_num = varargin{2}(1); else; frame_num = -1; end
if nargin > 4; erode = false; mask_scribble = varargin{3}(1); end;

%Text for title
p_text = ['Patient ' num2str(patient_num, '%03.f') ' frame ' num2str(frame_num, '%03.f') ' slice '];

%Get scribbles via erosion
erosion_scribble = generateScribbles(mask_gt.vol, 'SliceOrientation', 3, ...
    'ErosionRadii', [0 6 2 14], ...
    'Debug', 0 ...
    );

if erode
    original_scribble = erosion_scribble;
    mask_scribble = mask_gt;
    mask_scribble.vol = erosion_scribble;
else
    original_scribble = mask_scribble.vol;
end

%initialise variables
new_vals = original_scribble;
slice_count = size(mask_gt.vol,3);
labels = unique(mask_gt.vol);
sliceNo = 1;
go_to_previous_slice = false;
lab_idx = 2;

while sliceNo <= slice_count
    if go_to_previous_slice; sliceNo = sliceNo - 2; lab_idx = 4;go_to_previous_slice = false; end
    
    %Prevent going back to slice that doesn't exist
    if sliceNo < 1; sliceNo = 1; end;
    h = figure(1);
    set(gcf,'units','normalized','outerposition',[0 0.5 1 0.5]);
    
    %Label, for instructions
    mTextBox = uicontrol('style','text');
    set(mTextBox,'Units','Characters','HorizontalAlignment','Left');
    set(h,'Units','Characters');
    %graph_dims = get(h,'Position');
    set(mTextBox,'String',{'d for next slice'; ...
                           'a for previous slice'; ...
                           'w to create new scribble'; ...
                           'e to reset to erosion scribble';...
                           'r to reset to loaded scribble';});
    t_dims = get(mTextBox,'Position');
    set(mTextBox,'Position',[t_dims(1), t_dims(2), 25, 4]);
    
    %Show actual scan
    subplot(131);
    imshow(scan.vol(:,:,sliceNo), [0 255]);
    title([p_text num2str(sliceNo)]);
    
    ground_truth = mask_gt.vol(:,:,sliceNo);
    while lab_idx < 5
        if lab_idx < 2; go_to_previous_slice = true; lab_idx = 4; end
        
        if ~go_to_previous_slice 
            label_num = labels(lab_idx);
            
            %get grayscale of ground truth
            grayscale = (ground_truth == 1)*40 + (ground_truth == 2)*80 + (ground_truth == 3) * 120;
            
            %initialise RGB matrix
            rgb = zeros([size(grayscale) 3]);
            for i = 1:3; rgb(:,:,i) = grayscale/255; end
            grayscale = rgb;

            %current ground truth label appears red
            rgb(:,:,1) = rgb(:,:,1) + (ground_truth == label_num);
            
            %SHOW GROUND TRUTH
            subplot(132);
            imshow(rgb,[0,1]);
            title('GROUND TRUTH');

            %SHOW SCRIBBLE PLOT
            subplot(133);
            
            %faint background of scan
            for i = 1:3; grayscale(:,:,i) = 0.3*scan.vol(:,:,sliceNo)/255; end;
            
            %Make current scribble 
            grayscale(:, :, 3) =  grayscale(:,:,3)+ (new_vals(:,:,sliceNo) == label_num);
            imshow(grayscale,[0,1]);
            title('SCRIBBLE');

            
            %keyboard control
            while waitforbuttonpress == 0; k_press = ' '; end;
            k_press = h.CurrentCharacter;            
            
            while (k_press ~= 'd') && (k_press~='a') && (k_press~='w') && (k_press~='r') && (k_press~='e')
                while waitforbuttonpress == 0; k_press = ' '; end;
                k_press = h.CurrentCharacter
            end
            
            %GO PREVIOUS IMAGE
            if k_press == 'a'
                lab_idx = lab_idx -2;
                
            %GET USER INPUT
            elseif k_press == 'w'
                %Getting input from user
                set(mTextBox,'string',{sprintf('SCRIBBLING ON LABEL %s',num2str(label_num));...
                                       'Pick up to ten points';...
                                       'Hit Enter/Return to finish selecting points'})
                %Get new mask
                [x,y] = ginput(10);
                x(x>size(grayscale,2)) = size(grayscale,2); x(x<1)=1;
                y(y>size(grayscale,1)) = size(grayscale,1); y(y<1)=1;
                new_mask = generate_scribble_stroke(x,y,size(grayscale,1),size(grayscale,2),2);
                
                
                old_mask = new_vals(:,:,sliceNo);                       
                old_mask((old_mask == label_num)) = 0;                  %Remove old mask for this label
                %old_mask((old_mask == 0)&(new_mask~=0)) = label_num;    %Where there are no allocated pixels, insert new mask
                old_mask((new_mask~=0)) = label_num;    %Where there are no allocated pixels, insert new mask
                new_vals(:,:,sliceNo) = old_mask;
                
                %Bring back standard label
                set(mTextBox,'String',{'d for next slice'; ...
                                       'a for previous slice'; ...
                                       'w to create new scribble'; ...
                                       'e to reset to erosion scribble';...
                                       'r to reset to loaded scribble';});
                lab_idx = lab_idx - 1;
                
            %RESET TO EROSION SCRIBBLE
            elseif k_press == 'e'
                %Reset to erosion scribble
                old_mask = new_vals(:,:,sliceNo);
                old_mask(old_mask == label_num) = 0;
                old_mask((erosion_scribble(:,:,sliceNo) == label_num)) = label_num;
                new_vals(:,:,sliceNo) = old_mask;
                lab_idx = lab_idx - 1;
            %RESET TO LOADED SCRIBBLE
            elseif k_press == 'r'
                old_mask = new_vals(:,:,sliceNo);
                old_mask(old_mask == label_num) = 0;
                old_mask((original_scribble(:,:,sliceNo) == label_num)) = label_num;
                new_vals(:,:,sliceNo) = old_mask;
                lab_idx = lab_idx - 1;
            end

            lab_idx = lab_idx + 1;
        else
            lab_idx = 5;
        end;
    end
    lab_idx = 2;
    sliceNo = sliceNo + 1;
    clf;
    
end
close all;
new_vals(new_vals < 0) = 0;
scan.vol = new_vals;
scribbles = scan;
end