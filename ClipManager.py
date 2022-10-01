import json
import os
import shutil
from Addons import checklistcombobox
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
#from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkinter import font as tkFont
from datetime import datetime
from PIL import ImageTk
from PIL import Image

# --------------------------------------------------------------------------------------------------
# MAIN APP CLASS
class App():
	def __init__(self):
		self.root = Tk()
		self.root.title("ClipManager")
		#self.root.iconbitmap("path/to/ico/file")
		# theme and font color
		self.main_theme = "grey35"
		self.font_color1 = "orange"
		self.font_color2 = "white"
		self.main_button_color = "grey45"
		self.selected_button_color = "DarkOrange2"
		self.critical_button_color = "firebrick2"
		self.safe_button_color = "green3"
		self.main_font_size11 = tkFont.Font(size=11, weight="bold")
		self.main_font_size8 = tkFont.Font(size=8, weight="bold")

		# variables
		self.currentClipName = StringVar(self.root)
		self.currentClipName.set("CLIP NAME.mp4")

		self.currentClipInfo = StringVar(self.root)
		self.currentClipInfo.set("NEW, 27/02/2022, 03:45, 400Mo")

		self.killCounter = 0
		self.mouseOverKill_counter = False

		self.main_frame = None
		self.loadMenuBar()
		self.loadClipManager()

	# --------------------------------------------------------------------------------------------------
	# MENU BAR
	def loadMenuBar(self):
		self.menubar = Menu(self.root, bg=self.main_theme, fg=self.font_color1, activebackground="white", activeforeground='black')
		self.file = Menu(self.menubar, tearoff=0, background=self.main_theme, fg=self.font_color1, font=self.main_font_size8)
		self.file.add_command(label="Options", command=self.openOptions)
		self.file.add_command(label="Help", command=None)
		self.menubar.add_cascade(label="File", menu=self.file)
		self.root.config(menu=self.menubar)

	# --------------------------------------------------------------------------------------------------
	# CLIP MANAGER MAIN PAGE
	def loadClipManager(self):
		# main paned window
		self.mainPanedWindow = PanedWindow(self.root, sashrelief=RAISED, showhandle=False, sashwidth=5, bg=self.font_color1)
		self.mainPanedWindow.pack(fill=BOTH, expand=True)

		# main window left frame
		self.leftFrame = LabelFrame(self.mainPanedWindow, text="TAG", font=self.main_font_size8, labelanchor="n", borderwidth=0, height=100, width=100, fg=self.font_color1, bg=self.main_theme)
		self.leftFrame.pack(fill=BOTH, expand=1, side=LEFT, padx=0, pady=0)

		# First Frame (Clip Name + Clip Info + Rename Button) NIR = NameInfoRename
		self.currentClipNIRFrame = Frame(self.leftFrame, borderwidth=0, bg=self.main_theme, relief="sunken")
		self.currentClipNIRFrame.pack(side=TOP, fill=X, expand=False, padx=5, pady=5)

		self.currentClipFrame = Frame(self.currentClipNIRFrame, borderwidth=0, bg=self.main_theme, relief="groove")
		self.currentClipFrame.pack(side=LEFT, fill=X, expand=True)

		self.currentClipNameEntry = Entry(self.currentClipFrame, text=self.currentClipName, font=self.main_font_size8, fg=self.font_color1, bg=self.main_theme, highlightbackground="red", highlightcolor="red", state=NORMAL)
		self.currentClipNameEntry.pack(side=TOP, fill=X, expand=False)
		
		self.currentClipInfoLabel = Label(self.currentClipFrame, text=self.currentClipInfo.get(), font=self.main_font_size8, anchor="w", fg=self.font_color1, bg=self.main_theme, borderwidth=0, relief="groove")
		self.currentClipInfoLabel.pack(side=TOP, fill=X, expand=False)

		self.buttonRename = Button(self.currentClipNIRFrame, text="Rename", fg=self.font_color1, font=self.main_font_size8, relief="raised", bg=self.main_theme, width=10, bd="1p")
		#self.buttonRename['command'] = self.buttonRename_clicked1
		self.buttonRename.pack(side=RIGHT, fill=Y)

		# --------------------------------------------------------------------------------------------------
		# Second Frame (PPNKCR = Previous + Pause + Next buttons + Kill Counter + Rating)
		self.PPNKCRFrame = Frame(self.leftFrame, borderwidth=0, bg=self.main_theme, relief="sunken")
		self.PPNKCRFrame.pack(side=TOP, fill=X, expand=False, pady=5)

		# --------------------------------------------------------------------------------------------------
		# Sub Frame PPN = Previous + Play + Next
		self.PPNFrame = LabelFrame(self.PPNKCRFrame, text="Media control", font=self.main_font_size8, labelanchor="s", borderwidth=0, bg=self.main_theme, fg=self.font_color1)
		self.PPNFrame.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=5)

		self.previousClipButton = Button(self.PPNFrame, wraplength=50, justify=CENTER, text="Previous Clip", fg=self.font_color2, font=self.main_font_size8, relief="raised", bg=self.main_theme, bd="1p")
		#self.previousClipButton['command'] = self.buttonPreviousClicked
		self.previousClipButton.pack(side=LEFT, fill=BOTH, expand=1)

		self.playButton = Button(self.PPNFrame, wraplength=60, justify=CENTER, text="Open Clip in Default Player", fg=self.font_color2, font=self.main_font_size8, relief="raised", bg=self.main_theme, bd="1p")
		#self.playButton['command'] = self.openInDefaultPlayer
		self.playButton.pack(side=LEFT, fill=BOTH, expand=1)

		self.nextClipButton = Button(self.PPNFrame, wraplength=60, justify=CENTER, text="Next Clip", fg=self.font_color2, font=self.main_font_size8, relief="raised", bg=self.main_theme, bd="1p")
		#self.nextClipButton['command'] = self.buttonNextClicked
		self.nextClipButton.pack(side=LEFT, fill=BOTH, expand=1)

		# --------------------------------------------------------------------------------------------------
		# Sub Frame KC = Kill Counter
		self.KCFrame = LabelFrame(self.PPNKCRFrame, text="Kill Counter", font=self.main_font_size8, labelanchor="s", borderwidth=0, bg=self.main_theme, fg=self.font_color1)
		self.KCFrame.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=5)

		# minus button
		buttonFont = tkFont.Font(size=16, weight="bold")
		self.buttonMINUS = Button(self.KCFrame, text="-", fg=self.font_color2, font=buttonFont, relief="raised", bg=self.main_theme, width=3, height=1, bd="1p")
		#self.buttonMINUS['command'] = self.buttonMINUSClicked
		self.buttonMINUS.pack(side=LEFT, fill=BOTH, expand=1)

		# kill count button
		self.buttonKILLCOUNTER = Button(self.KCFrame, text=str(self.killCounter), fg=self.font_color2,relief="raised", font=buttonFont, bg=self.main_theme, width=3, height=1, bd="1p")
		#self.buttonKILLCOUNTER['command'] = self.buttonKILLCOUNTERClicked
		#self.buttonKILLCOUNTER.bind("<Enter>", self._onEnterKillCounter)
		#self.buttonKILLCOUNTER.bind("<Leave>", self._onLeaveKillCounter)
		#self.buttonKILLCOUNTER.bind_all("<MouseWheel>", self._onMousewheel)
		self.buttonKILLCOUNTER.pack(side=LEFT, fill=BOTH, expand=1)

		# plus button
		self.buttonPLUS = Button(self.KCFrame, text="+", fg=self.font_color2, font=buttonFont, relief="raised", bg=self.main_theme, width=3, height=1, bd="1p")
		#self.buttonPLUS['command'] = self.buttonPLUSClicked
		self.buttonPLUS.pack(side=LEFT, fill=BOTH, expand=1)


		# --------------------------------------------------------------------------------------------------
		# Sub Frame R = Rating
		self.RFrame = LabelFrame(self.PPNKCRFrame, text="Rating", font=self.main_font_size8, labelanchor="s", borderwidth=0, bg=self.main_theme, fg=self.font_color1)
		self.RFrame.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=5)

		# star button 1
		iconSTAR = PhotoImage(file="Icons/Star.png")
		self.buttonSTAR1 = Button(self.RFrame, relief="raised", bg=self.main_theme, image=iconSTAR, bd="1p")
		self.buttonSTAR1.image = iconSTAR
		#self.buttonSTAR1['command'] = self.buttonSTAR1Clicked
		self.buttonSTAR1.pack(side=LEFT, expand=1, fill=BOTH)
		# star button 2
		self.buttonSTAR2 = Button(self.RFrame, relief="raised", bg=self.main_theme, image=iconSTAR, bd="1p")
		self.buttonSTAR2.image = iconSTAR
		#self.buttonSTAR2['command'] = self.buttonSTAR2Clicked
		self.buttonSTAR2.pack(side=LEFT, expand=1, fill=BOTH)
		# star button 3
		self.buttonSTAR3 = Button(self.RFrame, relief="raised", bg=self.main_theme, image=iconSTAR, bd="1p")
		self.buttonSTAR3.image = iconSTAR
		#self.buttonSTAR3['command'] = self.buttonSTAR3Clicked
		self.buttonSTAR3.pack(side=LEFT, expand=1, fill=BOTH)
		# star button 4
		self.buttonSTAR4 = Button(self.RFrame, relief="raised", bg=self.main_theme, image=iconSTAR, bd="1p")
		self.buttonSTAR4.image = iconSTAR
		#self.buttonSTAR4['command'] = self.buttonSTAR4Clicked
		self.buttonSTAR4.pack(side=LEFT, expand=1, fill=BOTH)
		# star button 5
		self.buttonSTAR5 = Button(self.RFrame, relief="raised", bg=self.main_theme, image=iconSTAR, bd="1p")
		self.buttonSTAR5.image = iconSTAR
		#self.buttonSTAR5['command'] = self.buttonSTAR5Clicked
		self.buttonSTAR5.pack(side=LEFT, expand=1, fill=BOTH)

		self.buttonSTARRef = [self.buttonSTAR1, self.buttonSTAR2, self.buttonSTAR3, self.buttonSTAR4, self.buttonSTAR5]



		# --------------------------------------------------------------------------------------------------
		# main window right frame
		self.rightFrame = LabelFrame(self.mainPanedWindow, text="SEARCH", font=self.main_font_size8, labelanchor="n", borderwidth=0, height=100, width=100, fg=self.font_color1, bg=self.main_theme)
		self.rightFrame.pack(fill=BOTH, expand=1, side=LEFT, padx=0, pady=0)



		self.mainPanedWindow.add(self.leftFrame)
		self.mainPanedWindow.add(self.rightFrame)

	# --------------------------------------------------------------------------------------------------
	# OPTIONS WINDOW
	def openOptions(self):
		self.sub_win = Toplevel(self.root)
		self.sub_win.resizable(False, False)
		self.sub_win.grab_set()
		# main sub window frame
		frame_font = tkFont.Font(size=13, weight="bold")
		self.main_preference_frame = LabelFrame(self.sub_win, text="Set your preferences", font=frame_font, labelanchor="n", borderwidth=0, bg=self.main_theme, fg="white")
		self.main_preference_frame.pack(side=TOP)
		# clip folder frame
		self.clip_folder_frame = LabelFrame(self.main_preference_frame, text="Select clip folder", borderwidth=0, bg=self.main_theme, fg="white")
		self.clip_folder_frame.pack(side=TOP, padx=10, pady=10)
		# clip data folder frame
		self.clip_data_folder_frame = LabelFrame(self.main_preference_frame, text="Select folder location to save clip data base", borderwidth=0, bg=self.main_theme, fg="white")
		self.clip_data_folder_frame.pack(side=TOP, padx=10, pady=10)
		# validation button frame
		self.validation_frame = Frame(self.main_preference_frame, borderwidth=0, bg=self.main_theme)
		self.validation_frame.pack(side=TOP, padx=10, pady=10)

		# clip folder path label
		self.clip_folder_path_label = Label(self.clip_folder_frame, text="path", width=50, height=1, bg="lightgrey", anchor=W)
		self.clip_folder_path_label.pack(side=LEFT, fill=X, padx=2, pady=2)
		# browse button
		self.browse_button1 = Button(self.clip_folder_frame, text="Browse Folder", relief="raised", bg=self.main_button_color, fg="white")
		self.browse_button1['command'] = self.openClipFolderDialog
		self.browse_button1.pack(side=LEFT)

		# clip data base folder path label
		self.clip_data_path_label = Label(self.clip_data_folder_frame, text="path", width=50, height=1, bg="lightgrey", anchor=W)
		self.clip_data_path_label.pack(side=LEFT, fill=X, padx=2, pady=2)
		# browse button
		self.browse_button2 = Button(self.clip_data_folder_frame, text="Browse Folder", relief="raised", bg=self.main_button_color, fg="white")
		self.browse_button2['command'] = self.openDataFolderDialog
		self.browse_button2.pack(side=LEFT)

		# validation button
		self.validate_button = Button(self.validation_frame, text="Save and Exit", relief="raised", bg=self.main_button_color, fg="white")
		self.validate_button['command'] = lambda window=self.sub_win:self.saveAndExitPreferences(window)
		self.validate_button.pack(side=TOP)

	def openClipFolderDialog(self):
		self.clip_video_folder_path =  filedialog.askdirectory()
		self.clip_folder_path_label['text'] = self.clip_video_folder_path

	def openDataFolderDialog(self):
		self.clip_data_base_file_path =  filedialog.askdirectory()
		self.clip_data_path_label['text'] = self.clip_data_base_file_path

	def saveAndExitPreferences(self, window):
		#self.write_user_data()
		#self.loadClipDataBase()
		#self.clip_name_list = self.getClipList()
		window.destroy()

# --------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	app = App()
	app.root.mainloop()