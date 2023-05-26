import os
import shutil
import time
from datetime import datetime
from git import Repo
from git.exc import GitCommandError

# Set the path to your Git repository
repo_path = r"\\ARB-NUC\olenrun"

# Initialize the Git repository
repo = Repo(repo_path)

# Set the author's identity for this repository
repo.git.config('user.email', 'abessen@quarryvision.com')
repo.git.config('user.name', 'abessen')

while True:
    # Get the current date as a string in the same format as the file name
    current_date_str = datetime.now().strftime("%Y-%m-%d")

    # Create a variable for the new file path, with the modified file name
    wb_file_path = r"\\ARB-NUC\QVisionDataFiles\Transfer\Reports\OlenData1\\" + current_date_str + ".xlsx"

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

    try:
        # Check for changes in the repository
        status = repo.git.status()

        if 'nothing to commit, working tree clean' not in status:
            # Stage the changes (add the new file to the staging area)
            repo.git.add(local_file_path)

            # Commit the changes
            repo.git.commit("-m", f"Add new file {current_date_str}.xlsx")

            # Pull the latest changes and push the new changes to the remote repository
            repo.git.pull()
            repo.git.push()
            print("Changes detected, repository updated.")
        else:
            print("No changes detected in the repository.")
    except GitCommandError as e:
        print(f"Error: {e}. Git operation failed.")
    
    # Pause the script for 30 seconds
    time.sleep(30)
