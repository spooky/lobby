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





import json
import re
import hashlib

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import util
from AuthService import AuthService


PASSWORD_RECOVERY_URL = "http://www.faforever.com/faf/forgotPass.php"
NAME_CHANGE_URL = "http://www.faforever.com/faf/userName.php"
STEAM_LINK_URL = "http://www.faforever.com/faf/steam.php"

class LoginWizard(QWizard):
    def __init__(self, client):
        QWizard.__init__(self)

        self.client = client

        self.login = client.login
        self.password = client.password
        
        self.addPage(loginPage(self))

        self.setWizardStyle(QWizard.ModernStyle)
        self.setModal(True)

        buttons_layout = [QWizard.CancelButton, QWizard.FinishButton]

        self.setButtonLayout(buttons_layout)

        self.setWindowTitle("Login")

    def accept(self):
        self.login = self.field("login").strip()
        if (self.field("password") != "!!!password!!!"): #Not entirely nicely coded, this can go into a lambda function connected to the LineEdit
            # FIXME Sheeo pass hash
            self.password = hashlib.sha256(self.field("password").strip().encode("utf-8")).hexdigest()

        self.client.login = self.field("login").strip()
        self.client.password = self.password    #this is the hash, not the dummy password
        self.client.remember = self.field("remember")
        self.client.autologin = self.field("autologin")

        self.login_reply = reply = AuthService.Login(self.login, self.password)

        reply.error.connect(self._onLoginError)
        reply.done.connect(self._onLoginReply)

        # FIXME To be asynchronous
        # self.loop = loop = QEventLoop()
        # reply.finished.connect(self.loop.quit)
        # loop.exec_(QEventLoop.AllEvents | QEventLoop.WaitForMoreEvents)
        #
        # if self._onLoginReply():
        #     QWizard.accept(self)

    def reject(self):
        QWizard.reject(self)

    def _onLoginError(self, resp):
        QMessageBox.information(self, "Login Failed", resp['statusMessage'])

    def _onLoginReply(self, resp):
        self.client.session_id = resp["session_id"]
        QWizard.accept(self)


