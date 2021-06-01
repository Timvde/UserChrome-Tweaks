#!/usr/bin/env python3
import sys
import logging
import argparse
import re
import json
from PyQt5.QtWidgets import \
	QWidget, \
	QPushButton, \
	QHBoxLayout, \
	QVBoxLayout, \
	QApplication,\
	QTreeWidget, \
	QTreeWidgetItem, \
	QLabel, \
	QTableWidget, \
	QTableWidgetItem, \
	QGroupBox, \
	QMessageBox, \
	QFileDialog

from PyQt5.QtCore import \
	QDir, \
	QFile, \
	Qt

vcount = {2: logging.DEBUG,
		  1: logging.INFO,
		  None: logging.WARNING}

#Argument parser
parser = argparse.ArgumentParser(description='userChrome tweak manager for Firefox browser..')
parser.add_argument("-v", "--verbose", help="Verbose output.", action="count")
args = parser.parse_args()

logging.basicConfig(level=vcount[args.verbose])

class MoveButton(QPushButton):
	def __init__(self):
		super().__init__()
		self.setFixedSize(48, 48)

class ButtonBox(QVBoxLayout):
	def __init__(self):
		super().__init__()
		self.buttonUp = MoveButton()
		self.buttonDown = MoveButton()
		self.buttonLeft = MoveButton()
		self.buttonRight = MoveButton()
		
		self.buttonUp.setText("\u21e7")
		self.buttonDown.setText("\u21e9")
		self.buttonLeft.setText("-")
		self.buttonRight.setText("+")
		
		self.addStretch()
		self.addWidget(self.buttonRight)
		self.addWidget(self.buttonLeft)
		self.addWidget(self.buttonUp)
		self.addWidget(self.buttonDown)
		self.addStretch()
		
	def setEnable(self, enabled):
		logging.debug("enabling button...")
		self.buttonUp.setEnabled(enabled)
		logging.debug("enabling button...")
		self.buttonDown.setEnabled(enabled)
		logging.debug("enabling button...")
		self.buttonRight.setEnabled(enabled)
		logging.debug("enabling button...")
		self.buttonLeft.setEnabled(enabled)

class FilesBox(QHBoxLayout):
	def __init__(self):
		super().__init__()
		self.availableTweaks = QTreeWidget()
		self.availableTweaks.setHeaderLabel("Available tweaks")
		self.availableTweaks.itemClicked.connect(self.availTwkClick)
		self.availableTweaks.itemDoubleClicked.connect(self.addTweak)
		
		self.buttonBox = ButtonBox()
		self.buttonBox.buttonRight.clicked.connect(self.addTweak)
		self.buttonBox.buttonLeft.clicked.connect(self.removeTweak)
		self.buttonBox.buttonDown.clicked.connect(self.downTweak)
		self.buttonBox.buttonUp.clicked.connect(self.upTweak)
		
		self.selectedTweaks = QTreeWidget()
		self.selectedTweaks.setColumnCount(3)
		self.selectedHeaders = ["", "Category", "Name"]
		self.selectedTweaks.setHeaderLabels(self.selectedHeaders)
		self.resizeColumns()
		
		self.addWidget(self.availableTweaks)
		self.addItem(self.buttonBox)
		self.addWidget(self.selectedTweaks)
		
		self.tweaksAdded = {}
	
	def availTwkClick(self):
		if self.availableTweaks.currentItem().parent() is None:
			logging.debug("Tweak category selected: %s/", self.availableTweaks.currentItem().text(0))
		else:
			logging.debug("Tweak selected: %s/%s", self.availableTweaks.currentItem().parent().text(0), self.availableTweaks.currentItem().text(0))
	
	def addTweak(self):
		if self.availableTweaks.currentItem().parent() is not None:
			tweakName = self.availableTweaks.currentItem().text(0)
			tweakCat = self.availableTweaks.currentItem().parent().text(0)
			self.tweaksAdded[tweakCat + tweakName] = QTreeWidgetItem(self.selectedTweaks)
			self.tweaksAdded[tweakCat + tweakName].setCheckState(0, 2)
			self.tweaksAdded[tweakCat + tweakName].setText(1, tweakCat)
			self.tweaksAdded[tweakCat + tweakName].setText(2, tweakName)
			self.resizeColumns()
			logging.debug("Tweak added: %s/%s", tweakCat, tweakName)
			
	def removeTweak(self):
		if self.selectedTweaks.currentItem() is not None:
			tweakName = self.selectedTweaks.currentItem().text(2)
			tweakCat = self.selectedTweaks.currentItem().text(1)
			logging.debug("Removing %s", self.selectedTweaks.indexOfTopLevelItem(self.selectedTweaks.selectedItems()[0]))
			self.selectedTweaks.takeTopLevelItem(self.selectedTweaks.indexOfTopLevelItem(self.selectedTweaks.selectedItems()[0]))
			self.resizeColumns()
			logging.debug(self.tweaksAdded[tweakCat + tweakName])
			logging.debug("Tweak removed: %s/%s", tweakCat, tweakName)
		
	def resizeColumns(self):
		self.selectedTweaks.resizeColumnToContents(0)
		self.selectedTweaks.resizeColumnToContents(1)
		self.selectedTweaks.resizeColumnToContents(2)
		
	def downTweak(self):
		tweakName = self.selectedTweaks.currentItem().text(2)
		tweakCat = self.selectedTweaks.currentItem().text(1)
		logging.debug("Moving down %s", self.selectedTweaks.indexOfTopLevelItem(self.selectedTweaks.selectedItems()[0]))
		selectedAdded = self.selectedTweaks.selectedItems()[0]
		indexOfSelected = self.selectedTweaks.indexOfTopLevelItem(selectedAdded)
		self.selectedTweaks.takeTopLevelItem(indexOfSelected)
		self.selectedTweaks.insertTopLevelItem(indexOfSelected+1, selectedAdded)
		self.selectedTweaks.setCurrentItem(selectedAdded)
		logging.debug(self.tweaksAdded[tweakCat + tweakName])
		logging.debug("Tweak moved down: %s/%s", tweakCat, tweakName)
		
	def upTweak(self):
		tweakName = self.selectedTweaks.currentItem().text(2)
		tweakCat = self.selectedTweaks.currentItem().text(1)
		logging.debug("Moving up %s", self.selectedTweaks.indexOfTopLevelItem(self.selectedTweaks.selectedItems()[0]))
		selectedAdded = self.selectedTweaks.selectedItems()[0]
		indexOfSelected = self.selectedTweaks.indexOfTopLevelItem(selectedAdded)
		self.selectedTweaks.takeTopLevelItem(indexOfSelected)
		self.selectedTweaks.insertTopLevelItem(indexOfSelected-1, selectedAdded)
		self.selectedTweaks.setCurrentItem(selectedAdded)
		logging.debug(self.tweaksAdded[tweakCat + tweakName])
		logging.debug("Tweak moved up: %s/%s", tweakCat, tweakName)
		

