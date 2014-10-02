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

from PyQt5.QtGui import QFont, QDesktopServices

import fa
#BUGREPORT_URL = 'http://thygrrr.de/faforward.php'
BUGREPORT_USER = 'pre-login'

from util import VERSION_STRING, APPDATA_DIR, PERSONAL_DIR, LOG_FILE_GAME, LOG_FILE_FAF, readfile,\
    readlines
from PyQt5 import QtCore
from PyQt5.QtWidgets import *

import hashlib

HELP_URL = "http://www.faforever.com/forums/viewforum.php?f=3"
TICKET_URL = "http://bitbucket.org/thepilot/modular-client/issues"

class ReportDialog(QDialog):
    def __init__(self, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)
        
        dialog = self
                
        self.title = u"[auto] Report from " + BUGREPORT_USER
        self.hash = hashlib.md5(self.title)
        
        dialog.setWindowTitle(self.title)
        dialog.setLayout(QVBoxLayout())
        label = QLabel()
        label.setText("<b>Send us logs to help us find bugs!</b><br/><br/>Thanks for opting to report a bug.<br/><br/>")
        label.setWordWrap(True)
        dialog.layout().addWidget(label)

#        label = QLabel()
#        label.setText("<b>This is what happened</b> (explain what happened, and how)")
#        label.setWordWrap(False)
#        dialog.layout().addWidget(label)

#        self.report = QTextEdit()
#        report = self.report
#        report.append("type here")
#        dialog.layout().addWidget(report)
        
        label = QLabel()
        label.setText("<b>These are the partial logs</b>")
        label.setWordWrap(False)
        dialog.layout().addWidget(label)
        self.box = QTextEdit()
        box = self.box
        box.setReadOnly(True)
        try:
            box.setFont(QFont("Lucida Console", 8))
            box.append(u"\n**FAF Username:** " + BUGREPORT_USER)
            box.append(u"\n**FAF Version:** " + VERSION_STRING)
            box.append(u"\n**FAF Directory:** " + APPDATA_DIR)
            box.append(u"\n**FA Path:** " + str(fa.gamepath))
            box.append(u"\n**Home Directory:** " + PERSONAL_DIR)
            box.append(u"")
            box.append(u"\n**FA Forever Log (last 128 lines):**")
            box.append(u"{{{")
            try:
                box.append("\n".join(readlines(LOG_FILE_FAF, False)[-128:]))
            except:
                box.append(unicode(LOG_FILE_FAF))
                box.append(u"empty or not readable")
                
            box.append(u"}}}")
            box.append(u"")
            box.append(u"\n**Forged Alliance Log (full):**")
            box.append(u"{{{")
            try:
                box.append(readfile(LOG_FILE_GAME, False))
            except:
                box.append(unicode(LOG_FILE_GAME))
                box.append(u"empty or not readable")
            box.append(u"}}}")
            box.append(u"")
        except:
            box.append(u"\n**(Exception raised while writing debug vars)**")
            pass

        dialog.layout().addWidget(box)
        self.sendButton = QPushButton("\nReport this error\n")
        self.sendButton.pressed.connect(self.postReport) 
        dialog.layout().addWidget(self.sendButton)
        
        label = QLabel()
        label.setText("<b>Do you want to continue, or get help in the forums?</b><br/><i>(thanks for helping us make FAF better)</i>")
        label.setWordWrap(False)
        dialog.layout().addWidget(label)
        
        self.buttons = QDialogButtonBox()
        buttons = self.buttons        
        buttons.addButton("Close", QDialogButtonBox.AcceptRole)
        buttons.addButton("Help", QDialogButtonBox.HelpRole)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        buttons.helpRequested.connect(dialog.techSupport)
        dialog.layout().addWidget(buttons)        
    
        self.setModal(False)
    
    
    @QtCore.pyqtSlot()
    def techSupport(self):
        QDesktopServices.openUrl(QtCore.QUrl(HELP_URL))


    @QtCore.pyqtSlot()
    def postReport(self):
        QDesktopServices.openUrl(QtCore.QUrl(HELP_URL))
#            self.sendButton.setEnabled(False)
#            self.sendButton.setText("\nSending...\n")
#            QApplication.processEvents()
#            
#            import urllib
#            import urllib2
#
#            #A simple POST forwarder sends these to the REST Api of Bitbucket
#            url = BUGREPORT_URL
#            
#            content = self.report.toPlainText() + u'\n\n\n' + self.box.toPlainText()
#            data = urllib.urlencode({
#                                        'title': self.title.encode("utf-8"),
#                                        'content': content.encode("utf-8"),
#                                        'hash' : self.hash
#                                     })
#            request = urllib2.Request(url=url, data=data)
#            urllib2.urlopen(request)
#            self.sendButton.setText("\nThanks!\n")
#        except:
#            logger.error("Error sending bug report!", exc_info = sys.exc_info())
#            self.sendButton.setText("\nFailed. :( Click Help and tell us about it!\n")
#            pass

        
