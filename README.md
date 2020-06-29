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
3. Install Arduino IDE v1.8.5. (https://www.arduino.cc/en/Main/Software)
	
4. Create and configure a virtual environment for installing the HomeCageSinglePellet code.
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
	- `pip install /path/to/HASRA/requirment/opencv_python-4.1.2+contrib-cp36-cp36m-win_amd64.whl`

5. `git clone https://github.com/SilasiLab/HomeCageSinglePellet_server.git`
	
	
# **Assembly:**

The detailed assembly manual can be found here:
https://github.com/SilasiLab/HomeCageSinglePellet_server/blob/master/Homecage%20assembly%20manual.pdf



# **Usage**:
### **Running the Device**
1. Enter the virtual environment that the system was installed in by typing `conda activate <my_env>` into a terminal.

2. Optional: Use `cd` to navigate to` HomeCageSinglePellet_server/src/client/` and then run `python -B genProfiles.py`. The text prompts will walk you through entering your new animals into the system. Since the folder and the file are already inclued in this repo, this step is optional.

3. Open HomeCageSinglePellet_server/config/config.txt and set the system configuration you want.

4. Find the COM port ids for Arduino and RFID reader, using `mode` command in terminal.
(In linux: Arduino needs to be USB0 , and RFID reader needs to be USB1. You can see connected USB devices with terminal command:
ls /dev/tty* and You need to replace the COMs in main.py -> `sys_init()` function manually.) 
  
5. Open a termanal and run following command:
* `cd \your\path\to\HomeCageSinglePellet_server\src\client\`
* `conda activate YourEnvironment` replace YourEnvironment by the name of your environment.
* `python main.py COM-arduino COM-RFID` replace COM-arduino and COM-RFID by the COM ids of Arduino and RFID respectively.


6. Optional: If you have a google file stream mounted on this computer, you can choose to upload all the viedos and log files to google drive. You need firstly find out the local path to this google drive folder, in this case it is: `G:\Shared drives\SilasiLabGdrive`.
Since there could be mutiple cage running on the same computer and they can also be stored in the same google cloud folder. You can add a suffix to the project foler name by changing the root folder name from `HomeCageSinglePellet_server` to `HomeCageSinglePellet_server_id`(replace the id by your id) 
In the same folder, open another terminal and activate the virtual environment again, then run `python googleDriveManager.py \path\to\your\cloud\drive\folder`.
The videos and the log files will be stored in `your cloud drive\homecage_id_sync`.

7. You need to put in the RFID tag numbers manually into the profiles. Take mouse 1 as an instance, you need to replace the first line in `HomeCageSinglePellet_server\AnimalProfiles\MOUSE1\MOUSE1_save.txt`. If you do not know your tag number, don't worry. You can scan it on the RFID reader, it will be printed in the Terminal as `[tag number] not recognized`.

8. To test that everything is running correctly, block the IR beam breaker with something
	and scan one of the system’s test tags. If a session starts properly, it’s working. You will also be able to find out hom many pellets have been succefully displayed out of current displays we have as it is shown in the terminal too. 

9. To shut the system down cleanly; 

	- Ensure no sessions are currently running. 
	- Press the quit button on the GUI.
	- Ctrl+c out of the program running in the terminal.


# **Troubleshooting**:

* Is everything plugged in?
* Make sure you are in the correct virtual environment.
* Make sure the HomeCageSinglePellet/config/config.txt file contains the correct configuration. (If the file gets deleted it will be replaced by a default version at system start)
* Make sure there are 1 to 5 profiles in the HomeCageSinglePellet/AnimalProfiles/ directory. Ensure these profiles contain all the appropriate files and that the save.txt file for each animal contains the correct information. 
