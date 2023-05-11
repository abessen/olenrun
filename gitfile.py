import os
import shutil
from git import Repo
import time
from datetime import datetime

while True:
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

    # Set the local file path (within your Git repository)
    # local_file_path = "c:\\olenrun\\NowData.xlsx"
    local_file_path =r"\\ARB-NUC\olenrun\NowData.xlsx"


    try:
        # Copy the file to the local GitHub repository
        shutil.copy(wb_file_path, local_file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}. File not found. Skipping this iteration.")
        continue
    except PermissionError as e:
        print(f"Error: {e}. Skipping file copy.")
        continue

    # Set the path to your Git repository
    repo_path = "c:\\olenrun"

    # Initialize the Git repository
    repo = Repo(repo_path)

    # Check for changes in the repository
    if repo.is_dirty():
        # Stage the changes (add the new file to the staging area)
        repo.git.add(local_file_path)

        # Add all changes to the staging area
        repo.git.add(".")

        # Commit the changes
        repo.git.commit("-m", f"Add new file {new_file_name}")

        # Push the changes to the remote repository
        repo.git.pull()
        repo.git.push()
        print("changes detected, repository updated.")
    else:
        print("No changes detected in the repository.")

    # Pause the script for 60 seconds
    time.sleep(60)
