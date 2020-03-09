"""
    Author: Julian Pitney, Junzheng Wu
    Email: JulianPitney@gmail.com, jwu220@uottawa.ca
    Organization: University of Ottawa (Silasi Lab)
"""

import gui
import arduinoClient
import systemCheck
import time
import multiprocessing
import serial
from subprocess import PIPE, Popen
import os
import datetime
from driver_for_a_better_camera import *
from googleDriveManager import is_locked
import numpy as np
from detector import Detector
D = Detector("model/model.h5")
systemCheck.check_directory_structure()
# Load all configuration information for running the system.
# Note: Configuration information for data analysis does not come from here.

dirpath = os.getcwd()
base_dir = dirpath.split('src'+os.sep+'client')[0]
PROFILE_SAVE_DIRECTORY = os.path.join(base_dir, 'AnimalProfiles')


# This function generates a list of AnimalProfiles found inside <profile_save_directory>.
# It then reads the save.txt file for each profile found, and uses the information
# in that file to reconstruct the AnimalProfile object. It returns all the
# reconstructed profiles as a list of AnimalProfiles.
# Note: This function works by assuming the directory structure of each AnimalProfile
# is consistent and the required save.txt files are present, i.e:
#
# <profile_save_directory>
#   -
#   - ProfileName
#       -
#       - Logs
#       - Videos
#       - save.txt
mouse1TrialLimit = None
mouse2TrialLimit = None
mouse3TrialLimit = None
mouse4TrialLimit = None
mouse5TrialLimit = None

mouse1TrialsToday = 0
mouse2TrialsToday = 0
mouse3TrialsToday = 0
mouse4TrialsToday = 0
mouse5TrialsToday = 0

def loadAnimalProfileTrialLimits():

    global mouse1TrialLimit, mouse2TrialLimit, mouse3TrialLimit, mouse4TrialLimit, mouse5TrialLimit

    with open(".." + os.sep + ".." + os.sep + "config" + os.sep + "trialLimitConfig.txt") as f:
        # print(f.readline().rstrip())
        mouse1TrialLimit = int(f.readline().rstrip())
        mouse2TrialLimit = int(f.readline().rstrip())
        mouse3TrialLimit = int(f.readline().rstrip())
        mouse4TrialLimit = int(f.readline().rstrip())
        mouse5TrialLimit = int(f.readline().rstrip())

def resetAnimalProfileTrialsToday():

    global mouse1TrialsToday, mouse2TrialsToday, mouse3TrialsToday, mouse4TrialsToday, mouse5TrialsToday
    currentDT = datetime.datetime.now()

    if(currentDT.hour == "07"):
        print("Resetting animal trial limits for the day!")
        mouse1TrialsToday = 0
        mouse2TrialsToday = 0
        mouse3TrialsToday = 0
        mouse4TrialsToday = 0
        mouse5TrialsToday = 0


def loadAnimalProfiles(profile_save_directory):
    # Get list of profile folders
    profile_names = os.listdir(profile_save_directory)
    profiles = []
    print(profile_names)
    for profile in profile_names:

        # Build save file path
        # load_file = profile_save_directory + profile + "/" + profile + "_save.txt"
        load_file = os.path.join(profile_save_directory , profile, profile + "_save.txt")
        profile_state = []
        # Open the save file
        try:
            load = open(load_file, 'r')
        except IOError:
            print("Could not open AnimalProfile save file!")

        # Read all lines from save file and strip them
        with load:
            profile_state = load.readlines()
        profile_state = [x.strip() for x in profile_state]

        # Create AnimalProfile object using loaded data and put it in profile list
        ID = profile_state[0]
        name = profile_state[1]
        mouseNumber = profile_state[2]
        cageNumber = profile_state[3]
        difficulty_dist_mm1 = profile_state[4]
        difficulty_dist_mm2 = profile_state[5]
        dominant_hand = profile_state[6]
        session_count = profile_state[7]
        animal_profile_directory = load_file.replace(name + "_save.txt", "")
        temp = AnimalProfile(ID, name, mouseNumber, cageNumber, difficulty_dist_mm1, difficulty_dist_mm2, dominant_hand, session_count,
                             animal_profile_directory, False)
        profiles.append(temp)

    return profiles


