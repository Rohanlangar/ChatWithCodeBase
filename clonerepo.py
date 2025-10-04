import os
from git import Repo
import shutil
import stat

def handle_remove_readonly(func, path, exc):
    """Error handler for Windows readonly files"""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_repository(repo_url, clone_path="cloned_repo"):
    if os.path.exists(clone_path):
        print(f"Directory {clone_path} already exists. Removing it.")
        # Use onerror for Windows compatibility
        shutil.rmtree(clone_path, onerror=handle_remove_readonly)

    Repo.clone_from(repo_url, clone_path)
    print(f"Repository cloned to {clone_path}")
    return clone_path