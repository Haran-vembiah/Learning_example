import logging
import os
import pathlib
import shutil

logging.basicConfig(
    filename=r'C:\Users\vembiah-1\OneDrive - Mettler Toledo LLC\copy_contents_to_onedrive\copy_update_project_files.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')
src = r'C:\Users\vembiah-1\ProjectFiles'
dst = pathlib.Path(r"C:\Users\vembiah-1\OneDrive - Mettler Toledo LLC\ProjectFiles")


def copytree(src, dst, symlinks=False, ignore=None):
    # print('eneterd again')
    if not os.path.exists(dst):
        # print('Created dir:' + dst)
        logging.info('Created the directory:' + dst)
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        # print('Item is :'+ str(item))
        # print('source is:'+ str(s))
        # print('Dest is:'+ str(d))
        if os.path.isdir(s):
            # print("dir is:"+str(s))
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                # print('copied s: '+ s)
                # print('copied d: '+ d)
                logging.info('Got the updated copy of:' + item)
                shutil.copy2(s, d)


for folder in os.listdir(src):
    source = os.path.join(src, folder)
    dest = os.path.join(dst, folder)
    print(source)
    # print("For the folder: ", folder )
    copytree(source, dest)
print("Documents are updated with latest")
