from pathlib import Path


def remove_directory(start_directory: Path):
    """Recursively and permanently removes the specified directory, all of its
    subdirectories, and every file contained in any of those folders."""
    for path in start_directory.iterdir():
        if path.is_file():
            if ".gitkeep" not in path.name:
                path.unlink()
        else:
            remove_directory(path)


def mkdir_directory(directory: Path):
    if not directory.exists():
        directory.mkdir()
