# **Overview**:

This system allows the user to host up to 5 mice in their home environment and automatically administer the single pellet reaching test to those animals. The system can run unsupervised and continuously for weeks at a time, allowing all 5 mice to perform an unlimited number of single pellet trials at their leisure. 

The design allows a single mouse at a time to enter the reaching tube. Upon entry, the animal’s RFID tag will be read, and if authenticated, a session will start for that animal. A session is defined as everything that happens from the time an animal enters the reaching tube to when they leave the tube. At the start of a session, the animal’s profile will be read and the task difficulty will be automatically adjusted by moving the pellet presentation arm to the appropriate distance away from the reaching tube. After the difficulty is set, pellets will begin being presented with either the left or right presentation arm, depending on which arm is specified in the mouse’s profile. Pellets will continue to be presented periodically until the mouse leaves the tube, at which point the session will end. Video and other data is recorded for the duration of each session. At session end, all the data for the session is saved in an organized way. 





# **Dependencies:**
* Ubuntu v16.04 LTS: Kernel version 4.4.19-35 or later
* Or Windows 10 is recommended, since the backend camera driver performs better that the one on linux in our experiment.
* Python v3.6.10
	* pySerial==3.4	
	* numpy==1.18.1
	* OpenCV=4.1.2 (A whl file is provided under requirment folder.)
	* tkinter=8.6.8
	* matplotlib=3.1.3
	* Pillow
	* tqdm
	* tensorflow
	* keras
	* psutil
	* multiprocessing
	* subprocess
	
* Arduino IDE v1.8.5

# **Software Installation:**
1. Install Ubuntu 16.04 LTS or Windows10 on your machine.
2. Install Anaconda. (https://www.anaconda.com/distribution/)
3. Install the Flir Spinnaker SDK v1.10.31 **INSERT GOOGLE DRIVE LINK TO SPINNAKER SDK HERE**
4. Install Arduino IDE v1.8.5. (https://www.arduino.cc/en/Main/Software)
	
5. Create and configure a virtual environment for installing the HomeCageSinglePellet code.
	- `conda create -n <yourenvname> python=3.5.2 anaconda`
	- `conda activate <yourenvname>`
	- `conda install -c anaconda numpy`
	- `conda install -c anaconda pyserial`
	- `conda install -c anaconda tk`
	- `conda install -c conda-forge matplotlib`
	- `conda install tqdm`
	- `conda install Pillow`
	- `pip install psutil`
	- `pip install pysnooper`
	
6. For opencv, we need to download whl file first. https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv and download `opencv_python‑3.4.6+contrib‑cp35‑cp35m‑win_amd64.whl`
	Open a terminal, go in to the directory containing this file.
	- `pip install ./opencv_python‑3.4.6+contrib‑cp35‑cp35m‑win_amd64.whl`

7. Download the HCSP source code from https://github.com/SilasiLab/HomeCageSinglePellet and unpack it.
8. Optional (Only if you want to use the analysis features): Install Deeplabcut using the Anaconda based pip installation method. (https://github.com/AlexEMG/DeepLabCut/blob/master/docs/installation.md)
9. Optional (Only if you want to use the anaylsis features): Move the file `HomeCageSinglePellet/src/analysis/HCSP_analyze.py` into `~/.conda/envs/DLC2/lib/python3.6/site-packages/deeplabcut` (Where DLC2 is the name of the anaconda virtual environment where you installed Deeplabcut).
10. Optional (Only if you want to use the anaylsis features): Download our pretrained DLC2 network for automatically extracting reach attempts from your videos. **INSERT GOOGLE DRIVE LINK TO NETWORK HERE**
11. Done!
	
	
# **Assembly:**

The detailed assembly manual can be found here:
https://github.com/SilasiLab/HomeCageSinglePellet_server/blob/master/Homecage%20assembly%20manual.pdf



# **Usage**:
### **Running the Device**
1. Enter the virtual environment that the system was installed in by typing `source activate <my_env>` into a terminal.

2. Use `cd` to navigate to HomeCageSinglePellet_server/src/client/ and then run `python -B genProfiles.py`. The text prompts will walk you through entering your new animals into the system.

3. Open HomeCageSinglePellet_server/config/config.txt and set the system configuration you want.

4. Enter HomeCageSinglePellet_server/src/client/ and run `python -B main.py`

5. In the same folder, open another terminal and activate the virtual environment again, modify the cage ID in the script googleDriveManager.py, then run `python googleDriveManager.py`

6. To test that everything is running correctly, block the IR beam breaker with something
	and scan one of the system’s test tags. If a session starts properly, it’s working.

7. To shut the system down cleanly; 

	- Ensure no sessions are currently running. 
	- Press the quit button on the GUI.
	- Ctrl+c out of the program running in the terminal.
NB.
1. Arduino needs to be USB0 , and RFID reader needs to be USB1. You can see connected USB devices with terminal command:
ls /dev/tty*







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