class LayoutBox(QVBoxLayout):
	def __init__(self):
		super().__init__()
		self.profileGroup = QGroupBox("Profile")
		self.profileLabel = QLabel("none")
		self.profileSelect = QPushButton("Open...")
		self.profileSelect.clicked.connect(self.openProfileClick)
		self.profileSave = QPushButton("Save")
		self.profileSave.clicked.connect(self.saveProfileClick)
		self.profileSave.setEnabled(False)
		self.profileBox = QHBoxLayout()
		self.profileBox.addWidget(self.profileLabel)
		self.profileBox.addStretch()
		self.profileBox.addWidget(self.profileSelect)
		self.profileBox.addWidget(self.profileSave)
		self.profileGroup.setLayout(self.profileBox)
		
		self.filesBox = FilesBox()
		self.filesBox.buttonBox.setEnable(False) #
		self.filesBox.availableTweaks.setEnabled(False)#
		self.filesBox.selectedTweaks.setEnabled(False)#
		
		self.filesBox.availableTweaks.itemClicked.connect(self.availClick)
		self.filesBox.selectedTweaks.itemClicked.connect(self.selectClick)
		
		self.descriptionGroup = QGroupBox("Tweak description")
		self.descriptionGroup.setMinimumHeight(50)
		self.description = QLabel("")
		self.description.setTextInteractionFlags(Qt.TextInteractionFlags(5))
		
		self.descriptionBox = QHBoxLayout()
		self.descriptionBox.addWidget(self.description)
		self.descriptionGroup.setLayout(self.descriptionBox)
		
		self.addWidget(self.profileGroup)
		self.addItem(self.filesBox)
		self.addWidget(self.descriptionGroup)
		self.profileDir = QDir()
		self.profilePathDialog = QFileDialog()
		self.profilePath = ""
		self.appDir = QDir().current()
	
	def openProfileClick(self):
		#Button Open... click
		self.profilePath = self.profilePathDialog.getExistingDirectory(self.profileSelect, "Select Firefox profile")
		logging.debug("Selected directory: \"%s\"", self.profilePath)
		if self.profilePath != "":
			self.selectedProfile = QDir(self.profilePath)
			self.firefoxDir = QDir(self.profilePath)
			logging.debug("Selected profile qdir: %s", self.selectedProfile.path())
			self.firefoxDir.cdUp()
			self.profilesFile = QFile(self.firefoxDir.path() + "/profiles.ini")
			logging.debug("Profiles file: %s", self.profilesFile.fileName())
			logging.debug("Profiles file exists: %s", self.profilesFile.exists())
			logging.debug("Firefox folder: %s", self.firefoxDir.dirName())
			# Basic check if parent directory is named 'firefox' and contains a file named 'profiles.ini'
			#if self.firefoxDir.dirName() == "firefox" and self.profilesFile.exists():
			if True:
				self.profilePath = self.profilePath
				self.profileLabel.setText(self.profilePath)
				
				self.filesBox.buttonBox.setEnable(True)
				self.filesBox.availableTweaks.setEnabled(True)
				self.filesBox.selectedTweaks.setEnabled(True)
				self.profileSave.setEnabled(True)
				
				self.profileDir.setPath(self.profilePath)
				logging.debug("Profile dirs: %s", self.profileDir.entryList())
				self.userChrome = QFile(self.profilePath + "/chrome/userChrome.css")
				self.userFFSettings = QFile(self.profilePath + "/chrome/userFirefox.json")
				logging.debug("userChrome exists: %s", self.userChrome.exists())
				if self.userChrome.exists() and not self.userFFSettings.exists():
					self.backupChrome = QMessageBox()
					self.backupChrome.setIcon(QMessageBox.Question)
					self.backupChrome.setText("userChrome.css file already exists in this profile. This may be overwritten. Do you want to make a backup?")
					self.backupChrome.setStandardButtons(QMessageBox.StandardButtons(81920)) #yes, no
					self.backupChrome.exec()
					logging.debug("Dialog result: %s", self.backupChrome.result())
					if self.backupChrome.result() == 16384: #yes
						logging.debug("Backing up userChrome")
						self.backupDone = QMessageBox()
						self.backupFile = QFile(self.profilePath + "/chrome/userChrome.css~")
						logging.debug("Backup file: %s", self.backupFile.fileName())
						logging.debug("Backup exists: %s", self.backupFile.exists())
						if self.backupFile.exists():
							logging.debug("Backup already exists")
							self.backupDone.setIcon(QMessageBox.Warning)
							self.backupDone.setText("Backup already exists. The file was NOT overwritten and new backup not made.")
						else:
							if self.userChrome.copy(self.profilePath + "/chrome/userChrome.css~"):
								self.backupDone.setIcon(QMessageBox.Information)
								self.backupDone.setText("Backed up to 'userChrome.css~'")
							else:
								self.backupDone.setIcon(QMessageBox.Critical)
								self.backupDone.setText("Backing up failed.")
						self.backupDone.exec()
					elif self.backupChrome.result() == 65536: #no
						logging.debug("Not backing up userChome")
				# Load existing settings
				try:
					with open(self.profilePath + "/chrome/userFirefox.json") as uFP:
						savedTweaks = json.load(uFP)
					logging.debug("Loaded json settings: %s", savedTweaks)
					for loadedTweak in savedTweaks:
						logging.debug("Loaded tweak. check: %i, category: %s, name: %s", loadedTweak["Enabled"], loadedTweak["Category"], loadedTweak["Name"])
						tweakCat = loadedTweak["Category"]
						tweakName = loadedTweak["Name"]
						self.filesBox.tweaksAdded[tweakCat + tweakName] = QTreeWidgetItem(self.filesBox.selectedTweaks)
						self.filesBox.tweaksAdded[tweakCat + tweakName].setCheckState(0, loadedTweak["Enabled"])
						self.filesBox.tweaksAdded[tweakCat + tweakName].setText(1, tweakCat)
						self.filesBox.tweaksAdded[tweakCat + tweakName].setText(2, tweakName)
				except FileNotFoundError:
					pass
				self.filesBox.resizeColumns()
			else:
				self.noProfile = QMessageBox()
				self.noProfile.setIcon(QMessageBox.Warning)
				self.noProfile.setText("The selected directory does not appear to be a valid Firefox profile. Profiles are usually located at '~/.mozilla/firefox/xxxx' and is most likely a hidden directory.")
				self.noProfile.exec()
			
	def availClick(self):
		if self.filesBox.availableTweaks.currentItem().parent() is not None:
			tweakName = self.filesBox.availableTweaks.currentItem().text(0)
			tweakCat = self.filesBox.availableTweaks.currentItem().parent().text(0)
			self.showDesc(tweakCat, tweakName)
		
	def selectClick(self):
		try:
			tweakName = self.filesBox.selectedTweaks.currentItem().text(2)
			tweakCat = self.filesBox.selectedTweaks.currentItem().text(1)
			self.showDesc(tweakCat, tweakName)
		except:
			pass
	def showDesc(self, category, name):
		logging.debug("Showing description for %s/%s: ", category, name)
		currentDir = QDir().current().path()
		tweakPath = currentDir + "/" + category + "/" + name
		logging.debug("Loading %s", tweakPath)
		tweakDesc = ""
		descLines = 0
		with open(tweakPath) as tweakContent:
			for line in tweakContent:
				if (re.search("^(\/\* ?)|( \* ?)|( \*\/)", line) is not None):
					if len(line) > 3:
						trimmedLine = line[3:]
						tweakDesc += trimmedLine
						descLines += 1
				else:
					break
		logging.debug("Description: %s", tweakDesc)
		self.description.setText(tweakDesc)
		logging.debug("Desc lines: %i", descLines)
		
	def saveProfileClick(self):
		logging.debug("Saving profile")
		self.saveQuestion = QMessageBox()
		self.saveQuestion.setIcon(QMessageBox.Question)
		self.saveQuestion.setStandardButtons(QMessageBox.StandardButtons(81920)) #yes, no
		self.saveQuestion.setText("Do you want to apply selected tweaks and overwrite userChrome?")
		self.saveQuestion.exec()
		self.saveCSS = ""
		if self.saveQuestion.result() == 16384: #yes
			logging.debug("Saving userChrome")
			selTweaksNumber = self.filesBox.selectedTweaks.topLevelItemCount()
			savingTweaks = []
			for i in range(selTweaksNumber):
				currentSavingTweak = self.filesBox.selectedTweaks.topLevelItem(i)
				currentSavingData = {}
				currentSavingData["Enabled"] = currentSavingTweak.checkState(0)
				currentSavingData["Category"] = currentSavingTweak.text(1)
				currentSavingData["Name"] = currentSavingTweak.text(2)
				logging.debug("Tweak cat %s, name %s, selected %s", currentSavingData["Category"], currentSavingData["Name"], currentSavingData["Enabled"])
				savingTweaks.append(currentSavingData)
				if currentSavingData["Enabled"] == 2:
					with open(self.appDir.path() + "/" + currentSavingData["Category"] + "/" + currentSavingData["Name"]) as twkFile:
						self.saveCSS += twkFile.read() + "\n"
			logging.debug("Selected tweaks: %s", savingTweaks)
			with open(self.profilePath + "/chrome/userFirefox.json", "w") as fp:
				json.dump(savingTweaks, fp)
			logging.debug("userChrome.css: %s", self.saveCSS)
			with open(self.profilePath + "/chrome/userChrome.css", "w") as fp:
				fp.write(self.saveCSS)
		elif self.saveQuestion.result() == 65536: #no
			logging.debug("Not saving userChrome.")

