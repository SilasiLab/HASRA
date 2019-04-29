from time import sleep
import time
import datetime
import shutil
from copy import copy
import os
import psutil
import subprocess
from multiprocessing import Process

def copyLargeFile(src, dest, buffer_size=16000):
    with open(src, 'rb') as fsrc:
        with open(dest, 'wb') as fdst:
            while 1:
                while not (work_in_free_time(1, 1, 0.4)):
                    print("Busy time, uploading paused.")
                    sleep(60)
                buf = fsrc.read(buffer_size)
                if not buf:
                    break
                fdst.write(buf)

def work_in_free_time(window_length=5, interval=3, threshold=0.3):
    cpu_pct = 0
    for i in range(window_length):
        cpu_pct += psutil.cpu_percent()
        sleep(interval)
    cpu_pct_ave = cpu_pct/float(window_length)
    print("cpu usage :%.4f" % cpu_pct_ave)
    if cpu_pct_ave < threshold * 100.:
        return True
    return False

def check_google_drive_status(path):
    return os.access(path, os.W_OK)

def self_recover(path, rlone_name):
    command_unmount = (['fusermount -u %s' % path])
    command_mount = (['rclone mount %s: %s -v --max-read-ahead 2000m --allow-non-empty' % (rlone_name, path)])
    result = subprocess.Popen(command_unmount, shell=True)
    result.communicate()
    result = subprocess.Popen(command_mount, shell=True)
    result.communicate()

def self_recover_backend(gdrive_local,gdrive_rclone, p):
    p.terminate()
    print("rlone restarting...")
    p = Process(target=self_recover, args=[gdrive_local, gdrive_rclone], name="manager")
    p.start()
    print("rclone restated.")
    return p

def check_safe_file(loacl_file_path):
    baseName = os.path.basename(loacl_file_path)
    rootdir = loacl_file_path.replace(baseName, '')
    created_time = os.path.getctime(loacl_file_path)
    modified_time = os.path.getmtime(loacl_file_path)
    if len(os.listdir(rootdir)) == 1:
        current_time = time.time() - 3600
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



def googleDriveManager(interval=20, min_interval=10, cage_id=85136, mice_n=4, gdrive_local="/mnt/googleTeamDrive/", gdrive_rclone='silasi_team_drive'):
    gdrive = os.path.join(gdrive_local, "HomeCages/")
    p = Process(target=self_recover, args=[gdrive_local, gdrive_rclone])
    p.start()
    status = check_google_drive_status(gdrive)
    if not status:
        p = self_recover_backend(gdrive_local, gdrive_rclone, p)
    gdrive_rootDir = os.path.join(gdrive_local, "HomeCages/", "cage_"+str(cage_id))
    gdrive_profilesDir = os.path.join(gdrive_rootDir, 'AnimalProfiles')
    check_dir_list = [gdrive, gdrive_rootDir, gdrive_profilesDir]
    for i in range(1, mice_n + 1):
        check_dir_list.append(os.path.join(gdrive_profilesDir, "MOUSE" + str(i)))
        check_dir_list.append(os.path.join(gdrive_profilesDir, "MOUSE" + str(i), "Videos"))
        check_dir_list.append(os.path.join(gdrive_profilesDir, "MOUSE" + str(i), "Logs"))
        check_dir_list.append(os.path.join(gdrive_profilesDir, "MOUSE" + str(i), "Analyses"))
        check_dir_list.append(os.path.join(gdrive_profilesDir, "MOUSE" + str(i), "Temp"))

    for dir_item in check_dir_list:
        if not os.path.exists(dir_item):
            try:
                os.mkdir(dir_item)
            except:
                p = self_recover_backend(gdrive_local, gdrive_rclone, p)
    local_profileDir = "../../AnimalProfiles/"

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
                        if file_item.endswith('.avi'):
                            if check_safe_file(os.path.join(video_root_dir, file_item)):
                                uploading_list.append(os.path.join(video_root_dir, file_item))
                                n_video += 1
                                flag = True
                    if flag:
                        for file_item in os.listdir(logs_root_dir):
                            if file_item.endswith('.csv'):
                                uploading_list.append(os.path.join(logs_root_dir, file_item))

                for item in uploading_list:
                    upload_success = False
                    retry_count = 0
                    origin_dir = copy(item)
                    basename = item.replace('../../', '')
                    target_dir = os.path.join(gdrive_rootDir, basename)

                    while not upload_success:
                        # sleep(min_interval)
                        #
                        # size1 = os.path.getsize(origin_dir)
                        # sleep(2. * min_interval)
                        # size2 = os.path.getsize(origin_dir)
                        # if size1 != size2:
                        #     print("Current video is under recording, wait for %d secs." % min_interval)
                        #     sleep(min_interval)
                        # else:
                        #     print("Recording finished! Uploading starts!")
                        try:
                            copyLargeFile(origin_dir, target_dir)
                            sleep(min_interval)
                        except IOError as e:
                            print("Failed, retry times: %d" % retry_count)
                            if os.path.exists(target_dir):
                                os.remove(target_dir)
                            sleep(min_interval)
                            retry_count += 1

                        if os.path.exists(target_dir):
                            size_origin = os.path.getsize(origin_dir)
                            size_target = os.path.getsize(target_dir)
                            print("original file size:%d, target file size:%d" % (size_origin, size_target))
                            if size_origin == size_target:
                                upload_success = True
                                print("File uploaded as: %s successfully!" % target_dir)
                                if origin_dir.endswith('.avi'):
                                    os.remove(origin_dir)
                                    print("Original file:%s deleted." % origin_dir)
        except:
            p = self_recover_backend(gdrive_local, gdrive_rclone, p)
        sleep(interval)

if __name__ == '__main__':
    googleDriveManager(300, 5, 85136, 4)
    '''gdrive_local = "/mnt/googleTeamDrive/"
    gdrive_rclone = 'silasi_team_drive'
    p = Process(target=self_recover, args=[gdrive_local, gdrive_rclone], name='manager')
    p.start()
    while True:
        sleep(1)
        p = self_recover_backend(gdrive_local, gdrive_rclone, p)
        count = sum(1 for proc in psutil.process_iter() if proc.name =="manager")
        print(count)

    '''