class loginPage(QWizardPage):
    def __init__(self, parent=None, *args, **kwargs):
        QWizardPage.__init__(self, *args, **kwargs)

        self.parent= parent
        self.client = parent.client
        
        self.setButtonText(QWizard.CancelButton, "Quit")
        self.setButtonText(QWizard.FinishButton, "Login")
        
        self.setTitle("ACU ready for combat.")
        self.setSubTitle("Log yourself in, commander.")
        
        self.setPixmap(QWizard.WatermarkPixmap, util.pixmap("client/login_watermark.png"))

        loginLabel = QLabel("&User name :")
        self.loginLineEdit = QLineEdit()
        loginLabel.setBuddy(self.loginLineEdit)
        self.loginLineEdit.setText(self.client.login)

        passwordLabel = QLabel("&Password :")
        self.passwordLineEdit = QLineEdit()
        
        passwordLabel.setBuddy(self.passwordLineEdit)
        
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
                
        if (self.client.password):
            self.passwordLineEdit.setText("!!!password!!!")

        self.passwordLineEdit.selectionChanged.connect(self.passwordLineEdit.clear)               


        self.rememberCheckBox = QCheckBox("&Remember password")
        self.rememberCheckBox.setChecked(self.client.remember)
        
        self.autologinCheckBox = QCheckBox("&Automatic Login")
        self.autologinCheckBox.setChecked(self.client.autologin)
        self.autologinCheckBox.setEnabled(self.client.remember)
        
        self.rememberCheckBox.clicked.connect(self.rememberCheck)
        self.rememberCheckBox.clicked.connect(self.autologinCheckBox.setChecked)
        self.rememberCheckBox.clicked.connect(self.autologinCheckBox.setEnabled)
        
        self.createAccountBtn = QPushButton("Create new Account")
        self.renameAccountBtn = QPushButton("Rename your account")
        self.linkAccountBtn = QPushButton("Link your account to Steam")
        self.forgotPasswordBtn = QPushButton("Forgot Login or Password")
        self.reportBugBtn = QPushButton("Report a Bug")

        self.createAccountBtn.released.connect(self.createAccount)
        self.renameAccountBtn.released.connect(self.renameAccount)
        self.linkAccountBtn.released.connect(self.linkAccount)
        self.forgotPasswordBtn.released.connect(self.forgotPassword)
        self.reportBugBtn.released.connect(self.reportBug)

        self.registerField('login', self.loginLineEdit)
        self.registerField('password', self.passwordLineEdit)
        self.registerField('remember', self.rememberCheckBox)
        self.registerField('autologin', self.autologinCheckBox)


        layout = QGridLayout()

        layout.addWidget(loginLabel, 1, 0)
        layout.addWidget(self.loginLineEdit, 1, 1)
        
        layout.addWidget(passwordLabel, 2, 0)
        layout.addWidget(self.passwordLineEdit, 2, 1)

        layout.addWidget(self.rememberCheckBox, 3, 0, 1, 3)
        layout.addWidget(self.autologinCheckBox, 4, 0, 1, 3)
        layout.addWidget(self.createAccountBtn, 5, 0, 1, 3)
        layout.addWidget(self.renameAccountBtn, 6, 0, 1, 3)
        layout.addWidget(self.linkAccountBtn, 7, 0, 1, 3)
        layout.addWidget(self.forgotPasswordBtn, 8, 0, 1, 3)

        layout.addWidget(self.reportBugBtn, 10, 0, 1, 3)

        self.setLayout(layout)



    def rememberCheck(self):
        self.client.remember = self.rememberCheckBox.isChecked()
                
        
    @QtCore.pyqtSlot()
    def createAccount(self):
        wizard = creationAccountWizard(self)
        if wizard.exec_():
            #Re-load credentials after successful creation.
            self.loginLineEdit.setText(self.client.login)
            self.setField('password', "!!!password!!!")
            self.parent.password = self.client.password # This is needed because we're writing the field in accept()

    @QtCore.pyqtSlot()
    def linkAccount(self):
        QDesktopServices.openUrl(QtCore.QUrl(STEAM_LINK_URL))
        
    @QtCore.pyqtSlot()
    def renameAccount(self):
        QDesktopServices.openUrl(QtCore.QUrl(NAME_CHANGE_URL))
        
    @QtCore.pyqtSlot()
    def forgotPassword(self):
        QDesktopServices.openUrl(QtCore.QUrl(PASSWORD_RECOVERY_URL))


    @QtCore.pyqtSlot()
    def reportBug(self):
        util.ReportDialog().exec_()



class creationAccountWizard(QWizard):
    def __init__(self, parent=None):
        
        super(creationAccountWizard, self).__init__(parent)

        self.client = parent.client

        self.setOption(QWizard.DisabledBackButtonOnLastPage)
        self.addPage(IntroPage())
        self.addPage(AccountCreationPage(self))
        self.addPage(AccountCreated())


        self.setWizardStyle(QWizard.ModernStyle)

        self.setPixmap(QWizard.BannerPixmap,
                QPixmap('client/banner.png'))
        self.setPixmap(QWizard.BackgroundPixmap,
                QPixmap('client/background.png'))

        self.setWindowTitle("Create Account")



class gameSettingsWizard(QWizard):
    def __init__(self, client, *args, **kwargs):
        QWizard.__init__(self, *args, **kwargs)
        
        self.client = client

        self.settings = GameSettings()
        self.settings.gamePortSpin.setValue(self.client.gamePort)
        self.settings.checkUPnP.setChecked(self.client.useUPnP)
        self.addPage(self.settings)

        self.setWizardStyle(1)

        self.setPixmap(QWizard.BannerPixmap,
                QPixmap('client/banner.png'))
        self.setPixmap(QWizard.BackgroundPixmap,
                QPixmap('client/background.png'))

        self.setWindowTitle("Set Game Port")

    def accept(self):
        self.client.gamePort = self.settings.gamePortSpin.value()
        self.client.useUPnP = self.settings.checkUPnP.isChecked()
        self.client.savePort()
        QWizard.accept(self)