class AnimalProfile(object):

    #    A profile containing all information related to a particular animal. When a new animal is added to the system,
    #    an AnimalProfile should be created for that animal. This profile will be used by the rest
    #    of the system for any operation pertaining to the animal (data logging, identification, etc). When the application closes,
    #    saveProfile() should be called on each profile in the system. A global loadProfiles() function is used to load/reconstruct
    #    each profile at load time. Each AnimalProfile has the following properties:
    #
    #    Attributes:
    #        ID: A unique identification number for the animal. In our case this number will be the RFID of the RF tag implanted in the animal.
    #        name: The name of the animal
    #		 mouseNumber: The number of the animal in it's cage (0-5).
    #		 cageNumber: The cage number of the animal.
    #        difficulty_dist_mm: An integer representing the distance from the tube to the presented pellet in mm.
    #        dominant_hand: A string representing the dominant hand of the mouse.
    #        session_count: The number of Sessions the animal has participated in. In our system, this is the number of times the animal has
    #                        entered the experiment tube.
    #        animal_profile_directory: A path to the root folder where AnimalProfile's are stored.
    #        video_save_directory: A path to where the videos for this animal are stored. This path will be inside [./<animal_profile_directory>/<animal_name>/]
    #        log_save_directory: A path to where the logs for this animal are stored. This pathh will be inside [./<animal_profile_directory/<animal_name/]

    def __init__(self, ID, name, mouseNumber, cageNumber, difficulty_dist_mm1, difficulty_dist_mm2, dominant_hand, session_count,
                 profile_save_directory, is_new):

        self.ID = str(ID)
        self.name = str(name)
        self.mouseNumber = str(mouseNumber)
        self.cageNumber = str(cageNumber)
        self.difficulty_dist_mm1 = int(difficulty_dist_mm1)
        self.difficulty_dist_mm2 = int(difficulty_dist_mm2)
        self.dominant_hand = str(dominant_hand)
        self.session_count = int(session_count)

        if is_new:
            self.animal_profile_directory = profile_save_directory + name + os.sep
        else:
            self.animal_profile_directory = profile_save_directory

        self.video_save_directory = self.animal_profile_directory + "Videos" + os.sep
        self.log_save_directory = self.animal_profile_directory + "Logs" + os.sep

        if is_new:

            if not os.path.isdir(self.animal_profile_directory):
                os.makedirs(self.animal_profile_directory)

            if not os.path.isdir(self.video_save_directory):
                os.makedirs(self.video_save_directory)

            if not os.path.isdir(self.log_save_directory):
                os.makedirs(self.log_save_directory)

    # This function writes the state of the AnimalProfile object to the
    # AnimalProfile's save file.
    def saveProfile(self):

        save_file_path = self.animal_profile_directory + str(self.name) + "_save.txt"

        with open(save_file_path, 'w') as save:
            save.write(str(self.ID) + "\n")
            save.write(str(self.name) + "\n")
            save.write(str(self.mouseNumber) + "\n")
            save.write(str(self.cageNumber) + "\n")
            save.write(str(self.difficulty_dist_mm1) + "\n")
            save.write(str(self.difficulty_dist_mm2) + "\n")
            save.write(str(self.dominant_hand) + "\n")
            save.write(str(self.session_count) + "\n")
            save.write(str(self.animal_profile_directory) + "\n")

    # Generates the path where the video for the next session will be stored
    def genVideoPath(self, videoStartTimestamp):

        videoStartTimestamp = time.strftime("%Y-%m-%d_(%H-%M-%S)", time.localtime(videoStartTimestamp))
        temp_dir = os.path.join(PROFILE_SAVE_DIRECTORY, str(self.name), "Videos", videoStartTimestamp + "_" + str(
            self.ID) + "_" + str(self.cageNumber) + "_" + str(self.session_count))
        return temp_dir

    # This function takes all the information required for an animal's session log entry, and then formats it.
    # Once formatted, it appends the log entry to the animal's session_history.csv file.
    def insertSessionEntry(self, start_timestamp, end_timestamp, trial_count, successful_count=0):

        # TODO: Is there a better way to create + format strings?
        # session_history = self.log_save_directory + str(self.name) + "_session_history.csv"
        session_history = os.path.join(PROFILE_SAVE_DIRECTORY, str(self.name), 'Logs', str(self.name)+"_session_history.csv")
        start_date = time.strftime("%d-%b-%Y", time.localtime(start_timestamp))
        start_time = time.strftime("%H:%M:%S", time.localtime(start_timestamp))
        end_date = time.strftime("%d-%b-%Y", time.localtime(end_timestamp))
        end_time = time.strftime("%H:%M:%S", time.localtime(end_timestamp))
        csv_entry = str(self.session_count) + "," + str(self.name) + "," + str(self.ID) + "," + str(
            trial_count) + "," + str(successful_count) + "," + str(self.difficulty_dist_mm1) + "," + str(self.difficulty_dist_mm2) + "," + str(
            self.dominant_hand) + "," + start_date + "," + start_time + "," + end_date + "," + end_time + "\n"
        if not os.path.exists(session_history):
            with open(session_history, "w") as log:
                log.write(csv_entry)
        else:
            with open(session_history, "a") as log:
                log.write(csv_entry)

    def insertDisplay(self, time_stamp_list):
        csv_file = os.path.join(PROFILE_SAVE_DIRECTORY, str(self.name), 'Logs', str(self.name)+"_display_history.txt")
        if not os.path.exists(csv_file):
            with open(csv_file, 'w') as f:
                for time_stamp in time_stamp_list:
                    time_string = time_stamp.strftime("%Y/%m/%d,%H:%M:%S")
                    f.write(time_string + "\n")
        else:
            with open(csv_file, 'a') as f:
                for time_stamp in time_stamp_list:
                    time_string = time_stamp.strftime("%Y/%m/%d,%H:%M:%S")
                    f.write(time_string + "\n")

