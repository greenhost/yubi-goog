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
import sys
import subprocess
import argparse
import time
import struct
import platform
import yubico
import usb
from messages import INSTRUCTIONS

__author__ = ["Chris Snijder"]
__copyright__ = "MIT"
__license__ = "The MIT License (MIT)"
__version__ = "0.2"

DEFAULT_STEP = 30


def ytg_get_secret(secret=None):
    """
        Get the secret from the command line arguments or ask for it
        interactively if not set.
    """
    if secret is None:
        secret = raw_input("Google Authentication secret: ")

    secret = re.sub(r'\s', '', secret).upper()
    secret = secret.encode('ascii')
    return base64.b32decode(secret)


def ytg_setup(secret):
    """
        Convert the secret from binary to a hexlified string.
    """
    if len(secret) != 20:
        print(INSTRUCTIONS['en']['short_secret'])
        exit(1)
    return binascii.hexlify(secret)


def _gen_token_mac(yubi_slot, digits):
    if digits not in (6, 8):
        print("--digits argument should be 6 or 8.")
        exit(1)

    cmd = ['/usr/local/bin/ykchalresp', '-t', '-%d' % digits, '-%d' % yubi_slot]

    try:
        token = subprocess.check_output(cmd).strip()
    except subprocess.CalledProcessError as exc:
        sys.exit(1)
    return token


def _gen_token(yubi_slot, digits):
    try:
        yk = yubico.find_yubikey(debug=False)
    except yubico.yubikey_base.YubiKeyError as exc:
        print(exc.reason)
        exit(2)
    except usb.core.USBError as exc:
        if exc.errno == 13:
            print("Can't access your Yubikey, permission denied.")
            if platform.system() == 'Linux':
                print(INSTRUCTIONS['en']['usb_error_udev'])
            else:
                print(exc)
                raise
            exit(2)
        else:
            raise
    secret = struct.pack(
        "> Q", int(time.time()) // DEFAULT_STEP).ljust(64, b"\x00")

    response = yk.challenge_response(secret, slot=yubi_slot)

    token = '%.*i' % (
        digits,
        yubico.yubico_util.hotp_truncate(response, length=digits)
    )
    return token


def ytg_yubi(yubi_slot=1, digits=6, emulate_keyboard=False,
             emulate_return=False, emulate_speed=0.05):
    """
        Instead of using a supplied secret, let the Yubikey do the
        challenge response.
    """
    # If we're running on a Mac, we need to use Yubico's CLI tool to bypass
    # libusb which is broken on Mac.
    if platform.system() == "Darwin":
        token = _gen_token_mac(yubi_slot, digits)
    else:
        token = _gen_token(yubi_slot, digits)

    if emulate_keyboard:
        import pyautogui
        pyautogui.typewrite(token, emulate_speed)
        if emulate_return:
            pyautogui.press('return')
    else:
        return token


def main():
    """
        Figure out what the user intends to do and call the corresponding
        functions, to find out which functions are supported use the --help
        argument.
    """

    parser = argparse.ArgumentParser(
        prog=__file__,
        description='Generate TOTP token with your Yubikey.',
        conflict_handler='resolve'
    )

    sparser = parser.add_subparsers(
        title='Positional arguments',
        metavar='[subcommands]',
        dest='command',
    )

    setup = sparser.add_parser(
        'setup',
        help='Convert your TOTP secret to a Yubikey compatible format.'
    )

    hid = sparser.add_parser(
        'hid',
        help='Enter TOTP token generatd by Yubikey (keyboard emulation).'
    )

    yubi = sparser.add_parser(
        'yubi',
        help='Output TOTP token generatd by Yubikey.'
    )

    setup.add_argument(
        '-s',
        '--secret',
        required=False,
        metavar='[secret]',
        help='Specify the Google Authentication secret.',
        type=str
    )

    for obj in (yubi, hid):
        obj.add_argument(
            '--slot',
            required=False,
            metavar='[1/2]',
            help='In which Yubikey slot did you save your secret?',
            type=int,
            default=1
        )
        obj.add_argument(
            '--digits',
            metavar='[6/8]',
            help='How many digits should the output have?',
            type=int,
            default=6
        )

    hid.add_argument(
        '--speed',
        metavar='[50ms]',
        help='How fast should I type? (emulation)',
        type=int,
        default=50,
        dest='emulate_speed'
    )

    hid.add_argument(
        '--return',
        action="store_true",
        help='Should I press enter after entering your token? (emulation)',
        dest='emulate_return'
    )

    try:
        args = parser.parse_args().__dict__

        if 'command' in args.keys():
            command = args['command']
        else:
            parser.print_help()
            exit(1)

        if command == 'setup':
            secret = args.pop('secret', None)
            secret = ytg_get_secret(secret)
        if command == 'setup':
            print(INSTRUCTIONS['en']['setup'].format(ytg_setup(secret)))
        elif command == 'yubi':
            print(INSTRUCTIONS['en']['generate'].format(
                ytg_yubi(args['slot'], args['digits'])
            ))
        elif command == 'hid':
            ytg_yubi(
                args['slot'],
                args['digits'],
                emulate_keyboard=True,
                emulate_speed=args['emulate_speed'] / 1000,
                emulate_return=args['emulate_return']
            )
    except KeyboardInterrupt:
        print()
        exit(1)


if __name__ == "__main__":
    main()
