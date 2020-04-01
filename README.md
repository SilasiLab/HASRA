# **Overview**:

This system allows the user to host up to 5 mice in their home environment and automatically administer the single pellet reaching test to those animals. The system can run unsupervised and continuously for weeks at a time, allowing all 5 mice to perform an unlimited number of single pellet trials at their leisure. 

The design allows a single mouse at a time to enter the reaching tube. Upon entry, the animal’s RFID tag will be read, and if authenticated, a session will start for that animal. A session is defined as everything that happens from the time an animal enters the reaching tube to when they leave the tube. At the start of a session, the animal’s profile will be read and the task difficulty as well as the left and right preference will be automatically adjusted by moving the pellet presentation arm to the appropriate distance both away from the reaching tube and from right to left. Pellets will continue to be presented periodically until the mouse leaves the tube, at which point the session will end. Video and other data is recorded for the duration of each session. At session end, all the data for the session is saved in an organized way. We also have an auxiliary function for counting the successful rate of displaying a pellet using MobileNetV2 based on tensorflow and keras.

For further analyse, you can check the repository posted here:
https://github.com/SilasiLab/HomecageSinglePellet_Manual





# **Dependencies:**
* Ubuntu v16.04 LTS: Kernel version 4.4.19-35 or later
* Or Windows 10 is recommended, since the backend camera driver performs better that the one on linux in our experiment.
* Anaconda 3 environment, for the dependancies without a version number, it means there is no specific requirement on it. 
	* Python==3.6.10
	* pySerial==3.4	
	* numpy==1.18.1
	* OpenCV=4.1.2 (A whl file is provided under requirment folder.)
	* tkinter=8.6.8
	* matplotlib=3.1.3
	* Pillow
	* tqdm
	* tensorflow=1.10.0
	* keras=2.2.4
	* psutil
	* multiprocessing
	* subprocess
	
* Arduino IDE v1.8.5

