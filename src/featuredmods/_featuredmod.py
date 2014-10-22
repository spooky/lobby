#-------------------------------------------------------------------------------
# Copyright (c) 2012 Gael Honorez.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the GNU Public License v3.0
# which accompanies this distribution, and is available at
# http://www.gnu.org/licenses/gpl.html
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#-------------------------------------------------------------------------------


import os

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtNetwork import *

import util

import logging
logger = logging.getLogger(__name__)



FormClass, BaseClass = util.loadUiType("featuredmods/featuredmods.ui")



class FeaturedModsWidget(FormClass, BaseClass):
    def __init__(self, client, *args, **kwargs):
        
        BaseClass.__init__(self, *args, **kwargs)        
        
        self.setupUi(self)

        self.client = client
        
        self.currentMod     = None
        self.modFiles       = None
        self.versionFiles   = None

        self.login          = None
        self.password       = None
        
        self.fileToUpload   = None
        self.currentUid     = None
        
        self.ftp = QNetworkAccessManager(self)
        self.ftp.finished.connect(self.ftpCommandFinished)
        self.ftp.listInfo.connect(self.addToList)
        self.ftp.dataTransferProgress.connect(self.updateDataTransferProgress)
        self.ftplist = []
        
        self.progressDialog = QProgressDialog(self)
        self.progressDialog.canceled.connect(self.cancelUpload)
        
        
        
        self.client.featuredModManager.connect(self.manageMod)
        self.client.featuredModManagerInfo.connect(self.manageModInfo)
        
        self.filesTable.cellPressed.connect(self.fileClicked)
        self.versionTable.cellPressed.connect(self.versionClicked)
        
        self.filesTable.horizontalHeader().setStretchLastSection ( True )
        self.versionTable.horizontalHeader().setStretchLastSection ( True )
        
        self.setStyleSheet(self.client.styleSheet())
        
    def cancelUpload(self):
        self.ftp.abort()

    def addToList(self, urlInfo):
        self.ftplist.append(urlInfo.name())

    def ftpCommandFinished(self, _, error):
        if self.ftp.currentCommand() == QtNetwork.QFtp.ConnectToHost:
            if error:
                QMessageBox.information(self, "FTP",
                        "Unable to connect to the FTP server at faforever.com. ")
                logger.warn("Cannot connect to FTP")
                self.ftp.abort()       
                self.ftp.close()
                return
        
        if self.ftp.currentCommand() == QtNetwork.QFtp.Login:
            if error :
                QMessageBox.information(self, "FTP",
                        "Unable to login to the FTP. Please check your login and/or password.")
                logger.warn("Cannot login to FTP")
                self.ftp.abort()     
                self.ftp.close()
                return
            
            self.ftp.list()

        if self.ftp.currentCommand() == QtNetwork.QFtp.Put:
            if error:
                QMessageBox.information(self, "FTP",
                        "Canceled upload of %s." % self.fileToUpload.fileName())
                logger.info("Upload cancelled")
                self.fileToUpload.close()
                self.ftp.abort()
                logger.info("Deleting file")
                self.ftp.remove(os.path.basename(self.fileToUpload.fileName()))
                self.ftp.close()
            else:
                QMessageBox.information(self, "FTP",
                        "%s uploaded !" % self.fileToUpload.fileName())

                logger.info("Upload done !")
                self.fileToUpload.close()
                self.ftp.close()

                self.client.send(dict(command="mod_manager_info", action="added_file", type = self.currentUid, mod=self.currentMod, version=self.version, file=os.path.basename(self.fileToUpload.fileName())))

        if self.ftp.currentCommand() == QtNetwork.QFtp.List:
            
            filename = os.path.basename(self.fileToUpload.fileName ())
            
            if filename in self.ftplist :
                QMessageBox.information(self, "FTP",
                        "This file already exists on the server. Please rename it.")
                logger.warn("file already exists in FTP")
                self.ftp.abort()  
                self.ftp.close()
                return   

            else :
                if not self.fileToUpload.open(QtCore.QIODevice.ReadWrite):
                    QMessageBox.information(self, "FTP",
                            "Can't open this file.")
                    logger.warn("Can't open this file.")
                    self.ftp.abort() 
                    self.ftp.close()
                    return
                
                self.ftp.put(self.fileToUpload, filename)
                self.progressDialog.setLabelText("uploading %s..." % filename)
                
                self.progressDialog.show()


    def updateDataTransferProgress(self, readBytes, totalBytes):
        self.progressDialog.setMaximum(totalBytes)
        self.progressDialog.setValue(readBytes)

    def addVersionFile(self):
        text, ok = QInputDialog.getText(self, "Version number",
                "Please enter the version number :", QLineEdit.Normal, "")
                
        if ok and text != '':
            
            version = [x for x in text if x.isdigit()]
            
            if len(version) != 0 :
                self.version = int(version)
                
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                
                fileName = QFileDialog.getOpenFileName(self,
                "Select the file",
                "",
                "aLL Files (*.*)", options)
                
                if fileName:
                    
                    self.fileToUpload = QtCore.QFile(fileName)
                    self.ftp.connectToHost("faforever.com", 1980)
                    logger.debug("Connecting to FTP")
                    self.ftp.login(self.currentMod, self.password)
                    logger.debug("Logging to FTP")
                

        
    def updateTitle(self):
        self.title.setText("MOD MANAGER : %s" % self.currentMod)
        self.setWindowTitle("MOD MANAGER : %s" % self.currentMod)

    
    def versionClicked(self, row, col):
        if QApplication.mouseButtons() != QtCore.Qt.RightButton:
            return            
        
        menu = QMenu(self.versionTable)
        
        actionAdd = QAction("Add File", menu)
        # Adding to menu
        menu.addAction(actionAdd)            
        
        # Triggers
        actionAdd.triggered.connect(lambda: self.addVersionFile())
        #actionAdd.triggered.connect()
        
        #Finally: Show the popup
        menu.popup(QCursor.pos())
        
    
    def fileClicked(self, row, col):
