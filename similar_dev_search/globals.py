import logging
from pathlib import Path

logger = logging.getLogger(__name__)
repo_folder: Path
repo_info_folder: Path
results_folder: Path
enry_folder: Path


def setup(enry_folder_path: str = "../",
          repo_folder_path: str = "../repos",
          repo_info_path: str = "../repos_info",
          results_folder_path: str = "../results",
          ):
    global repo_folder, repo_info_folder, results_folder, enry_folder
    enry_folder = Path(enry_folder_path)
    if not enry_folder.exists():
        raise FileNotFoundError("Enry folder not found. Install enry for your os and specify path to the containing folder")
    repo_folder = Path(repo_folder_path)
    repo_folder.mkdir(parents=True, exist_ok=True)
    repo_info_folder = Path(repo_info_path)
    repo_info_folder.mkdir(parents=True, exist_ok=True)
    results_folder = Path(results_folder_path)
    results_folder.mkdir(parents=True, exist_ok=True)


setup()
