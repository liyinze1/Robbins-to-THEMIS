import os
import platform

if platform.system().lower() == 'windows':
    os.system('rmdir /s dataset\\deleted_images')
    os.system('rmdir /s dataset\\labels')
    os.system('rename dataset\\revised_labels labels')
else:
    os.system('rm -rf dataset/deleted_images')
    os.system('rm -rf dataset/labels')
    os.system('mv dataset/revised_labels dataset/labels')