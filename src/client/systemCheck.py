'''
    Author: Julian Pitney, Junzheng Wu
    Email: JulianPitney@gmail.com, jwu220@uottawa.ca
    Organization: University of Ottawa (Silasi Lab)

    This script is designed for automatically create all the folders in the directory.
'''
import os

def check_directory_structure():
    dirpath = os.getcwd()
    base_dir = dirpath.split('src'+os.sep+'client')[0]
    mouse_num = 5

    subfolder_level_1 = ['src', 'bin', 'config', 'resources', 'temp', 'AnimalProfiles']
    mousefolder_level_2 = ['Analyses', 'Logs', 'Videos', 'Temp']
    for l1 in subfolder_level_1:
        temp_path = os.path.join(base_dir, l1)
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

        if l1 == 'src':
            src_folder = ['arduino'+os.sep+'homecage_server', 'client']
            for src_file in src_folder:
                assert (os.path.exists(os.path.join(temp_path, src_file))), "Error: %s does not exist"%src_file

        elif l1 == 'bin':
            if not os.path.exists(os.path.join(temp_path, 'SessionVideo')):
                os.mkdir(os.path.join(temp_path, 'SessionVideo'))

        elif l1 == 'AnimalProfiles':
            for i in range(1, mouse_num + 1):
                mouse_folder = os.path.join(temp_path, 'MOUSE%d'%i)
                for file_name in mousefolder_level_2:
                    if not os.path.exists(os.path.join(mouse_folder, file_name)):
                        os.mkdir(os.path.join(mouse_folder, file_name))
                # session_dir = os.path.join(mouse_folder, 'Logs/MOUSE%d_session_history.csv'%i)
                # assert os.path.exists(session_dir), "Error: %s does not exist"%session_dir
                # txt_dir = os.path.join(mouse_folder, 'MOUSE%d_save.txt'%i)
                # assert os.path.exists(txt_dir),  "Error: %s does not exist"%txt_dir
        elif l1 == 'config':

            if not os.path.isfile(os.path.join(temp_path, 'trialLimitConfig.txt')):

                with open(os.path.join(temp_path, 'trialLimitConfig.txt'), 'w') as f:
                    f.write("2000\n")
                    f.write("2000\n")
                    f.write("2000\n")
                    f.write("2000\n")
                    f.write("2000\n")
                    f.write("2000\n")
