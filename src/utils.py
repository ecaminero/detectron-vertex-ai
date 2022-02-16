import os

TMP_FOLDER = "./tmp"

def create_tmp_folder():
    os.makedirs(TMP_FOLDER, exist_ok=True)

def get_img_name(path):
    return os.path.basename(path)