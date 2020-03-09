'''
    Author: Junzheng Wu
    Email: jwu220@uottawa.ca
    Organization: University of Ottawa (Silasi Lab)
    This script will update the recorded video onto google drive.
'''
from time import sleep
import time
from copy import copy
import os
import psutil
import sys
import ctypes


def copyLargeFile(src, dest, buffer_size=int(8*1e6)):
    '''
    This function will robustly copy large files.
    :param src:
    :param dest:
    :param buffer_size:
    :return:
    '''
    with open(src, 'rb') as fsrc:
        with open(dest, 'wb') as fdst:
            while 1:
                while not (work_in_free_time(1, 1, 0.6)):
                    print("\nBusy time, uploading paused.\n")
                    sleep(30)
                buf = fsrc.read(buffer_size)
                if not buf:
                    break
                fdst.write(buf)

def work_in_free_time(window_length=5, interval=3, threshold=0.6):
    '''
    Keep monitoring the usage of cpu, and only update the files in spare time.
    :param window_length:
    :param interval:
    :param threshold:
    :return:
    '''
    cpu_pct = 0
    for i in range(window_length):
        cpu_pct += psutil.cpu_percent()
        sleep(interval)
    cpu_pct_ave = cpu_pct/float(window_length)
    sys.stdout.write("\rCPU Usage: {} % ".format(cpu_pct_ave))
    sys.stdout.flush()
    if cpu_pct_ave < threshold * 100.:
        return True
    return False

def check_google_drive_status(path):
    return os.access(path, os.W_OK)


def check_safe_file(loacl_file_path):
    baseName = os.path.basename(loacl_file_path)
    rootdir = loacl_file_path.replace(baseName, '')
    created_time = os.path.getctime(loacl_file_path)
    modified_time = os.path.getmtime(loacl_file_path)
    if len(os.listdir(rootdir)) == 1:
        current_time = time.time() - 300
        if current_time < created_time or current_time < modified_time:
            return False
        else:
            return True
    else:
        flag_latest = True
        for item in os.listdir(rootdir):
            fullDir = os.path.join(rootdir, item)
            temp_created_time = os.path.getctime(fullDir)
            temp_modified_time = os.path.getmtime(fullDir)

            if temp_created_time > created_time or temp_modified_time > modified_time:
                flag_latest = False

        if flag_latest:
            current_time = time.time() - 3600
            if current_time < created_time or current_time < modified_time:
                return False
            else:
                return True
        else:
            return True



def googleDriveManager(interval=20, min_interval=10, cage_id=1, mice_n=4, gdrive_local=r"G:\Shared drives\SilasiLabGdrive"):

    ctypes.windll.kernel32.SetConsoleTitleW("BackupAuto Homecage-%d"%cage_id)
    gdrive_rootDir = os.path.join(gdrive_local, "homecage_%d_sync" % cage_id)


    gdrive_profilesDir = os.path.join(gdrive_rootDir, 'AnimalProfiles')
    check_dir_list = [gdrive_rootDir, gdrive_profilesDir]
    for i in range(1, mice_n + 1):
        check_dir_list.append(os.path.join(gdrive_profilesDir, "MOUSE" + str(i)))
        check_dir_list.append(os.path.join(gdrive_profilesDir, "MOUSE" + str(i), "Videos"))
        check_dir_list.append(os.path.join(gdrive_profilesDir, "MOUSE" + str(i), "Logs"))

    for dir_item in check_dir_list:
        if not os.path.exists(dir_item):
            try:
                os.mkdir(dir_item)
            except:
                raise (IOError, "Failed at making directories.")

    local_profileDir = ".." + os.path.sep + ".." + os.path.sep + "AnimalProfiles"

    while True:
        try:
            if work_in_free_time():
                n_video = 0
                uploading_list = []
                for i in range(1, mice_n + 1):
                    flag = False
                    video_root_dir = os.path.join(local_profileDir, 'MOUSE' + str(i), 'Videos')
                    logs_root_dir = os.path.join(local_profileDir, 'MOUSE' + str(i), 'Logs')
                    video_list = os.listdir(video_root_dir)
                    for file_item in video_list:
                        if file_item.endswith('.avi') and 'temp' not in os.path.basename(file_item):
                            full_path = os.path.join(video_root_dir, file_item)
                            # if os.path.getsize(full_path) < 18*1e6:
                            #     os.remove(full_path)
                            #     print("\n Small size File deleted: %s" % os.path.basename(full_path))
                            if check_safe_file(full_path):
                                uploading_list.append(full_path)
                                n_video += 1
                                flag = True
                    if flag:
                        for file_item in os.listdir(logs_root_dir):
                            if file_item.endswith('.csv') or file_item.endswith('.txt'):
                                uploading_list.append(os.path.join(logs_root_dir, file_item))
                                print("logs have beend added to uploading list.")

                for item in uploading_list:
                    print("\n==========================================================================================================================")
                    print("Number of files to upload: %d\n"%len(uploading_list))
                    upload_success = False
                    retry_count = 0
                    origin_dir = copy(item)

                    basename = item.replace(".." + os.path.sep + ".." + os.path.sep, '')

                    target_dir = os.path.join(gdrive_rootDir, basename)
                    print("Uploading--%s\n"%os.path.basename(target_dir))
                    while not upload_success:
                        try:
                            if origin_dir.endswith('.csv') or origin_dir.endswith('.txt'):
                                while is_locked(origin_dir):
                                    sleep(1)
                            copyLargeFile(origin_dir, target_dir)
                            sleep(min_interval)
                        except IOError as e:
                            print(e)
                            print("Failed, retry times: %d" % retry_count)
                            if os.path.exists(target_dir):
                                os.remove(target_dir)
                            sleep(min_interval)
                            retry_count += 1

                        if os.path.exists(target_dir):
                            size_origin = os.path.getsize(origin_dir)
                            size_target = os.path.getsize(target_dir)
                            if size_origin == size_target:
                                upload_success = True
                                print("\n\nFile uploaded as: %s successfully! \n" % target_dir)
                                if origin_dir.endswith('.avi'):
                                    os.remove(origin_dir)
                                    print("Original file:%s deleted." % origin_dir)
                                uploading_list.remove(item)
        except:
            raise (IOError, "Failed at making directories.")
        print("Current mission finished, Sleeping.....")
        sleep(interval)

def is_locked(filepath):
    """Checks if a file is locked by opening it in append mode.
    If no exception thrown, then the file is not locked.
    """
    locked = None
    file_object = None
    if os.path.exists(filepath):
        try:
            print("Trying to open %s." % filepath)
            buffer_size = 8
            # Opening file in append mode and read the first 8 characters.
            file_object = open(filepath, 'a', buffer_size)
            if file_object:
                print("%s is not locked." % filepath)
                locked = False
        except IOError as message:
            print("File is locked (unable to open in append mode). %s." % message)
            locked = True
        finally:
            if file_object:
                file_object.close()
                print("%s closed." % filepath)
    else:
        print("%s not found." % filepath)

    return locked

if __name__ == '__main__':
    cage_index = [item for item in os.getcwd().split(os.sep)
                  if 'homecagesinglepellet' in item.lower()][0].split('_')[-1]
    if cage_index.isdigit():
        cage_index = int(cage_index)
    else:
        cage_index = 1
    googleDriveManager(interval=300, min_interval=5, cage_id=cage_index, mice_n=5)