# -------------------------------------------------------------------------------
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
# -------------------------------------------------------------------------------


# Bug Reporting

CRASH_REPORT_USER = "pre-login"

import fa

from . import APPDATA_DIR, PERSONAL_DIR, VERSION_STRING, LOG_FILE_FAF, \
    readlines
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QDesktopServices
from PyQt5.QtWidgets import *

import traceback
import hashlib


HELP_URL = "http://www.faforever.com/forums/viewforum.php?f=3"
TICKET_URL = "https://github.com/FAForever/lobby/issues"

class CrashDialog(QDialog):
    def __init__(self, exc_info, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)

        exc_type, exc_value, traceback_object = exc_info

        dialog = self
        
        
        dialog.setLayout(QVBoxLayout())
        label = QLabel()
        label.setText("An Error has occurred in FAF.<br><br>"
        "You can report it by clicking the ticket button. <b>Please check if that error is new first !</b>")
        
        label.setWordWrap(True)
        dialog.layout().addWidget(label)

        label = QLabel()
        label.setText("<b>This is what happened (but please add your own explanation !)</b>")
        label.setWordWrap(False)
        dialog.layout().addWidget(label)

        self.trace = "".join(traceback.format_exception(exc_type, exc_value, traceback_object, 10))
        self.hash = hashlib.md5(self.trace.encode()).hexdigest()

        self.title = "[auto] Crash from " + CRASH_REPORT_USER + ": " + str(exc_value)

        dialog.setWindowTitle(self.title)
        
        self.box = QTextEdit()
        box = self.box
        try:
            box.setFont(QFont("Lucida Console", 8))
            box.append("\n**FAF Username:** " + CRASH_REPORT_USER)
            box.append("\n**FAF Version:** " + VERSION_STRING)
            box.append("\n**FAF Directory:** " + APPDATA_DIR)
            box.append("\n**FA Path:** " + str(fa.gamepath))
            box.append("\n**Home Directory:** " + PERSONAL_DIR)
        except Exception:
            box.append("\n**(Exception raised while writing debug vars)**")
            pass

        box.append("")
        box.append("\n**FA Forever Log (last 128 lines):**")
        box.append("{{{")
        try:
            box.append("\n".join(readlines(LOG_FILE_FAF, False)[-128:]))
        except Exception:
            box.append(str(LOG_FILE_FAF))
            box.append("empty or not readable")

        box.append("\n**Stack trace:**")
        box.append("{{{")
        box.append(self.trace)
        box.append("}}}")
        box.append("")

        dialog.layout().addWidget(box)
        self.sendButton = QPushButton("\nOpen ticket system.\n")
        self.sendButton.pressed.connect(self.post_report)
        dialog.layout().addWidget(self.sendButton)

        label = QLabel()
        label.setText("<b></b><br/><i>(please note that the error may be fatal, proceed at your own risk)</i>")
        label.setWordWrap(False)
        dialog.layout().addWidget(label)
        
        self.buttons = QDialogButtonBox()
        buttons = self.buttons        
        buttons.addButton("Continue", QDialogButtonBox.AcceptRole)
        buttons.addButton("Close FAF", QDialogButtonBox.RejectRole)
        buttons.addButton("Help", QDialogButtonBox.HelpRole)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        buttons.helpRequested.connect(self.tech_support)
        dialog.layout().addWidget(buttons)

    @QtCore.pyqtSlot()
    def tech_support(self):
        QDesktopServices().openUrl(QtCore.QUrl(HELP_URL))

    @QtCore.pyqtSlot()
    def post_report(self):
        QDesktopServices().openUrl(QtCore.QUrl(TICKET_URL))
