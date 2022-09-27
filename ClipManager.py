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
		self.font_color = "orange"
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
		self.menubar = Menu(self.root, bg=self.main_theme, fg=self.font_color, activebackground="white", activeforeground='black')
		self.file = Menu(self.menubar, tearoff=0, background=self.main_theme, fg=self.font_color, font=self.main_font_size8)
		self.file.add_command(label="Options", command=self.openOptions)
		self.file.add_command(label="Help", command=None)
		self.menubar.add_cascade(label="File", menu=self.file)
		self.root.config(menu=self.menubar)

	# --------------------------------------------------------------------------------------------------
	# CLIP MANAGER MAIN PAGE
	def loadClipManager(self):
		# main window left frame
		self.leftFrame = LabelFrame(self.root, text="TAG", font=self.main_font_size8, labelanchor="n", borderwidth=3, height=100, width=100, fg=self.font_color, bg=self.main_theme)
		self.leftFrame.pack(fill=BOTH, expand=1, side=LEFT, padx=0, pady=0)

		# First Frame (Clip Name + Clip Info + Rename Button) NIR = NameInfoRename
		self.currentClipNIRFrame = Frame(self.leftFrame, borderwidth=0, bg=self.main_theme, relief="sunken")
		self.currentClipNIRFrame.pack(side=TOP, fill=X, expand=False)

		self.currentClipFrame = Frame(self.currentClipNIRFrame, borderwidth=0, bg=self.main_theme, relief="groove")
		self.currentClipFrame.pack(side=LEFT, fill=X, expand=True)

		self.currentClipNameEntry = Entry(self.currentClipFrame, text=self.currentClipName, font=self.main_font_size8, fg=self.font_color, bg=self.main_theme, highlightbackground="red", highlightcolor="red", state=NORMAL)
		self.currentClipNameEntry.pack(side=TOP, fill=X, expand=False)
		
		self.currentClipInfoLabel = Label(self.currentClipFrame, text=self.currentClipInfo.get(), font=self.main_font_size8, anchor="w", fg=self.font_color, bg=self.main_theme, borderwidth=1, relief="sunken")
		self.currentClipInfoLabel.pack(side=TOP, fill=X, expand=False)

		self.buttonRename = Button(self.currentClipNIRFrame, text="Rename", fg=self.font_color, font=self.main_font_size8, relief="raised", bg=self.main_theme)
		#self.buttonRename['command'] = self.buttonRename_clicked1
		self.buttonRename.pack(side=RIGHT, fill=Y)

		# --------------------------------------------------------------------------------------------------
		# Second Frame (PPNKC = Previous + Pause + Next buttons + Kill Counter)
		self.PPNKCFrame = Frame(self.leftFrame, borderwidth=0, bg=self.main_theme, relief="sunken")
		self.PPNKCFrame.pack(side=TOP, fill=X, expand=False)

		# --------------------------------------------------------------------------------------------------
		# Sub Frame PPN = Previous + Play + Next
		self.PPNFrame = LabelFrame(self.PPNKCFrame, text="Media control", font=self.main_font_size8, labelanchor="s", borderwidth=1, bg=self.main_theme, fg=self.font_color)
		#self.PPNFrame = Frame(self.PPNKCFrame, borderwidth=0, bg=self.main_theme, relief="sunken")
		self.PPNFrame.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=5)

		self.PPNCenterFrame = Frame(self.PPNFrame, borderwidth=3, bg=self.main_theme)
		self.PPNCenterFrame.pack(side=TOP)

		image = Image.open("Icons/Previous.png")
		image = image.resize((40,40))
		previousIcon = ImageTk.PhotoImage(image)
		self.previousClipButton = Button(self.PPNCenterFrame, relief="raised", bg=self.main_theme, image=previousIcon)
		self.previousClipButton.image = previousIcon
		#self.previousClipButton['command'] = self.buttonPreviousClicked
		self.previousClipButton.pack(side=LEFT, padx=5)

		image = Image.open("Icons/Play.png")
		image = image.resize((40,40))
		playIcon = ImageTk.PhotoImage(image)
		self.playButton = Button(self.PPNCenterFrame, relief="raised", bg=self.main_theme, image=playIcon)
		self.playButton.image = playIcon
		#self.playButton['command'] = self.openInDefaultPlayer
		self.playButton.pack(side=LEFT, pady=5)

		image = Image.open("Icons/Next.png")
		image = image.resize((40,40))
		next_icon = ImageTk.PhotoImage(image)
		self.nextClipButton = Button(self.PPNCenterFrame, relief="raised", bg=self.main_theme, image=next_icon)
		self.nextClipButton.image = next_icon
		#self.nextClipButton['command'] = self.buttonNextClicked
		self.nextClipButton.pack(side=LEFT, padx=5)#padx=(5,5), pady=5)

		# --------------------------------------------------------------------------------------------------
		# Sub Frame KC = Kill Counter
		self.KCFrame = LabelFrame(self.PPNKCFrame, text="Kill Counter", font=self.main_font_size8, labelanchor="s", borderwidth=1, bg=self.main_theme, fg=self.font_color)
		self.KCFrame.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=5)

		self.KCCenterFrame = Frame(self.KCFrame, borderwidth=3, bg=self.main_theme)
		self.KCCenterFrame.pack(side=TOP)

		# minus button
		buttonFont = tkFont.Font(size=16, weight="bold")
		#iconVIRTUAL = PhotoImage(width=1, height=1)
		self.buttonMINUS = Button(self.KCCenterFrame, text="-", fg="white", font=buttonFont, relief="raised", bg=self.main_theme, width=3, height=1)
		#self.buttonMINUS['command'] = self.buttonMINUSClicked
		self.buttonMINUS.pack(side=LEFT, padx=5)

		# kill count button
		buttonFont = tkFont.Font(size=16, weight="bold")
		self.buttonKILLCOUNTER = Button(self.KCCenterFrame, text=str(self.killCounter), fg="white",relief="raised", font=buttonFont, bg=self.main_theme, width=3, height=1)
		#self.buttonKILLCOUNTER['command'] = self.buttonKILLCOUNTERClicked
		#self.buttonKILLCOUNTER.bind("<Enter>", self._onEnterKillCounter)
		#self.buttonKILLCOUNTER.bind("<Leave>", self._onLeaveKillCounter)
		#self.buttonKILLCOUNTER.bind_all("<MouseWheel>", self._onMousewheel)
		self.buttonKILLCOUNTER.pack(side=LEFT)

		# plus button
		buttonFont = tkFont.Font(size=16, weight="bold")
		#iconVIRTUAL = PhotoImage(width=1, height=1)
		self.buttonPLUS = Button(self.KCCenterFrame, text="+", fg="white", font=buttonFont, relief="raised", bg=self.main_theme, width=3, height=1)
		#self.buttonPLUS['command'] = self.buttonPLUSClicked
		self.buttonPLUS.pack(side=LEFT, padx=5)



		# --------------------------------------------------------------------------------------------------
		# main window right frame
		self.rightFrame = LabelFrame(self.root, text="SEARCH", font=self.main_font_size8, labelanchor="n", borderwidth=3, height=100, width=100, fg=self.font_color, bg=self.main_theme)
		self.rightFrame.pack(fill=BOTH, expand=1, side=LEFT, padx=0, pady=0)

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