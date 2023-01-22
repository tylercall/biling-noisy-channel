# file to generate a conditions file per sub experiment

import shutil
from pathlib import Path
import csv
from operator import itemgetter

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
        rows_to_write = generate_conditions_rows(exp)
        write_conditions_file(exp["exp_name"], rows_to_write)



def generate_conditions_rows(exp):
    sub_exp = exp["exp_name"]
    print('\nGenerating conditions file for exp-' + sub_exp + "\n\n")

    # get list of files for this sub-exp
    files_list = []        
    for file in Path("exp-" + sub_exp + "/").glob('**/*.wav'):
        filename = str(file).split('/')[1]
        files_list.append(filename)
    #print("files_list length is: " + str(len(files_list)))

    # get filler text file contents in list form for searching
    filler_text_file = open("base-fillers2.txt", 'r')
    filler_content = filler_text_file.readlines()
    filler_text_file.close()
    # clean content (strip whitespace)
    filler_content_stripped = []
    for i in filler_content:
        filler_content_stripped.append(i.strip())
    
    # get dopo text file contents in list form for searching
    dopo_text_file = open("dopo-to.txt", 'r')
    dopo_content = dopo_text_file.readlines()
    dopo_text_file.close()
    # clean content (strip whitespace)
    dopo_content_stripped = []
    for i in dopo_content:
        dopo_content_stripped.append(i.strip())
    
    # loop through all files in exp folder; get filename and make list of filenames

    rows_to_write = []
        
    for filename in files_list:
        filename_split = filename.split('_')
        item_number_leading_zero_str = filename_split[1]
        item_number = int(item_number_leading_zero_str)
        category = filename_split[2]

        if category == "filler":
            trial_key = "filler_" + item_number_leading_zero_str
            file_to_search = filler_content_stripped
            lookup_string = "# filler " + str(item_number) + " filler"
        else:
            category_sub = category[0:2]
            if exp["target_accented"]:
                trial_key_suffix = "_foreign"
            else:
                trial_key_suffix = "_eng"
            trial_key = "target_" + category_sub + "_" + item_number_leading_zero_str + trial_key_suffix
            file_to_search = dopo_content_stripped
            lookup_string = "# dopo " + str(item_number) + " " + category_sub + "_implausible"

        index_of_lookup = file_to_search.index(lookup_string)
        if index_of_lookup < 0:
            print("\n\n\nCould not find the string! This is bad\n\n\n")
            # this can't actually happen; it will throw an exception
        else:
            index_of_question_line = index_of_lookup + 2
            question_line = file_to_search[index_of_question_line]
        
        # print('trial_key: ' + trial_key)
        # print('filename: ' + filename)
        # print('question line: ' + question_line)

        # parse question info and get question and correct answer        

        question = question_line[2:-3].strip()
        # print(question)
        correct_answer = question_line[-3:].strip()
        correct_answer_coded = correct_answer[0].lower()
        # print(correct_answer)

        # make a new dictionary, append value to rows_to_write
        row_as_dict = {
            "trial_key": trial_key,
            "audio_file_name": "resources/" + filename,
            "question_text": question,
            "correct_response": correct_answer_coded
        }

        rows_to_write.append(row_as_dict)

        # sort row alphabetically by key
        rows_sorted = sorted(rows_to_write, key=itemgetter('trial_key'))
    return rows_sorted

def write_conditions_file(sub_exp_name, rows):
    path_to_new_folder = Path("exp-" + sub_exp_name)
    file_name = "conditions_noisy_" + sub_exp_name + ".csv"
    full_file_path = path_to_new_folder / file_name

    field_names = ["trial_key", "audio_file_name", "question_text", "correct_response"]

    with open(full_file_path, 'w') as conditions_csv:
        writer = csv.DictWriter(conditions_csv, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(rows)             
    
if __name__ == "__main__":
    main()
