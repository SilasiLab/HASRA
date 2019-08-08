"""
    Author: Julian Pitney, Junzheng Wu
    Email: JulianPitney@gmail.com, jwu220@uottawa.ca
    Organization: University of Ottawa (Silasi Lab)
"""

from tkinter import *
import os
import pysnooper

# This is the GUI for configuring AnimalProfiles. It reads profiles from the ~/HomeCageSinglePellet/AnimalProfiles/ directory.
# It expects to find 5 profiles there and will not work with any other number. Profiles should be named as follows: 
# MOUSE1, MOUSE2, MOUSE3, MOUSE4, MOUSE5. Do not use other names. This GUI gets instantiated in its own process that runs
# concurrently with the SessionController process.
#
# Disclaimer: This was not well written. However, it's pretty straightforward. 
# Create button -> Assign function to it -> Position it -> Pack it into tk frame.
# Nothing fancy going on. Just note the dependancy tree is a mess and changing one thing 
# might affect something seemingly unrelated. Advise not modifying unless really needed.
#
#
# Most of the buttons are attached to a function that simply reads and writes to a profileState. They will also update text boxes
# when appropriate. It's mostly clear just by reading it.

class GUI:


    # All of the buttons are intialized and rendered inside __init__. 
	def __init__(self, master, animalProfilePath):


		self.master = master
		self.animalProfilePath = animalProfilePath
		self.profileNames = []
		self.profileSaveFilePaths = []
		self.profileStates = []
		self.currentMouse = -1

		self.triallimit_box_list = []
		self.triallimit_list = []

		self.front_back_box_list = []
		self.left_right_box_list = []


		with open(".."+os.sep+".."+os.sep+"config"+ os.sep +"trialLimitConfig.txt") as f:
			for i in range(6):
				self.triallimit_list.append(f.readline().rstrip())


		menubar = Menu(master)
		menubar.config(fg="red",)
		menubar.add_command(label="Quit!", command=master.quit)
		master.config(menu=menubar)

		frame1 = Frame(master)
		for i in range(1, 7):
			temp_label =  Label(frame1, text="Mouse %d"%i)
			temp_label.pack(padx=80, side=LEFT)
		frame1.pack()

		frame2 = Frame(master)

		self.load_animal_profiles()
		self.dists1 = [0, 0, 0, 0, 0, 0]
		self.dists2 = [0, 0, 0, 0, 0, 0]

		for mouse in range(1, 7):
			profileIndex = self.find_profile_state_index(mouse)
			self.dists1[mouse -1] = self.profileStates[profileIndex][4]
			self.dists2[mouse - 1] = self.profileStates[profileIndex][5]

		for i in range(6):
			temp_label = Label(frame2, text="trial limitation")
			temp_label.pack(padx=60,side=LEFT)

		frame2.pack()


		frameLimBox = Frame(master)
		for i in range(6):
			var = IntVar(value=int(self.triallimit_list[i]))  # initial value
			trial_box = Spinbox(frameLimBox, from_=0, to=3000, command=self.update_spinbox_trial, textvariable=var)
			trial_box.pack(padx=38,side=LEFT)
			self.triallimit_box_list.append(trial_box)
		frameLimBox.pack()


		frame_distance_front2back = Frame(master)
		for i in range(6):
			temp_label = Label(frame_distance_front2back, text="distance front 2 back")
			temp_label.pack(padx=40, side=LEFT)
		frame_distance_front2back.pack()

		frame_fb_spin = Frame(master)
		for i in range(6):
			var = IntVar(value=int(self.dists1[i]))
			fb_box = Spinbox(frame_fb_spin, from_=0, to=15, command=self.update_dist_fb, textvariable=var)
			fb_box.pack(padx=40, side=LEFT)
			self.front_back_box_list.append(fb_box)
		frame_fb_spin.pack()

		frame_distance_left2right = Frame(master)
		for i in range(6):
			temp_label = Label(frame_distance_left2right, text="distance left 2 right")
			temp_label.pack(padx=40, side=LEFT)
		frame_distance_left2right.pack()

		frame_lr_spin = Frame(master)
		for i in range(6):
			var = IntVar(value=int(self.dists2[i]))
			lr_box = Spinbox(frame_lr_spin, from_=0, to=15, command=self.update_dist_lr, textvariable=var)
			lr_box.pack(padx=40, side=LEFT)
			self.left_right_box_list.append(lr_box)
		frame_lr_spin.pack()

		frame42 = Frame(master)
		self.label = Label(frame42, text="\nPellet Presentation Distance(mm)")
		self.label.pack()
		frame42.pack()

	def update_spinbox_trial(self):
		for i in range(6):
			self.triallimit_list[i] = self.triallimit_box_list[i].get()

		with open(".."+os.sep+".."+os.sep+"config"+os.sep+"trialLimitConfig.txt", 'w') as f:
			for i in range(6):
				f.write(self.triallimit_list[i] + '\n')


	def update_dist_fb(self):
		for i in range(6):
			self.dists1[i] = self.front_back_box_list[i].get()
		self.on_update()

	def update_dist_lr(self):
		for i in range(6):
			self.dists2[i] = self.left_right_box_list[i].get()
		self.on_update()

	def load_animal_profiles(self):

		self.profileNames = []
		self.profileStates = []
		self.profileSaveFilePaths = []

		# Get list of profile folders
		self.profileNames = os.listdir(self.animalProfilePath)


		for profile in self.profileNames:

			# Build save file path and save in list
			loadFile = self.animalProfilePath + os.sep + profile + os.sep + profile + "_save.txt"
			# Open the save file
			try:
				load = open(loadFile, 'r')
			except IOError:
				print ("Could not open AnimalProfile save file!")

			# Read all lines from save file and strip them
			with load:
				profileState = load.readlines()

			self.profileStates.append([x.strip() for x in profileState])


			self.profileSaveFilePaths.append(loadFile)


	def save_animal_profile(self, profileIndex):

		with open(self.profileSaveFilePaths[profileIndex], 'w') as save:
			save.write(str(self.profileStates[profileIndex][0]) + "\n")
			save.write(str(self.profileStates[profileIndex][1]) + "\n")
			save.write(str(self.profileStates[profileIndex][2]) + "\n")
			save.write(str(self.profileStates[profileIndex][3]) + "\n")
			save.write(str(self.profileStates[profileIndex][4]) + "\n")
			save.write(str(self.profileStates[profileIndex][5]) + "\n")
			save.write(str(self.profileStates[profileIndex][6]) + "\n")
			save.write(str(self.profileStates[profileIndex][7]) + "\n")
			save.write(str(self.profileStates[profileIndex][8]) + "\n")



	# Since the profiles might be loaded into <profileStates> in an arbitrary order,
    # we need to identify which profileState index corresponds to which profile number.
    # This function just takes a profile/mouse number and searches <profileStates> for the 
    # profileState corresponding to that mouse number. It then returns the correct index. 
    #
    # E.G MOUSE1's profileState index might be 4
	def find_profile_state_index(self, mouseNumber):

		for x in range(0,len(self.profileStates)):
			if mouseNumber == int(self.profileStates[x][2]):

				return x

		return -1

	def on_update(self):
		self.load_animal_profiles()
		for i in range(1, 7):
			profileIndex = self.find_profile_state_index(i)
			self.profileStates[profileIndex][4] = self.dists1[i - 1]
			self.profileStates[profileIndex][5] = self.dists2[i - 1]
			self.save_animal_profile(profileIndex)

	def update_button_onClick(self):

		self.load_animal_profiles()

		if self.currentMouse > 0 and self.currentMouse <= 5:

			profileIndex = self.find_profile_state_index(self.currentMouse)

			if profileIndex == -1:

				print("Error: Could not find profile for Mouse " + str(self.currentMouse))
				return -1

			else:

				self.profileStates[profileIndex][4] = self.scale.get()
				self.save_animal_profile(profileIndex)


	def shutdown_onClick(self):
		self.master.destroy()
		exit()

# Entry point of GUI initialization. This function is outside of the GUI class
# so that it can be called by multiprocessing without having to construct a GUI
# object in the parent process first. Constructing a GUI object is expensive and
# we don't want it tying up the parent process. This is bad practice but it's easy
# so I'm leaving it for now.
def start_gui_loop(animalProfilePath):

	root = Tk()
	root.title("Cage1")
	gui = GUI(root, animalProfilePath)
	gui.load_animal_profiles()
	root.mainloop()
	root.destroy()


