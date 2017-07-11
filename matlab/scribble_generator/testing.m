filepath = '/scratch/python/datasets/ACDC/ACDC_challenge_20170617/patient001';

nii_filename = 'patient001_frame01.nii.gz';

seg_filename = 'patient001_frame01_gt.nii.gz';

scrib_filename = 'patient001_frame01_scribble.nii.gz';

input_data = fullfile(filepath,seg_filename);

gt = MRIread(input_data);
go = gt;
%implement a loop to test different erosion radii
eR1 = 0;
eR2 = 6;
eR3 = 2;
eR4 = 18;
disp(sprintf('Eroding with radii %i %i %i %i',eR1,eR2,eR3,eR4));
erosionRadii = [eR1 eR2 eR3 eR4];
close all;
go.vol = generateScribbles_2(gt.vol, 'SliceOrientation', 3, ...
    'ErosionRadii', erosionRadii, ...
    'Debug', 1 ...
    );

%MRIwrite(go,fullfile(filepath,scrib_filename))
