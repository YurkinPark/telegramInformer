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

from gi.repository import Gtk

import deluge.component as component
from deluge.plugins.pluginbase import Gtk3PluginBase
from deluge.ui.client import client

from . import common

log = logging.getLogger(__name__)


class Gtk3UI(Gtk3PluginBase):
    def enable(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(common.get_resource('config.ui'))
        component.get('Preferences').add_page('TelegramInformer', self.builder.get_object('prefs_box'))
        component.get('PluginManager').register_hook('on_apply_prefs', self.on_apply_prefs)
        component.get('PluginManager').register_hook('on_show_prefs', self.on_show_prefs)

    def disable(self):
        component.get('Preferences').remove_page('TelegramInformer')
        component.get('PluginManager').deregister_hook(
            'on_apply_prefs', self.on_apply_prefs)
        component.get('PluginManager').deregister_hook(
            'on_show_prefs', self.on_show_prefs)

    def on_apply_prefs(self):
        config = {
            'botApiKey': self.builder.get_object('botApiKey').get_text(),
            'userId': self.builder.get_object('userId').get_text()
        }
        log.debug(f'Applying config {config}')
        client.telegraminformer.set_config(config)

    def on_show_prefs(self):
        client.telegraminformer.get_config().addCallback(self.cb_get_config)

    def cb_get_config(self, config):
        """callback for on show_prefs"""
        self.builder.get_object('botApiKey').set_text(config['botApiKey'])
        self.builder.get_object('userId').set_text(config['userId'])
