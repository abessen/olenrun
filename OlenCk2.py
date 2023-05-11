import os
import shutil
from git import Repo
import time
from datetime import datetime


    # specify the file path as a string
   # file_path = r"C:\QVisionData\OneDrive\QuarryVisionDev\QVisionDataFiles\Transfer/Reports\OlenData1\*.xlsx"
   file_path = r"\\ARB-NUC\QVisionDataFiles\Transfer\Reports\OlenData1\*.xlsx"
    
    # get the current date as a string in the same format as the file name
    current_date_str = datetime.now().strftime("%Y-%m-%d")

    # create a variable for the file extension
    file_extension = os.path.splitext(file_path)[1]

    # create a variable for the new file name, with the current date
    new_file_name = current_date_str + file_extension

    # create a variable for the new file path, with the modified file name
    wb_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
    print(wb_file_path)