class UserFirefox(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
	
	def initUI(self):
		self.setWindowTitle("userFirefox - userChrome tweak manager")
		self.setGeometry(300, 300, 640, 640)
		self.layoutBox = LayoutBox()
		self.setLayout(self.layoutBox)
		currentDir = QDir().current()
		logging.info("Current application dir: %s", currentDir.path())
		currentDir.setFilter(QDir.Filters(24577)) #filter only dirs 0x001 and no dots 0x2000 and 0x4000 results to 0d24577
		tweakCats = currentDir.entryList()
		tweaksAvail = {}
		tweaksTree = {}
		logging.debug("List of tweak categoriess: %s", tweakCats)
		for tCat in tweakCats:
			categoryDir = QDir()
			categoryDir.setPath(currentDir.path())
			categoryDir.cd(tCat)
			categoryDir.setFilter(QDir.Filters(2)) #filter files 0x002 results to 0d2
			logging.debug("Tweaks in category %s are %s", tCat, categoryDir.entryList())
			tweaksAvail[tCat] = categoryDir.entryList()
		logging.info("Dictionary of all available tweaks: %s", tweaksAvail)
		for tCat in tweaksAvail:
			logging.debug(tCat)
			tweaksTree["_uFFTree"] = {}
			tweaksTree[tCat] = QTreeWidgetItem(self.layoutBox.filesBox.availableTweaks)
			tweaksTree[tCat].setText(0, tCat)
			for tName in tweaksAvail[tCat]:
				tweaksTree["_uFFTree"][tName] = QTreeWidgetItem(tweaksTree[tCat])
				tweaksTree["_uFFTree"][tName].setText(0, tName)
		#qtreetop = QTreeWidgetItem(self.layoutBox.filesBox.availableTweaks)
		#qtreetop.setText(0, "baf")
		self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    userFirefox = UserFirefox()
    sys.exit(app.exec_())