# **Software Installation:**
1. Windows 10 is strongly recommended for a better support of camera driver. Ubuntu 16.04 LTS is alternative.
2. Install Anaconda. (https://www.anaconda.com/distribution/)
3. Install the Flir Spinnaker SDK v1.10.31 **INSERT GOOGLE DRIVE LINK TO SPINNAKER SDK HERE**
4. Install Arduino IDE v1.8.5. (https://www.arduino.cc/en/Main/Software)
	
5. Create and configure a virtual environment for installing the HomeCageSinglePellet code.
	- `conda create -n <yourenvname> python=3.6.10 anaconda`
	- `conda activate <yourenvname>`
	- `conda install -c anaconda numpy==1.18.1`
	- `conda install -c anaconda pyserial==3.4`
	- `conda install -c anaconda tk==8.6.8`
	- `conda install -c conda-forge matplotlib`
	- `conda install tqdm`
	- `conda install Pillow`
	- `conda install tensorflow==1.10.0`
	- `conda install keras==2.2.4`
	- `pip install psutil`
	- `pip install /path/to/HomeCageSinglePellet_server/requirment/opencv_python-4.1.2+contrib-cp36-cp36m-win_amd64.whl`

7. `git clone https://github.com/SilasiLab/HomeCageSinglePellet_server.git`
	
	
# **Assembly:**

The detailed assembly manual can be found here:
https://github.com/SilasiLab/HomeCageSinglePellet_server/blob/master/Homecage%20assembly%20manual.pdf



# **Usage**:
### **Running the Device**
1. Enter the virtual environment that the system was installed in by typing `conda activate <my_env>` into a terminal.

2. Optional: Use `cd` to navigate to` HomeCageSinglePellet_server/src/client/` and then run `python -B genProfiles.py`. The text prompts will walk you through entering your new animals into the system. Since the folder and the file are already inclued in this repo, this step is optional.

3. Open HomeCageSinglePellet_server/config/config.txt and set the system configuration you want.

4. 
5. Enter HomeCageSinglePellet_server/src/client/ and run `python main.py`

6. OPtional: If you have a google file stream mounted on this computer, you can choose to upload all the viedos and log files to google drive. In the same folder, open another terminal and activate the virtual environment again, modify the cage ID in the script googleDriveManager.py, then run `python googleDriveManager.py`

7. To test that everything is running correctly, block the IR beam breaker with something
	and scan one of the system’s test tags. If a session starts properly, it’s working.

8. To shut the system down cleanly; 

	- Ensure no sessions are currently running. 
	- Press the quit button on the GUI.
	- Ctrl+c out of the program running in the terminal.
NB.
1. 
* In linux: Arduino needs to be USB0 , and RFID reader needs to be USB1. You can see connected USB devices with terminal command:
ls /dev/tty*
* For windows: You can use the command `mode` in the terminal to check the port name of each device connected to the computer.  






### **Analysis**:

A high level analysis script is provided that runs the data for all animals through a long analysis pipeline. The functions performed on each video include;

* Analyze with Deeplabcut2.
* Identify all reaching attempts and record frame indexes where reaches occur.
* Compute 3D trajectory of reaches and estimate magnitude of movement in millimeters.
* Cut videos to remove any footage not within the bounds of a reaching event.
* Neatly package data for each analyzed video in a descriptively named folder within the animals ./Analyses/ directory.

![](https://raw.githubusercontent.com/SilasiLab/HomeCageSinglePellet/master/resources/Images/reach.gif)

This analysis is started by entering the HomeCageSinglePellet/src/analysis/ directory and running
`bash analyze_videos.sh <CONFIG_PATH> <VIDEO_DIRECTORY> <NETWORK_NAME>`

This script takes the following input;

**CONFIG_PATH** = Full path to config.yaml file in root directory of DLC2 project.
![alt text](https://raw.githubusercontent.com/SilasiLab/HomeCageSinglePellet/master/resources/Images/CONFIG_PATH_ANALYSIS.png)

**VIDEO_DIRECTORY** = Full path to directory containing videos you want to analyze. (e.g <~/HomeCageSinglePellet/AnimalProfiles/MOUSE1/Videos/>)

**NETWORK_NAME** = Full name of DLC2 network you want to use to analyze videos. (e.g <DeepCut_res
net50_HomeCageSinglePelletNov18shuffle1_950000>)


Another script (`HomeCageSinglePellet/src/analysis/scoreTrials.py`) is provided for manually categorizing reaches once they have been identified in the step detailed above. This script opens a GUI that allows the user to select an animal and browse through all the videos that have been analyzed for that animal. (In the video list, blue videos indicate videos where reaches were detected by the analysis software. Beige videos indicate videos where no reaches were detected. Green videos indicate videos that have already been manually scored). When users select a video from the list, the video window will display the first detected reach in a loop. It will also display the "reach count" (e.g 1/16) to indicate how many reaches the video contains and which one is currently being viewed. The user can then use the mouse or a hotkey to place the current reach into a category. The video window will then jump to the next reach. This repeats until all the reaches for a given video are scored, at which point the category information will be saved. 
<img width="800" height="400" src="https://raw.githubusercontent.com/SilasiLab/HomeCageSinglePellet/master/resources/Images/SCORING_GUI_1.png">
<img width="800" height="400" src="https://raw.githubusercontent.com/SilasiLab/HomeCageSinglePellet/master/resources/Images/SCORING_GUI_2.png">

**Note:** All the analysis functions read and write all their data to/from `HomeCageSinglePellet/AnimalProfiles/<animal_name>/Analyses/`. Information for each video is saved in a unique folder whose name includes video creation date, animal RFID, cage number and session number. (e.g `2019-01-25_14:36:31_002FBE737B99_67465_5233`). Each of these folders will contain the raw video, the deeplabcut output from analyzing the video (.h5 and .csv formats). In addition, if >=1 reaches were found in the video, the folder will contain a file named date_time_rfid_cage_number_session_number_reaches.txt (e.g `2019-01-25_14:36:31_002FBE737B99_67465_5233_reaches.txt`). This file contains the start and stop frame indexes of each reach in the video and (x,y,z) vectors for each reach. In addition, once a video has been scored manually using `scoreTrials.py`, a file named date_time_rfid_cage_number_session_number_reaches_scored.txt (e.g `2019-01-25_14:36:31_002FBE737B99_67465_5233_reaches_scored.txt`) will be added to the video's folder. This file is the same as date_time_rfid_cage_number_session_number_reaches.txt, except that it also contains a category identifier for every reach.


# **Troubleshooting**:

* Is everything plugged in?
* Shutting the system down incorrectly will often cause the camera and camera software to enter a bad state.
	* Check if the light on the camera is solid green. If it is, unplug the camera and plug it back in.
	* Check the HomeCageSinglePellet/src/client/ directory for a file named KILL. If this file exists, delete it.
	* Make sure the camera is plugged into a USB 3.0 or greater port and that it is not sharing a USB bridge with too many 			other devices (I.e if you have 43 devices plugged into the back of the computer and none in the front, plug the 		camera into the front).
* Make sure you are in the correct virtual environment.
* Make sure the HomeCageSinglePellet/config/config.txt file contains the correct configuration. (If the file gets deleted it will be replaced by a default version at system start)
* Make sure there are 1 to 5 profiles in the HomeCageSinglePellet/AnimalProfiles/ directory. Ensure these profiles contain all 		the appropriate files and that the save.txt file for each animal contains the correct information. 
* Make sure that the Arduino mounted as device ttyUSB0 and that the RFID reader mounted as ttyUSB1 in /dev/. If they mounted 
differently, rebooting and attaching them in the correct order will fix the problem.

