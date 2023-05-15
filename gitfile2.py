import os
import shutil
import time
from datetime import datetime
import subprocess
from git import Repo

    # Set the path to your Git repository
repo_path = r"\\ARB-NUC\olenrun"
    # Initialize the Git repository
repo = Repo(repo_path)
    # Set the author's identity for this repository
repo.git.config('user.email', 'abessen@quarryvision.com')
repo.git.config('user.name', 'abessen')

while True:
    # specify the file path as a string on your local machine
    file_path = r"\\ARB-NUC\QVisionDataFiles\Transfer\Reports\OlenData1\*.xlsx"
    
    # get the current date as a string in the same format as the file name
    current_date_str = datetime.now().strftime("%Y-%m-%d")

    # create a variable for the file extension
    file_extension = os.path.splitext(file_path)[1]

    # create a variable for the new file name, with the current date
    new_file_name = current_date_str + file_extension

    # create a variable for the new file path, with the modified file name
    wb_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

    # Set the local file path (within your Git repository) to a network path
    local_file_path = r"\\ARB-NUC\olenrun\NowData.xlsx"

    try:
        # Copy the file to the network GitHub repository
        shutil.copy(wb_file_path, local_file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}. File not found. Skipping this iteration.")
        continue
    except PermissionError as e:
        print(f"Error: {e}. Skipping file copy.")
        continue

    # Set the path to your Git repository
    repo_path = r"\\ARB-NUC\olenrun"

    # Initialize the Git repository
    repo = Repo(repo_path)

    try:
        # Check for changes in the repository
        status = repo.git.status()
    except Exception as e:
        if 'exit code(128)' in str(e):
            # Add an exception for the directory to the Git configuration
            subprocess.run(["git", "config", "--global", "--add", "safe.directory", f"%(prefix)//{repo_path}/"], check=True)
            # Retry the git status command
            status = repo.git.status()
        else:
            # If the exception wasn't due to exit code(128), raise it again
            raise

    if 'nothing to commit, working tree clean' not in status:
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
    time.sleep(30)
