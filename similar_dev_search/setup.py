import logging
from pathlib import Path

logger = logging.getLogger(__name__)
repo_folder: Path
enry_folder: Path


def setup(enry_folder_path: str = "../", repo_folder_path: str = "../repos", ):
    """
    Create folder to save cloned repos. Specify enry folder
    :param enry_folder_path: enry executable should be inside this folder
    :param repo_folder_path: folder should be accessible for writing and reading
    """
    global repo_folder, enry_folder
    enry_folder = Path(enry_folder_path)
    if not enry_folder.exists():
        raise FileNotFoundError("Enry folder not found. Install enry for your os "
                                "and specify path to the containing folder")
    repo_folder = Path(repo_folder_path)
    repo_folder.mkdir(parents=True, exist_ok=True)


setup()
