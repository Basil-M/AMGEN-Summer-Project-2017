folder_path = '/scratch/bmustafa/datasets/ACDC/ACDC_challenge_20170617/';

%INITIALISE LOOP
%CHECK LOG FILE
if exist(fullfile(folder_path,'log.txt'))
    done = csvread(fullfile(folder_path,'log.txt'));
    if length(done) > 0
        choice = questdlg(sprintf('Annotations recorded up to and including patient %03d frame %02d. Continue or start from scratch?', ...
                                  done(length(done),1), done(length(done),2)), 'Initialising...','Continue','Start over','Continue');
        switch choice
            case 'Continue'
                if length(done) > 1
                    if done(length(done) - 1, 1) == done(length(done), 1)
                        %Both frames for final patient were annotated
                        current_patient = done(length(done),1) + 1;
                        skip_frame = false;
                    else
                        current_patient = done(length(done),1);
                        skip_frame = true;
                    end
                else
                    current_patient = done(length(done),1);
                    skip_frame = true;
                end
            otherwise
                current_patient = 1;
                skip_frame = false;
        end
    else
        edit(fullfile(folder_path,'log.txt'));
        current_patient = 1;
        skip_frame = false;
    end
end

while current_patient <=100
    %FIND FILES IN CURRENT PATIENT FOLDER
    patient_path = [folder_path 'patient' num2str(current_patient,'%03d') '/'];
    current_files = dir([patient_path '*gt.nii.gz']);
    
    %skip frame if already done
    if skip_frame
        start_i = 2;
        skip_frame = false;
    else
        start_i = 1;
    end
    
    for i = start_i:numel(current_files)
        %get frame number
        current_frame = str2num(current_files(i).name(17:strfind(current_files(1).name,'_gt.nii.gz') - 1));
        
        %set filenames
        gt_filename = current_files(i).name;
        scan_filename = strrep(gt_filename,'_gt','');
        scrib_filename = strrep(gt_filename,'_gt','_scribble');
        
        %load MRIs
        input_gt = MRIread(fullfile(patient_path,gt_filename));
        input_scan = MRIread(fullfile(patient_path,scan_filename));
        
        if exist(fullfile(patient_path,scrib_filename)) == 2
            disp('Found previous scribble file');
            input_scribble = MRIread(fullfile(patient_path,scrib_filename));
            scribbled = freehand_scribble(input_scan,input_gt,current_patient,current_frame,input_scribble);
        else
            scribbled = freehand_scribble(input_scan,input_gt,current_patient,current_frame);
        end
        choice = questdlg(sprintf('Scribbling complete for patient %i frame %i - save?',current_patient,current_frame),'Save scribble','Yes','No','No');
        switch choice
            case 'Yes'
                MRIwrite(scribbled,fullfile(patient_path,scrib_filename));
                log_file = fopen(fullfile(folder_path,'log.txt'),'a');
                fprintf(log_file,'\n%d,%d',current_patient,current_frame);
                fclose(log_file)
            otherwise
                disp('Not saving');
        end
        clearvars scribbled input_scan input_gt
    end
    current_patient = current_patient + 1;
end