import os
from git import Repo
import shutil

def clone_repository(repo_url, clone_path="cloned_repo"):
    if os.path.exists(clone_path):
        print(f"Directory {clone_path} already exists. Removing it.")
        shutil.rmtree(clone_path)

    Repo.clone_from(repo_url, clone_path)
    print(f"Repository cloned to {clone_path}")
    return clone_path