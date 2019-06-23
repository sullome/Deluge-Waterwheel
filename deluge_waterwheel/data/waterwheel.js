/**
 * Script: waterwheel.js
 *     The client-side javascript code for the Waterwheel plugin.
 *
 * Copyright:
 *     (C) Constantine Farrahov 2019 <sullome.techie@gmail.com>
 *
 *     This file is part of Waterwheel and is licensed under GNU GPL 3.0, or
 *     later, with the additional special exception to link portions of this
 *     program with the OpenSSL library. See LICENSE for more details.
 */

WaterwheelPlugin = Ext.extend(Deluge.Plugin, {
    constructor: function(config) {
        config = Ext.apply({
            name: 'Waterwheel'
        }, config);
        WaterwheelPlugin.superclass.constructor.call(this, config);
    },

    onDisable: function() {
        deluge.preferences.removePage(this.prefsPage);
    },

    onEnable: function() {
        this.prefsPage = deluge.preferences.addPage(
            new Deluge.ux.preferences.WaterwheelPage());
    }
});
new WaterwheelPlugin();
