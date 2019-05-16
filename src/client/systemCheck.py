"""
    Author: Julian Pitney
    Email: JulianPitney@gmail.com
    Organization: University of Ottawa (Silasi Lab)
"""



import os

def check_directory_structure():

    assert(os.path.isdir('../../../HomeCageSinglePellet_server_1')),"Error: HomeCageSinglePellet_server directory does not exist"
    assert(os.path.isdir('../../src')),"Error: HomeCageSinglePellet_server/src directory does not exist"
    assert(os.path.isdir('../../bin')),"Error: HomeCageSinglePellet_server/bin directory does not exist"
    assert(os.path.isdir('../../config')),"Error: HomeCageSinglePellet_server/config directory does not exist"
    assert(os.path.isdir('../../resources')),"Error: HomeCageSinglePellet_server/resources directory does not exist"
    assert(os.path.isdir('../../temp')),"Error: HomeCageSinglePellet_server/temp directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles')),"Error: HomeCageSinglePellet_server/AnimalProfiles directory does not exist"
    #assert(os.path.isdir('../../src/analysis')),"Error: HomeCageSinglePellet_server/src/analysis directory does not exist"
    assert(os.path.isdir('../../src/arduino')),"Error: HomeCageSinglePellet_server/src/arduino directory does not exist"
    assert(os.path.isdir('../../src/arduino/homecage_server')),"Error: HomeCageSinglePellet_server/src/arduino/homecage_server directory does not exist"
    assert(os.path.isdir('../../src/client')),"Error: HomeCageSinglePellet_server/src/client directory does not exist"
    assert(os.path.isdir('../../src/ptgrey')),"Error: HomeCageSinglePellet_server/src/ptgrey directory does not exist"
    assert(os.path.isfile('../../bin/SessionVideo')),"Error: HomeCageSinglePellet_server/bin/SessionVideo file does not exist"
    #assert(os.path.isfile('../../config/3D_reconstruction_calibration.txt')),"Error: HomeCageSinglePellet_server/config/3D_reconstruction_calibration.txt file does not exist"
    assert(os.path.isfile('../../config/config.txt')),"Error: HomeCageSinglePellet_server/config/config.txt file does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE1')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE1 directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE1/Analyses')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE1/Analyses directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE1/Logs')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE1/Logs directory does not exist"
    assert(os.path.isfile('../../AnimalProfiles/MOUSE1/Logs/MOUSE1_session_history.csv')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE1/Logs/MOUSE1_session_history.csv does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE1/Videos')),"Error: HomeCageSinglePellet/AnimalProfiles/MOUSE1/Videos directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE1/Temp')),"Error: HomeCageSinglePellet/AnimalProfiles/MOUSE1/Temp directory does not exist"
    assert(os.path.isfile('../../AnimalProfiles/MOUSE1/MOUSE1_save.txt')),"Error: HomeCageSinglePellet/AnimalProfiles/MOUSE1/MOUSE1_save.txt does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE2')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE2 directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE2/Analyses')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE2/Analyses directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE2/Logs')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE2/Logs directory does not exist"
    assert(os.path.isfile('../../AnimalProfiles/MOUSE2/Logs/MOUSE2_session_history.csv')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE2/Logs/MOUSE2_session_history.csv does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE2/Videos')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE2/Videos directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE2/Temp')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE2/Temp directory does not exist"
    assert(os.path.isfile('../../AnimalProfiles/MOUSE2/MOUSE2_save.txt')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE2/MOUSE2_save.txt does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE3')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE3 directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE3/Analyses')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE3/Analyses directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE3/Logs')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE3/Logs directory does not exist"
    assert(os.path.isfile('../../AnimalProfiles/MOUSE3/Logs/MOUSE3_session_history.csv')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE3/Logs/MOUSE3_session_history.csv does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE3/Videos')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE3/Videos directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE3/Temp')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE3/Temp directory does not exist"
    assert(os.path.isfile('../../AnimalProfiles/MOUSE3/MOUSE3_save.txt')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE3/MOUSE3_save.txt does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE4')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE4 directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE4/Analyses')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE4/Analyses directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE4/Logs')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE4/Logs directory does not exist"
    assert(os.path.isfile('../../AnimalProfiles/MOUSE4/Logs/MOUSE4_session_history.csv')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE4/Logs/MOUSE4_session_history.csv does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE4/Videos')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE4/Videos directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE4/Temp')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE4/Temp directory does not exist"
    assert(os.path.isfile('../../AnimalProfiles/MOUSE4/MOUSE4_save.txt')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE4/MOUSE4_save.txt does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE5')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE5 directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE5/Analyses')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE5/Analyses directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE5/Logs')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE5/Logs directory does not exist"
    assert(os.path.isfile('../../AnimalProfiles/MOUSE5/Logs/MOUSE5_session_history.csv')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE5/Logs/MOUSE5_session_history.csv does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE5/Videos')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE5/Videos directory does not exist"
    assert(os.path.isdir('../../AnimalProfiles/MOUSE5/Temp')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE5/Temp directory does not exist"
    assert(os.path.isfile('../../AnimalProfiles/MOUSE5/MOUSE5_save.txt')),"Error: HomeCageSinglePellet_server/AnimalProfiles/MOUSE5/MOUSE5_save.txt does not exist"


    if(not os.path.isfile('../../config/trialLimitConfig.txt')):
        with open('../../config/trialLimitConfig.txt', 'w') as f:
            f.write("0\n")
            f.write("0\n")
            f.write("0\n")
            f.write("0\n")
            f.write("0\n")