#        if QApplication.mouseButtons() != QtCore.Qt.RightButton:
#            return            
        self.viewUpdatesFiles(row+1)
#        menu = QMenu(self.filesTable)
#        
#        
#        actionView = QAction("View Update Files", menu)
#        actionAdd = QAction("Add File", menu)
#        # Adding to menu
#        menu.addAction(actionView)
#        #menu.addAction(actionAdd)            
#        
#        # Triggers
#        actionView.triggered.connect(lambda: self.viewUpdatesFiles(row+1))
#        #actionAdd.triggered.connect()
#        
#        #Finally: Show the popup
#        menu.popup(QCursor.pos())

    def viewUpdatesFiles(self, uid):
        self.currentUid = uid
        self.versionTable.clear()
        self.versionTable.setHorizontalHeaderItem(0, QTableWidgetItem("version"))
        self.versionTable.setHorizontalHeaderItem(1, QTableWidgetItem("filename"))
                
        i = 0
        for f in self.versionFiles :
            if f["fileuid"] == uid :
                itemFile = QTableWidgetItem (f["name"])
                itemVersion = QTableWidgetItem (str(f["version"]))
                
                #self.filesTable.insertRow(uid)
                self.versionTable.setRowCount ( i+1 )
                self.versionTable.setItem ( i, 0, itemVersion )
                self.versionTable.setItem ( i, 1, itemFile ) 
                i = i + 1               
    
    def updateModFiles(self):
        ## Clearing both table
        self.filesTable.clear()
        self.versionTable.clear()
        
        self.filesTable.setHorizontalHeaderItem(0, QTableWidgetItem("path"))
        self.filesTable.setHorizontalHeaderItem(1, QTableWidgetItem("filename"))
        
        self.versionTable.setHorizontalHeaderItem(0, QTableWidgetItem("version"))
        self.versionTable.setHorizontalHeaderItem(1, QTableWidgetItem("filename"))
        
        
        self.filesTable.setRowCount(len(self.modFiles))
        for f in self.modFiles :
            itemFile = QTableWidgetItem (f["filename"])
            itemPath = QTableWidgetItem (f["path"])
            uid = f["uid"] - 1
            #self.filesTable.insertRow(uid)
            self.filesTable.setItem ( uid, 0, itemPath )
            self.filesTable.setItem ( uid, 1, itemFile )

    
    def manageModInfo(self, message):
        self.currentMod = message["mod"]
        self.modFiles       = message["mod_files"]
        self.versionFiles   = message["version_files"] 
        self.updateTitle()
        self.updateModFiles()

        
    def manageMod(self, mod):
        self.currentMod = mod
        self.updateTitle()        
        self.show()
        

        text, ok = QInputDialog.getText(self, "Password",
            "Please enter your password for this mod :", QLineEdit.Password, "")
    
        if ok and text != '':
            self.password = text        
    
            # asking for mod info
            self.client.send(dict(command="mod_manager_info", action="list", mod=self.currentMod))