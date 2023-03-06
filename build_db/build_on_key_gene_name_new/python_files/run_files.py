"""
Author: Tillman Heisner
Email: theisner@posteo.de

This calls different python scripts
"""
import subprocess
import shutil

if __name__ == '__main__':
    # List of files
    files = ["filter.py",
             "edit_exp_data.py",
             "edit_string_files.py"]
    # copy the needed files from original data to edited data
    exp_data_dir_path = "../original_data/exp_data/"
    functional_terms_dir_path = "../original_data/functional_terms_data/"
    edited_data_dir = "../edited_data/"
    # Use shutil.copy to copy some files
    functional_terms_data = ["KappaTerms.csv", "OverlapEdges.csv"]
    for file in functional_terms_data:
        shutil.copy(functional_terms_dir_path + file, edited_data_dir + file)
    # run the files
    for file in files:
        try:
            subprocess.run(["python3", file])
        except Exception as e:
            print(f"Failed to run file: {file}")
            raise SystemExit(e)
