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

import logging

from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from games.gameitem import GameItem, GameItemDelegate
import modvault
from fa import maps
import util

from client.GamesService import GamesService

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

RANKED_SEARCH_EXPANSION_TIME = 10000 #milliseconds before search radius expands

SEARCH_RADIUS_INCREMENT = 0.05
SEARCH_RADIUS_MAX = 0.25

FormClass, BaseClass = util.loadUiType("games/host.ui")


class HostgameWidget(FormClass, BaseClass):
    def __init__(self, client, parent, *args, **kwargs):
        BaseClass.__init__(self, *args, **kwargs)

        self.setupUi(self)
        self.parent = parent
        
        self.parent.options = []

        self.client = client

        item_options = {}

        if len(item_options) == 0 :
            self.optionGroup.setVisible(False)
        else :
            group_layout = QVBoxLayout()
            self.optionGroup.setLayout(group_layout)
            
            for option in item_options :
                checkBox = QCheckBox(self)
                checkBox.setText(option)
                checkBox.setChecked(True)
                group_layout.addWidget(checkBox)
                self.parent.options.append(checkBox)
        
        self.setStyleSheet(self.parent.client.styleSheet())
        
        self.setWindowTitle ( "Hosting Game " )
        self.titleEdit.setText ( self.parent.gamename )
        self.passEdit.setText ( self.parent.gamepassword )
        self.game = GameItem(0)
        self.gamePreview.setItemDelegate(GameItemDelegate(self))
        self.gamePreview.addItem(self.game)

        nickname = self.parent.client.login

        self.message = {}
        self.message['Title'] = self.parent.gamename
        self.message['host'] = {'username':self.parent.client.login}
        self.message['teams'] = {1:[self.parent.client.login]}
#        self.message.get('access', 'public')
        self.message['featured_mod'] = "faf"
        self.message['mapname'] = self.parent.gamemap
        self.message['GameState'] = "Lobby"
        self.message["GameOption"] = {"Slots": 12}

        msg = self.message

        msg["PlayerOption"] = {}
        msg["PlayerOption"][1] = {"PlayerName": nickname,
                                  "Team": 1}
        self.game.update(self.message, self.parent.client)
        
        i = 0
        index = 0
        if self.parent.canChooseMap == True:
            allmaps = dict()
            for map in list(maps.maps.keys()) + maps.getUserMaps():
                allmaps[map] = maps.getDisplayName(map)
            for (map, name) in sorted(iter(allmaps.items()), key=lambda x: x[1]):
                if map == self.parent.gamemap :
                    index = i
                self.mapList.addItem(name, map)
                i = i + 1
            self.mapList.setCurrentIndex(index)
        else:
            self.mapList.hide()
            
        icon = maps.preview(self.parent.gamemap, True)

        if not icon:
            icon = util.icon("games/unknown_map.png", False, True)
                

        self.mods = {}
        #this makes it so you can select every non-ui_only mod
        for mod in modvault.getInstalledMods():
            if mod.ui_only:
                continue
            self.mods[mod.totalname] = mod
            self.modList.addItem(mod.totalname)

        names = [mod.totalname for mod in modvault.getActiveMods(uimods=False)]
        logger.debug("Active Mods detected: %s" % str(names))
        for name in names:
            l = self.modList.findItems(name, QtCore.Qt.MatchExactly)
            logger.debug("found item: %s" % l[0].text())
            if l: l[0].setSelected(True)
            
        #self.mapPreview.setPixmap(icon)
        
        self.mapList.currentIndexChanged.connect(self.mapChanged)
        self.hostButton.clicked.connect(self._onHostButtonClicked)
        self.titleEdit.textChanged.connect(self.updateText)
        self.modList.itemClicked.connect(self.modclicked)

    def _onHostButtonClicked(self):
        from session.GameSession import GameSession

        from fa.check import check

        check('faf')
        self.client.game_session = sess = GameSession()

        sess.addArg('windowed', 1024, 768)
        sess.addArg('showlog')

        sess.addArg('mean', 1000)
        sess.addArg('deviation', 0)

        sess.addArg('init', 'init_test.lua')

        sess.setTitle(self.message['Title'])

        sess.setMap(self.message["mapname"])
        sess.setLocalPlayer(self.client.login, self.client.user_id)

        sess.setFAFConnection(self.client.lobby_ctx)

        sess.start()

        self.done(0)

    def updateText(self, text):
        self.message['Title'] = text
        self.game.update(self.message, self.parent.client)

    def hosting(self):
        self.parent.saveGameName(self.titleEdit.text().strip())
        self.parent.saveGameMap(self.parent.gamemap)
        if self.passCheck.isChecked() :
            self.parent.ispassworded = True
            self.parent.savePassword(self.passEdit.text())
        else :
            self.parent.ispassworded = False
        self.done(1)

    def mapChanged(self, index):
        self.parent.gamemap = self.mapList.itemData(index)
        icon = maps.preview(self.parent.gamemap, True)
        if not icon:
            icon = util.icon("games/unknown_map.png", False, True)
        #self.mapPreview.setPixmap(icon)
        self.message['mapname'] = self.parent.gamemap
        self.game.update(self.message, self.parent.client)

    @QtCore.pyqtSlot(QListWidgetItem)
    def modclicked(self, item):
        #item.setSelected(not item.isSelected())
        logger.debug("mod %s clicked." % str(item.text()))
