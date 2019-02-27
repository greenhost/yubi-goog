#!/usr/bin/env python
"""
Generate TOTP tokens utilising HOTP functions of the Yubikey.

Get your Yubikeys here: https://www.yubico.com/

The MIT License (MIT)

Copyright (c) 2016 Greenhost

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import base64
import re
import binascii
import subprocess
import time
import struct
import platform
import yubico
import usb
import yubigoog.messages as messages

DEFAULT_STEP = 30

__author__ = ["Chris Snijder"]
__copyright__ = "MIT"
__license__ = "The MIT License (MIT)"
__version__ = "0.2"


class YubiGoog:
    """Generate TOTP tokens utilising HOTP functions of the Yubikey."""

    def __init__(self, args, locale):
        """Init a class of YubiGoog to hold options and variables."""
        self.messages = messages.get(locale, messages['en_GB'])
        self.args = args
        command = self.args['command']
        if command == 'setup':
            self.ytg_setup()
        elif command == 'yubi':
            self.msg('generate', self.ytg_yubi())
        elif command == 'hid':
            self.ytg_yubi(True)
        else:
            print("Invalid command given.")
            exit(99)

    def ytg_get_secret(self):
        """Get secret from CLI args or ask for it interactively if not set."""
        secret = self.args.get('secret', None)
        if secret is None:
            self.msg('setup_hint_google_authenticator_secret')
            secret = input("Google Authentication secret: ")

        secret = re.sub(r'\s', '', secret).upper()
        secret = secret.encode('ascii')
        return base64.b32decode(secret)

    def ytg_setup(self):
        """Convert the secret from binary to a hexlified string."""
        secret = self.ytg_get_secret()
        # TODO: find out how to do this with more common 128 bit secrets
        if len(secret) != 20:
            self.msg('short_secret')
            exit(1)
        secret = binascii.hexlify(secret)
        self.msg('setup', secret)

    def _gen_token_mac(self, yubi_slot, digits):
        cmd = ['ykchalresp', '-t', '-%d' % digits, '-%d' % yubi_slot]
        try:
            token = subprocess.check_output(cmd).strip()
        except subprocess.CalledProcessError:
            # ykchalresp failed but it already printed an error..
            exit(1)
        return token

    def gen_token(self):
        """Generate a TOTP token using a Yubikey."""
        slot = self.args.get('slot', 1)
        digits = self.args.get('digits', 6)

        if digits not in (6, 8):
            self.msg('num_digits')
            exit(1)

        # If we're running on a Mac, we need to use Yubico's CLI tool to bypass
        # libusb which is broken on Mac.
        if platform.system() == "Darwin":
            return self._gen_token_mac(slot, digits)

        try:
            yk = yubico.find_yubikey(debug=self.args['debug'])
        except yubico.yubikey_base.YubiKeyError as exc:
            print(exc.reason)
            exit(2)
        except usb.core.USBError as exc:
            if exc.errno == 13:
                self.msg('access_denied')
                if platform.system() == 'Linux':
                    self.msg('usb_error_udev')
                else:
                    print(exc)
                    raise
                exit(2)
            else:
                raise
        # Convert time to struct
        secret = struct.pack("> Q", int(time.time()) // DEFAULT_STEP)
        # Pad the struct time with zero bytes
        secret = secret.ljust(64, b"\x00")

        response = yk.challenge_response(secret, slot=slot)

        token = '%.*i' % (
            digits,
            yubico.yubico_util.hotp_truncate(response, length=digits)
        )
        return token

    def ytg_yubi(self, emulate_keyboard=False):
        """Let the Yubikey do a challenge response."""
        token = self.gen_token()
        if emulate_keyboard:
            delay = self.args.get('emulate_speed', 50) / 1000
            do_return = self.args['emulate_return']
            if not self.args['no_x']:
                try:
                    import Xlib
                    import yubigoog.emulate_hid_x as emulate_hid
                    emulate_hid.token_entry(token, do_return, delay)
                except Xlib.error.XauthError:
                    self.msg("maybe_no_x_server")
            else:
                try:
                    import yubigoog.emulate_hid_no_x as emulate_hid
                    emulate_hid.token_entry(token, do_return, delay)
                except ImportError:
                    self.msg("need_sudo")
        else:
            return token

    def msg(self, message, format_args=None):
        """Print instruction from the message file, optionally format it."""
        # Get a message or fall back to English
        msg = self.messages.get(message, messages['en_GB'][message])
        if format_args:
            msg = msg.format(format_args)
        print(msg)