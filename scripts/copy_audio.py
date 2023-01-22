# file to copy audio files to separate single folders, one per sub experiment

import shutil
from pathlib import Path

def main():
    experiments = ['A', 'B', 'C', 'D']

    exps_dict = [
        {
            "exp_name": 'A',
            "target_speaker": "Idan",
            "filler_speaker": "Nezar",
            "target_accented": True
        },
        {
            "exp_name": 'B',
            "target_speaker": "Idan",
            "filler_speaker": "Nezar",
            "target_accented": False
        },
        {
            "exp_name": 'C',
            "target_speaker": "Nezar",
            "filler_speaker": "Idan",
            "target_accented": True
        },
        {
            "exp_name": 'D',
            "target_speaker": "Nezar",
            "filler_speaker": "Idan",
            "target_accented": False
        }
    ]
    
    for exp in exps_dict:
        #copy_files(exp)

def copy_files(exp):
    exp_name = exp["exp_name"]
    print('\nCopying files for experiment ' + exp_name)

    destination_folder_path = Path("exp-" + exp_name + "/")

    copy_target_files(exp, destination_folder_path)
    copy_filler_files(exp, destination_folder_path)    

def copy_target_files(exp, destination_folder_path):
    print("\nCopying target files for experiment " + exp["exp_name"])

    if (exp["target_accented"]):
        subfolder_name = "_foreign/"
        file_suffix = "_foreign"
    else:
        subfolder_name = "_eng/"
        file_suffix = "_eng"

    target_speaker = exp["target_speaker"]
    
    src_folder_path = Path("audio/" + target_speaker + subfolder_name + target_speaker + "_implaus/" )
    # print("\nTarget folder path is: " + str(src_folder_path))

    for i in range(1,21):
        if (i % 2 == 0):
            # copy even PO files
            alternation = "PO"
        else:
            # copy odd DO files
            alternation = "DO"

        if i < 10:
            filler_index = "0" + str(i)
        else:
            filler_index = str(i)

        src_file_name = target_speaker + "_" + filler_index + "_" + alternation + "implaus" + file_suffix + ".wav"
        # print("\nTarget file name: " + src_file_name)

        src_file_path = src_folder_path / src_file_name

        shutil.copy(src_file_path, destination_folder_path)

def copy_filler_files(exp, destination_folder_path):
    print("\nCopying filler files for experiment " + exp["exp_name"])

    filler_speaker_name = exp["filler_speaker"]

    filler_folder_path = Path("audio/" + filler_speaker_name + "_eng/" + filler_speaker_name + "_eng_fillers/")
    
    for i in range(1,61):
        if i < 10:
            filler_index = "0" + str(i)
        else:
            filler_index = str(i)
            
        src_file_name = filler_speaker_name + "_" + filler_index + "_filler_eng.wav"
        src_file_path = filler_folder_path / src_file_name 
        #print('\nSrc file name: ' + src_file_name)
        #print('\nSrc file path: ' + str(src_file_path))
        
        shutil.copy(src_file_path, destination_folder_path)
    
if __name__ == "__main__":
    main()
