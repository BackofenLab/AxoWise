"""
Author: Tillman Heisner
Email: theisner@posteo.de

This calls different python scripts, which download and edit csvs.
"""
import subprocess

if __name__ == '__main__':
    # List of files
    files = ["get_string_files.py","edit_string_files.py",
             "edit_exp_data.py", "filter.py"]
    # run the files
    for file in files:
      try:
        subprocess.run(["python3",file])
      except:
        print(f"Failed to run file: {file}")