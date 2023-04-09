import os
import shutil

#List files in directory
def list_files(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            if ".DS_Store" not in filename:
                file_list.append(os.path.join(root, filename))
    return file_list

#Move files to a designated folder
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False

#Put files back after testing and delete cached files
def put_files_back(dataset_path, all_images_dir, all_labels_dir):
    os.chdir(dataset_path)
    image_files = list_files("images")
    label_files = list_files("labels")

    cache_files = [file_ for file_ in label_files if "cache" in file_]
    if cache_files:
        cache_files_path = [dataset_path + file_ for file_ in cache_files]
        [os.remove(cache_file) for cache_file in cache_files_path]
        label_files = list_files("labels")

    move_files_to_folder(image_files, all_images_dir)
    move_files_to_folder(label_files, all_labels_dir)

#Delete all files in a directory
def delete_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))
