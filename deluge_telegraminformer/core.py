# -*- coding: utf-8 -*-
# Copyright (C) 2023 Yuriy Shupenko <yurkinpark@gmail.com>
#
# TelegramInformer plugin template created by the Deluge Team.
#
# This file is part of TelegramInformer and is licensed under GNU GPL 3.0, or later,
# with the additional special exception to link portions of this program with
# the OpenSSL library. See LICENSE for more details.
from __future__ import unicode_literals

import logging

from deluge.core.rpcserver import export
from deluge.plugins.pluginbase import CorePluginBase
from pytgbot import Bot
from deluge import component, configmanager

log = logging.getLogger(__name__)

DEFAULT_PREFS = {
    'botApiKey': '',
    'userId': ''
}

class Core(CorePluginBase):

    bot = None

    def enable(self):
        self.config = configmanager.ConfigManager('telegraminformer.conf', DEFAULT_PREFS)
        component.get('EventManager').register_event_handler('TorrentFinishedEvent', self.on_torrent_finished_event)

    def disable(self):
        component.get("EventManager").deregister_event_handler('TorrentFinishedEvent', self.on_torrent_finished_event)

    def update(self):
        pass

    def getBot(self):
        if self.bot is None:
            log.debug("Initializing telegram bot")
            botApiKey = self.config['botApiKey']
            self.bot = Bot(botApiKey)
        return self.bot

    def on_torrent_finished_event(self, torrent_id):
        try:
            torrent_manager = component.get("TorrentManager") # type: deluge.core.torrentmanager.TorrentManager
            data = torrent_manager.torrents[torrent_id] # type : deluge.core.torrent.Torrent
            self.getBot().send_message(self.config['userId'], "Torrent " + data.filename + " finished", parse_mode='Markdown')
            log.debug("Message sent to user")
        except Exception as e:
            log.error("error in torrent finished event: %s" % e)

    @export
    def set_config(self, config):
        """Sets the config dictionary"""
        for key in config:
            self.config[key] = config[key]
        self.config.save()

    @export
    def get_config(self):
        """Returns the config dictionary"""
        return self.config.config
