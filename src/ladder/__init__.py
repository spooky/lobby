from PyQt5 import QtCore
from PyQt5.QtWebKitWidgets import *
from PyQt5 import QtWebKit
import logging
import util

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Ladder(QtCore.QObject):
    def __init__(self, client, *args, **kwargs):
        QtCore.QObject.__init__(self, *args, **kwargs)
        logger.debug("Ladder tab instantiating.")
        
        self.client = client

        self.ui = QWebView()
        
        self.client.ladderTab.layout().addWidget(self.ui)
        
        self.loaded = False
        self.client.showLadder.connect(self.reloadView)
        self.ui.loadFinished.connect(self.ui.show)
        
    @QtCore.pyqtSlot()
    def reloadView(self):
        if (self.loaded): 
            return    
        self.loaded = True
        
        self.ui.setVisible(False)

        #If a local theme CSS exists, skin the WebView with it
        if util.themeurl("ladder/style.css"):
            self.ui.settings().setUserStyleSheetUrl(util.themeurl("ladder/style.css"))

        self.ui.setUrl(QtCore.QUrl("http://faforever.com/faf/leaderboards/read-leader.php?board=global&username=%s" % (self.client.login)))
        
        
    
