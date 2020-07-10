import os
from pathlib import Path

SUBDIRECTORIES = {
    "DOCUMENTS": ['.pdf', '.rtf', '.txt', '.py'],
    "AUDIO": ['.m4a', '.m4b', '.mp3'],
    "VIDEOS": ['.mov', '.avi', '.mp4'],
    "IMAGES": ['.jpg', '.jpeg', '.png']
}


# picking from the subdirectory category based on the file type that we pass as argument
def pickDirectoryValue(value):
    for category, suffixes in SUBDIRECTORIES.items():
        for suffix in suffixes:
            if suffix == value:
                return category
    return 'MISC'


print(pickDirectoryValue('.pdf'))


def organizeDirectory():
    for item in os.scandir():  # with the OS library function scandir. scandir will grab every object in our folder
        if item.is_dir():
            continue
        file_path = Path(item)  # To get the path of each item, using Path function from the pathlib library
        # print(file_path)
        file_type = file_path.suffix.lower()  # Getting the file type from the path
        directory = pickDirectoryValue(file_type)
        directory_path = Path(directory)
        # print(directory_path)
        file_path.rename(directory_path.joinpath(file_path))


organizeDirectory()