class SessionController(object):
    """
		A controller for all sessions that occur within the system. A "session" is defined as everything that happens while an animal is in the
                experiment tube. A session is started when an RFID is read and authorized. The session will continue until the IR beam is reconnected and
                the Arduino server sends a signal to indicate this. Sessions record several pieces of information during the session, including video, timestamps, motor actions, etc.
                The sessions is also responsible for sending requests to the Arduino for motor actions and for spawning a video recording process.
                A SessionController has the following properties:

		Attributes:
			profile_list: A list containing all animal profiles.
			arduino_client: An object that wraps a serial interface for talking to the Arduino server.
	"""

    def __init__(self, profile_list, arduino_client):

        self.profile_list = profile_list
        self.arduino_client = arduino_client
        self.predict = True

    def set_profile_list(self, profileList):

        self.profile_list = profileList

    # This function searches the SessionController's profile_list for a profile whose ID
    # matches the supplied RFID. If a profile is found, it is returned. If no profile is found,
    # -1 is returned. (Not very pythonic but I have C-like habits.)
    def searchForProfile(self, RFID):

        for profile in self.profile_list:

            if profile.ID == RFID:
                return profile

        return -1

    def print_session_start_information(self, profile, startTime):

        session_start_msg = "-------------------------------------------\n" + "Starting session for " + profile.name
        print(session_start_msg)
        human_readable_start_time = time.strftime("%Y%m%d-%H:%M:%S", time.localtime(startTime))
        print("Start Time: {}".format(human_readable_start_time))

    def print_session_end_information(self, profile, endTime):

        human_readable_end_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(endTime))
        print("End Time: {}".format(human_readable_end_time))
        session_end_msg = profile.name + "'s session has completed\n-------------------------------------------\n"
        print(session_end_msg)

    # This function starts an experiment session for the animal identified in the supplied <profile>.
    # The session remains active until a signal is received from the Arduino server indicating that
    # the IR beam breaker has been reconnected.
    #
    # Each session forks a process that records video for the duration of the session.
    # This function is also responsible for sending a terminate signal to that forked process.
    # This signal is sent by creating a file called 'KILL' in the current working
    # directory (Not good, but does the job. I was halfway through implementing IPC with sockets
    # but didn't have time to finish).
    #
    # This function is also responsible for telling the Arduino server how to position the stepper motors and
    # for periodically sending get pellet requests.
    #
    # Each session will also log data about itself.
    #
    # On completion, this session will update the <profile> it was running the session for,
    # clean up any processes it opened, and save all log data.
    #
    # TODO: This function is pretty bloated and probably harder to read than it needs to be. Better separation
    # of concerns could be easily achieved by splitting it into a few smaller functions.
    def startSession(self, profile):

        startTime = time.time()
        profile.session_count += 1
        self.print_session_start_information(profile, startTime)
        successful_count = 0
        vidPath = profile.genVideoPath(startTime) + '.avi'
        tempPath = os.path.join(os.path.dirname(vidPath), 'temp_'+ datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.avi')


        print("saved as :"+vidPath)
        if "TEST" in profile.name:
            print("Its testing")
            p = Popen(["python", "driver_for_a_better_camera.py", "--c", str(0), "--p", tempPath, "--t", "True"], stdin=PIPE, stdout=PIPE)
        else:
            p = Popen(["python", "driver_for_a_better_camera.py", "--c", str(0), "--p", tempPath, "--t", "False"], stdin=PIPE, stdout=PIPE)
        # Tell server to move stepper to appropriate position for current profile
        self.arduino_client.serialInterface.write(b'3')

        stepperMsg1 = scale_stepper_dist(profile.difficulty_dist_mm1)
        stepperMsg2 = scale_stepper_dist(profile.difficulty_dist_mm2)

        self.arduino_client.serialInterface.write(stepperMsg1.encode())
        self.arduino_client.serialInterface.write(stepperMsg2.encode())
        print(stepperMsg1, stepperMsg2)

        # Main session loop. Runs until it receives TERM sig from server. Polls
        # the camera queue for GETPEL messages and forwards to server if it receives one.

        trial_count = 1
        raise_moment = datetime.datetime.now()
        display_time_stamp_list = []
        SEED_FLAG = False

        def check_deetction_frame():
            try:
                os.rename("detection_frame.jpg", "detection_frame.jpg")
                if os.path.getsize("detection_frame.jpg") > 10:
                    return True
                return False
            except OSError as e:
                return False

        def detect(p):
            '''
            Wait for real code
            :return:
            '''
            if os.path.exists("detection_frame.jpg"):
                os.remove("detection_frame.jpg")
            p.stdin.write(b"detect\n")
            p.stdin.flush()

            while not check_deetction_frame():
                time.sleep(0.1)
            img = cv2.imread("detection_frame.jpg")
            print(img.shape)
            time.sleep(1)

            return D.predict_in_real_use(img)

        time.sleep(6)
        while True:
            if self.predict:
                if (datetime.datetime.now() - raise_moment).seconds >= 4:
                    # SEED_FLAG = detect(p)
                    SEED_FLAG = False
                if not SEED_FLAG:
                    self.arduino_client.serialInterface.write(b'1')
                    self.arduino_client.serialInterface.flushOutput()
                    trial_count += 1
                    time.sleep(4)
                    if detect(p):
                        SEED_FLAG = False # do cycling all the time
                        if "TEST" in profile.name:
                            SEED_FLAG = False
                        raise_moment = datetime.datetime.now()
                        display_time_stamp_list.append(raise_moment)
                        successful_count += 1
                    else:
                        SEED_FLAG = False
                print("Total trial: %d, successful trial: %d, Percentage; %.3f" % (trial_count, successful_count, float(successful_count) / float(trial_count)))
            else:
                if (datetime.datetime.now() - raise_moment).seconds >= 5:
                    if profile.dominant_hand == "LEFT":
                        self.arduino_client.serialInterface.write(b'1')
                    elif profile.dominant_hand == "RIGHT":
                        self.arduino_client.serialInterface.write(b'2')
                    elif profile.dominant_hand == "BOTH":
                        self.arduino_client.serialInterface.write(b'4')
                    raise_moment = datetime.datetime.now()
                    trial_count += 1
                    display_time_stamp_list.append(raise_moment)
                    time.sleep(1)

            # Check if message has arrived from server, if it has, check if it is a TERM message.
            if self.arduino_client.serialInterface.in_waiting > 0:
                serial_msg = self.arduino_client.serialInterface.readline().rstrip().decode()
                print("=========================================================")
                print("receive message from arduino: %s" % serial_msg)
                print("=========================================================")
                if serial_msg == "TERM":
                    self.arduino_client.serialInterface.flush()
                    self.arduino_client.serialInterface.flushInput()
                    break

        p.stdin.write(b"stop\n")
        p.stdin.flush()
        for line in p.stdout.readlines():
            print(line)
        # Log session information.
        while is_locked(tempPath):
            time.sleep(1)

        if trial_count == 0:
            os.remove(tempPath)
        else:
            os.rename(tempPath, vidPath)
        endTime = time.time()
        profile.insertSessionEntry(startTime, endTime, trial_count, successful_count)
        profile.insertDisplay(display_time_stamp_list)
        profile.saveProfile()
        self.print_session_end_information(profile, endTime)

def scale_stepper_dist(distance):
    if distance < 10:
        return str(distance)
    elif distance <= 15:
        return str(hex(distance)).replace('0x', '')
    else:
        simple_dict = {16: 'g', 17: 'h', 18: 'i', 19: 'j', 20: 'k'}
        return simple_dict[distance]
# Just a wrapper to launch the configuration GUI in its own process.
def launch_gui():
    gui_process = multiprocessing.Process(target=gui.start_gui_loop, args=(PROFILE_SAVE_DIRECTORY,))
    gui_process.start()
    return gui_process


# This function initializes all the high level system components, returning a handle to each one.
def sys_init():
    # print(PROFILE_SAVE_DIRECTORY)
    profile_list = loadAnimalProfiles(PROFILE_SAVE_DIRECTORY)
    arduino_client = arduinoClient.client("COM9", 9600)
    ser = serial.Serial('COM4', 9600)

    guiProcess = launch_gui()
    session_controller = SessionController(profile_list, arduino_client)
    return profile_list, arduino_client, session_controller, ser, guiProcess


# This function listens to the open port of a serial object. It waits for <x02>
# to indicate the start of an RFID, if then appends to a string until it detects <x03>, indicating the end
# of the RFID.
def listen_for_rfid(ser):
    rfid = ''

    while (ser.is_open):
        byte = ser.read(1)

        if (byte == b'\x02'):
            rfid = ''
        elif (byte == b'\x03'):
            return rfid
        else:
            # print(byte)
            rfid += byte.decode('utf-8')


def main():

    global mouse1TrialLimit, mouse2TrialLimit, mouse3TrialLimit, mouse4TrialLimit, mouse5TrialLimit
    global mouse1TrialsToday, mouse2TrialsToday, mouse3TrialsToday, mouse4TrialsToday, mouse5TrialsToday

    loadAnimalProfileTrialLimits()
    # These are handles to all the main system components.

    profile_list, arduino_client, session_controller, ser, guiProcess = sys_init()

    # Entry point of the system. This block waits for an RFID to enter the <SERIAL_INTERFACE_PATH> buffer.
    # Once it receives an RFID, it parses it and searches for a profile with a matching RFID. If a profile
    # is found, it starts a session for that profile. If no profile is found, it goes back to listening for
    # an RFID.
    while True:

        # Block until RFID is received
        print("Waiting for RFID...")
        RFID_code = listen_for_rfid(ser)[:12]
        # Check RFID authorization

        profile = session_controller.searchForProfile(RFID_code)

        # RFID authorized
        if profile != -1:

            # Before starting a session, reload the animal profiles. This is done incase a profile was
            # changed by the GUI or some other process since the last load occured.
            resetAnimalProfileTrialsToday()
            session_controller.set_profile_list(loadAnimalProfiles(PROFILE_SAVE_DIRECTORY))
            profile = session_controller.searchForProfile(RFID_code)

            if(profile.mouseNumber == "1"):
                if(mouse1TrialsToday >= mouse1TrialLimit):
                    print("MOUSE1 has reached maximum trials for today...aborting!")
                    continue
                else:
                    mouse1TrialsToday += 1

            elif(profile.mouseNumber == "2"):
                if(mouse2TrialsToday >= mouse2TrialLimit):
                    print("MOUSE2 has reached maximum trials for today...aborting!")
                    continue
                else:
                    mouse2TrialsToday += 1

            elif(profile.mouseNumber == "3"):
                if(mouse3TrialsToday >= mouse3TrialLimit):
                    print("MOUSE3 has reached maximum trials for today...aborting!")
                    continue
                else:
                    mouse3TrialsToday += 1

            elif(profile.mouseNumber == "4"):
                if(mouse4TrialsToday >= mouse4TrialLimit):
                    print("MOUSE4 has reached maximum trials for today...aborting!")
                    continue
                else:
                    mouse4TrialsToday += 1

            elif(profile.mouseNumber == "5"):
                if(mouse5TrialsToday >= mouse5TrialLimit):
                    print("MOUSE5 has reached maximum trials for today...aborting!")
                    continue
                else:
                    mouse5TrialsToday += 1


            # Start a session on Arduino server side. <A> is the magic byte that tells the Arduino to start a session.
            arduino_client.serialInterface.flushInput()
            arduino_client.serialInterface.write(b'A')

            # Start a session on Python client side.
            # Wait for the mouse to get into the tube.
            time.sleep(1)
            session_controller.startSession(profile)
            # After the session returns, flush the Arduino serial communication buffer.
            arduino_client.serialInterface.flush()

            # Load profileList after each session as well. Can't remember why I decided to reload profiles before AND after session, 
            # but I don't see any downside and removing this might break something. 
            session_controller.set_profile_list(loadAnimalProfiles(PROFILE_SAVE_DIRECTORY))
            loadAnimalProfileTrialLimits()
        # RFID NOT authorized
        else:

            # <Y> is the magic byte that tells the Arduino server that the RFID was rejected. Sending this rejection notice
            # is no longer necessary, it is a relic of when the RFID sensor was handled by the Arduino directly. However, removing it
            # would require modifying the Arduino server code and there's no need for that at present. 
            arduino_client.serialInterface.write(b'Y')
            unrecognized_id_msg = RFID_code + " not recognized. Aborting session.\n\n"
            print(unrecognized_id_msg)

        # Reset RFID serial buffers. This is necessary because while an animal is in a session, it's RFID chip will often 
        # get read many times as it wiggles around under the RFID sensor. This buffer reset prevents those additional reads
        # from being processed after the session ends. 
        ser.reset_input_buffer()
        ser.reset_output_buffer()

# Python convention for launching main() function.
if __name__ == "__main__":
    main()
