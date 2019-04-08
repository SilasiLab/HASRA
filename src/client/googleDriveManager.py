from time import sleep
import shutil
from copy import copy
import os
import psutil
import subprocess
from multiprocessing import Process
def copyLargeFile(src, dest, buffer_size=16000):
    with open(src, 'rb') as fsrc:
        with open(dest, 'wb') as fdest:
            shutil.copyfileobj(fsrc, fdest, buffer_size)

def work_in_free_time(window_length=5, interval=3, threshold=0.3):
    cpu_pct = 0
    for i in range(window_length):
        cpu_pct += psutil.cpu_percent()
        sleep(interval)
    cpu_pct_ave = cpu_pct/float(window_length)
    print("cpu usage :%.4f" % cpu_pct_ave)
    if cpu_pct_ave < threshold:
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

def self_recover_backend(gdrive_local,gdrive_rclone):
    print("rlone restarting...")
    p = Process(target=self_recover, args=[gdrive_local, gdrive_rclone])
    p.start()
    print("rclone restated.")

def googleDriveManager(interval=20, min_interval=10, cage_id=85136, mice_n=4, gdrive_local="/mnt/googleTeamDrive/", gdrive_rclone='silasi_team_drive'):
    gdrive = os.path.join(gdrive_local, "HomeCages/")
    status = check_google_drive_status(gdrive)
    if not status:
        self_recover_backend(gdrive_local, gdrive_rclone)
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
                self_recover_backend(gdrive_local, gdrive_rclone)
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
                        sleep(min_interval)

                        size1 = os.path.getsize(origin_dir)
                        sleep(min_interval)
                        size2 = os.path.getsize(origin_dir)
                        if size1 != size2:
                            print("Current video is under recording, wait for %d secs." % min_interval)
                            sleep(min_interval)
                        else:
                            print("Recording finished! Uploading starts!")
                            try:
                                while not work_in_free_time():
                                    sleep(min_interval)
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
            self_recover_backend(gdrive_local, gdrive_rclone)
        sleep(interval)

if __name__ == '__main__':
    googleDriveManager(300, 10, 85136, 4)