class mumbleOptionsWizard(QWizard):
    def __init__(self, client, *args, **kwargs):
        QWizard.__init__(self, *args, **kwargs)
        
        self.client = client

        self.settings = MumbleSettings()
        self.settings.checkEnableMumble.setChecked(self.client.enableMumble)
        self.addPage(self.settings)

        self.setWizardStyle(1)

        self.setPixmap(QWizard.BannerPixmap,
                QPixmap('client/banner.png'))
        self.setPixmap(QWizard.BackgroundPixmap,
                QPixmap('client/background.png'))

        self.setWindowTitle("Configure Voice")


    def accept(self):
        self.client.enableMumble = self.settings.checkEnableMumble.isChecked()
        self.client.saveMumble()
        QWizard.accept(self)



class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle("Welcome to FA Forever.")
        self.setSubTitle("In order to play, you first need to create an account.")
        self.setPixmap(QWizard.WatermarkPixmap, util.pixmap("client/account_watermark_intro.png"))

        label = QLabel("This wizard will help you in the process of account creation.<br/><br/><b>At this time, we only allow one account per computer.</b>")
        
        label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)



class AccountCreationPage(QWizardPage):
    def __init__(self, parent=None):
        super(AccountCreationPage, self).__init__(parent)

        self.parent = parent
        self.client = parent.client
        
        self.setTitle("Account Creation")
        self.setSubTitle("Please enter your desired login and password. Note that your password will not be stored on our server. Please specify a working email address in case you need to change it.")
        
        self.setPixmap(QWizard.WatermarkPixmap, util.pixmap("client/account_watermark_input.png"))

        loginLabel = QLabel("&User name :")
        self.loginLineEdit = QLineEdit()
        rxLog = QtCore.QRegExp("[A-Z,a-z]{1}[A-Z,a-z,0-9,_,-]{0,15}")
        validLog = QRegExpValidator(rxLog, self)
        self.loginLineEdit.setValidator(validLog)
        loginLabel.setBuddy(self.loginLineEdit)

        passwordLabel = QLabel("&Password :")
        self.passwordLineEdit = QLineEdit()
        passwordLabel.setBuddy(self.passwordLineEdit)

        self.passwordLineEdit.setEchoMode(2)

        passwordCheckLabel = QLabel("&Re-type Password :")
        self.passwordCheckLineEdit = QLineEdit()
        passwordCheckLabel.setBuddy(self.passwordCheckLineEdit)

        self.passwordCheckLineEdit.setEchoMode(2)

        EmailLabel = QLabel("E-mail :")
        self.EmailLineEdit = QLineEdit()
        rxMail = QtCore.QRegExp("^[a-zA-Z0-9]{1}[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$")
        validMail = QRegExpValidator(rxMail, self)
        self.EmailLineEdit.setValidator(validMail)


        self.registerField('login*', self.loginLineEdit)
        self.registerField('password*', self.passwordLineEdit)
        self.registerField('passwordCheck*', self.passwordCheckLineEdit)
        self.registerField('email*', self.EmailLineEdit)

        self.password1 = ''
        self.password2 = ''
        
        layout = QGridLayout()
                
        layout.addWidget(loginLabel, 1, 0)
        layout.addWidget(self.loginLineEdit, 1, 1)
        
        layout.addWidget(passwordLabel, 2, 0)
        layout.addWidget(self.passwordLineEdit, 2, 1)
        
        layout.addWidget(passwordCheckLabel, 3, 0)
        layout.addWidget(self.passwordCheckLineEdit, 3, 1)
        
        layout.addWidget(EmailLabel, 4, 0)
        layout.addWidget(self.EmailLineEdit, 4, 1)

        self.setLayout(layout)
