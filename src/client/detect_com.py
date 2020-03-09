from infi.devicemanager import DeviceManager
import os
import time
import copy

def get_camera_index(cage_id):

    dm = DeviceManager()
    camera_num = 0
    dm.root.rescan()
    camera_name = 'USB Video Device'
    for device in dm.all_devices:
        description = device.description
        if description == camera_name:
            camera_num += 1

    assert camera_num == 0
    camera_list = []
    while len(camera_list) < 3:
        dm.root.rescan()
        for device in dm.all_devices:
            description = device.description
            if description == camera_name:
                if device.address not in camera_list:
                    camera_list.append(device.address)
        time.sleep(0.1)
        print("scanning...", camera_list)

    current_camera_address = camera_list[cage_id - 1]
    sorted_list = copy.deepcopy(camera_list)
    # def sort_key(item):
    #     return -item
    # sorted_list.sort(key=sort_key)
    sorted_list.sort()
    camera_index = sorted_list.index(current_camera_address)
    print("camera index : %d" % camera_index)
    return camera_index

def get_device():
    dm = DeviceManager()
    camera_num = 0
    dm.root.rescan()
    camera_name = 'USB Video Device'
    for device in dm.all_devices:
        description = device.description
        if description == camera_name:
            camera_num += 1
            print(device.location_paths)
            print(device.instance_id)
if __name__ == '__main__':
    get_device()
