import json
import os
import shutil
from Addons import checklistcombobox
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkinter import font as tkFont
from datetime import datetime


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
		self.leftFrame = LabelFrame(self.root, text="TAG", font=self.main_font_size8, labelanchor="n", borderwidth=3, height=100, width=100, fg=self.font_color, bg=self.main_theme)
		self.leftFrame.pack(fill=BOTH, expand=1, side=LEFT, padx=0, pady=0)

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