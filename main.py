import os
import shutil
from threading import Thread

def move_files(direct, ext):
    if not os.path.exists(os.path.join(direct, ext)):
        os.makedirs(os.path.join(direct, ext))

    for name in os.listdir(direct):
        if name.endswith(ext) and not os.path.exists(os.path.join(direct, ext, name)):
            Thread(target=shutil.move, args=(os.path.join(direct, name), os.path.join(direct, ext, name))).start()

def process(direct):
    files = []
    for name in os.listdir(direct):
        if os.path.isdir(os.path.join(direct, name)):
            files.extend(process(os.path.join(direct, name)))
        else:
            files.append((direct, name))

    return files

def distribute(direct, files):
    for file_direct, name in files:
        ext = os.path.splitext(name)[1]
        Thread(target=move_files, args=(direct, ext)).start()
        if not os.path.exists(os.path.join(direct, ext, name)):
            Thread(target=shutil.move, args=(os.path.join(file_direct, name), os.path.join(direct, ext, name))).start()

def remove_folders(direct):
    for name in os.listdir(direct):
        if os.path.isdir(os.path.join(direct, name)):
            remove_folders(os.path.join(direct, name))
            if not os.listdir(os.path.join(direct, name)):
                os.rmdir(os.path.join(direct, name))

if __name__ == "__main__":
    files = process("G:\Garbage")
    distribute("G:\Garbage", files)
    remove_folders("G:\Garbage")
