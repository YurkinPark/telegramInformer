/**
 * Script: telegraminformer.js
 *     The client-side javascript code for the TelegramInformer plugin.
 *
 * Copyright:
 *     (C) Yuriy Shupenko 2023 <yurkinpark@gmail.com>
 *
 *     This file is part of TelegramInformer and is licensed under GNU GPL 3.0, or
 *     later, with the additional special exception to link portions of this
 *     program with the OpenSSL library. See LICENSE for more details.
 */

Ext.ns('Deluge.ux.preferences');

/**
 * @class Deluge.ux.preferences.TelegramInformerPage
 * @extends Ext.Panel
 */
Deluge.ux.preferences.TelegramInformerPage = Ext.extend(Ext.Panel, {
    title: _('Telegram informer'),
    header: false,
    layout: 'fit',
    border: false,

    initComponent: function () {
        Deluge.ux.preferences.TelegramInformerPage.superclass.initComponent.call(this);

        this.form = this.add({
            xtype: 'form',
            layout: 'form',
            border: false,
            autoHeight: true,
        });

        fieldset = this.form.add({
            xtype: 'fieldset',
            border: false,
            title: '',
            autoHeight: true,
            labelAlign: 'top',
            labelWidth: 80,
            defaultType: 'textfield',
        });

        this.botApiKey = fieldset.add({
            fieldLabel: _('Bot API key:'),
            labelSeparator: '',
            name: 'botApiKey',
            width: '97%',
        });

        this.userId = fieldset.add({
            fieldLabel: _('User ID:'),
            labelSeparator: '',
            name: 'userId',
            width: '97%',
        });

        this.on('show', this.updateConfig, this);
    },

    onApply: function () {
        // build settings object
        var config = {};

        config['botApiKey'] = this.botApiKey.getValue();
        config['userId'] = this.userId.getValue();

        deluge.client.telegraminformer.set_config(config);
    },

    onOk: function () {
        this.onApply();
    },

    updateConfig: function () {
        deluge.client.telegraminformer.get_config({
            success: function (config) {
                this.botApiKey.setValue(config['botApiKey']);
                this.userId.setValue(config['userId']);
            },
            scope: this,
        });
    },
});

Deluge.plugins.TelegramInformerPlugin = Ext.extend(Deluge.Plugin, {
    name: 'Telegram informer',

    onDisable: function() {
        deluge.preferences.removePage(this.prefsPage);
    },

    onEnable: function() {
        this.prefsPage = deluge.preferences.addPage(
            new Deluge.ux.preferences.TelegramInformerPage());
    }
});
Deluge.registerPlugin('TelegramInformer', Deluge.plugins.TelegramInformerPlugin);