#

    def validateEmail(self, email):
        if email.count("@") != 1:
            return False
        if len(email) > 6:
            if re.match("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email) != None:
                return True
        return False


    def validatePage(self):

        if self.done:
            return True

        password1 = hashlib.sha256(self.passwordLineEdit.text().encode("utf-8")).hexdigest()        
        password2 = hashlib.sha256(self.passwordCheckLineEdit.text().encode("utf-8")).hexdigest()
        
        if password1 != password2 :
            QMessageBox.information(self, "Create account","Passwords don't match!")
            return False
        
        email = self.EmailLineEdit.text()
        
        if not self.validateEmail(email) :
            QMessageBox.information(self, "Create account", "Invalid Email address!")
            return False   
        
        # check if the login is okay
        self.login = login = self.loginLineEdit.text().strip()
        self.password = password = password1

        rep = AuthService.Register(email, login, password)

        self.register_reply = rep

        # FIXME To be asynchronous
        rep.error.connect(self._onRegisterError)
        rep.done.connect(self._onRegisterSuccess)

        return False

    def _onRegisterError(self, resp):
        QMessageBox.information(self, "Create account", resp['statusMessage'])

    def _onRegisterSuccess(self, resp):
        self.client.login = self.login
        self.client.password = self.password
        self.client.session_id = resp["session_id"]

        self.done = True
        self.wizard().next()

    def onRegisterReply(self, resp):
        QEventLoop.exit()
        if 'success' not in resp:
        #if self.client.state == ClientState.REJECTED:
            self.massive_hack =  False
        else:
            self.client.session_id = resp["session_id"]
            self.massive_hack = True

class GameSettings(QWizardPage):
    def __init__(self, parent=None):
        super(GameSettings, self).__init__(parent)

        self.parent = parent
        self.setTitle("Network Settings")
        self.setPixmap(QWizard.WatermarkPixmap, util.pixmap("client/settings_watermark.png"))
        
        self.label = QLabel()
        self.label.setText('Forged Alliance needs an open UDP port to play. If you have trouble connecting to other players, try the UPnP option first. If that fails, you should try to open or forward the port on your router and firewall.<br/><br/>Visit the <a href="http://www.faforever.com/forums/viewforum.php?f=3">Tech Support Forum</a> if you need help.<br/><br/>')
        self.label.setOpenExternalLinks(True)
        self.label.setWordWrap(True)

        self.labelport = QLabel()
        self.labelport.setText("<b>UDP Port</b> (default 6112)")
        self.labelport.setWordWrap(True)
        
        self.gamePortSpin = QSpinBox()
        self.gamePortSpin.setMinimum(1024)
        self.gamePortSpin.setMaximum(65535) 
        self.gamePortSpin.setValue(6112)

        self.checkUPnP = QCheckBox("use UPnP")
        self.checkUPnP.setToolTip("FAF can try to open and forward your game port automatically using UPnP.<br/><b>Caution: This doesn't work for all connections, but may help with some routers.</b>")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.labelport)
        layout.addWidget(self.gamePortSpin)
        layout.addWidget(self.checkUPnP)
        self.setLayout(layout)


    def validatePage(self):        
        return 1

class MumbleSettings(QWizardPage):
    def __init__(self, parent=None):
        super(MumbleSettings, self).__init__(parent)

        self.parent = parent
        self.setTitle("Voice Settings")
        self.setPixmap(QWizard.WatermarkPixmap, util.pixmap("client/settings_watermark.png"))
        
        self.label = QLabel()
        self.label.setText('FAF supports the automatic setup of voice connections between you and your team mates. It will automatically move you into a channel with your team mates anytime you enter a game lobby or start a game. To enable, download and install <a href="http://mumble.sourceforge.net/">Mumble</a> and tick the checkbox below.')
        self.label.setOpenExternalLinks(True)
        self.label.setWordWrap(True)

        self.checkEnableMumble = QCheckBox("Enable Mumble Connector")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.checkEnableMumble)
        self.setLayout(layout)

    def validatePage(self):        
        return 1



class AccountCreated(QWizardPage):
    def __init__(self, *args, **kwargs):
        QWizardPage.__init__(self, *args, **kwargs)

        self.setFinalPage(True)
        self.setTitle("Congratulations!")
        self.setSubTitle("Your Account has been created.")
        self.setPixmap(QWizard.WatermarkPixmap, util.pixmap("client/account_watermark_created.png"))

        self.label = QLabel()
        self.label.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def initializePage(self):
        self.label.setText("You will be redirected to the login page.")

