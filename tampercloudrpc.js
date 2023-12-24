// ==UserScript==
// @name         Soundcloud Rich Presence
// @namespace    https://github.com/xionerme/soundcloud-discord-rpc
// @version      1.0.0
// @description  Adds Discord Rich Presence support to Soundcloud.
// @author       3j333
// @match        https://soundcloud.com/*
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {
    'use strict';

    const serverUrl = 'http://127.0.0.1:7769';

    function updateRichPresence(html) {
        try {
            GM_xmlhttpRequest({
                method: 'POST',
                url: `${serverUrl}/updateRichPresence`,
                headers: {
                    'Content-Type': 'application/json',
                },
                data: JSON.stringify({ html: html }),
                onload: function(response) {
                    console.log('Server response:', response.responseText);
                },
                onerror: function(error) {
                    console.error('Error:', error);
                },
            });
        } catch (error) {
            console.error('Caught an error:', error);
        }
    }

    function getDataFromSoundcloud() {
        try {
            const html = document.querySelector('.playControls.g-z-index-control-bar.m-visible').outerHTML;
            updateRichPresence(html);
        } catch (error) {
            console.error('Caught an error:', error);
        }
    }

    setInterval(getDataFromSoundcloud, 1000);
})();



