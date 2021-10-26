import shutil
from os import path
from zipfile import ZipFile

# Make a duplicate of an existing file

if path.exists("textfile.txt"):
    # Get  the path of the file in the current directory
    src = path.realpath("textfile.txt")

    # Let's make a backup copy by appending "bak" to the name
    dst = src + ".bak"

    # Copy over the permissions, modification times and other info
    shutil.copy(src, dst)
    shutil.copystat(src, dst)

    # rename the file
    # os.rename("textfile.txt", "newfile.txt")

    # put things into a zip archive
    root_dir, tail = path.split(src)
    print(str(root_dir))
    print(str(tail))
    shutil.make_archive("archived", "zip", root_dir)

    # more fie-grained control over zip files
    with ZipFile("testzip.zip", "w") as newzip:
        newzip.write("textfile.txt")
        newzip.write("textfile.txt.bak")
