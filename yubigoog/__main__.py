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

import locale
import argparse
import yubigoog.yubigoog


def parse_args():
    """
    Parse CLI arguments.

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

    generate = sparser.add_parser(
        'generate',
        help=(
            'Generate a yubikey compatible secret. Use this only if you can'
            ' choose your own secret value in an application (not common).'
        )
    )

    setup.add_argument(
        '-s',
        '--secret',
        required=False,
        metavar='[secret]',
        help='Specify the Google Authentication secret.',
        type=str
    )

    generate.add_argument(
        '-n',
        '--length',
        required=False,
        metavar='[128/160]',
        default=160,
        help='Specify a length in bits. (default: 160)',
        type=int
    )

    for obj in (yubi, hid, generate):
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
        obj.add_argument(
            '-d',
            '--debug',
            help=(
                'Enable debug mode (outputs some python-yubico debug '
                'messages.'
            ),
            action='store_true'
        )
        obj.add_argument(
            '--expert',
            help=(
                'Reduces error checking, allows uncommon values to be chosen,'
                ' e.g.: secrets with a non-standard length.'
            ),
            action='store_true'
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
        action='store_true',
        help='Should I press enter after entering your token? (emulation)',
        dest='emulate_return'
    )

    hid.add_argument(
        '--no-x',
        action='store_true',
        help=(
            "Use this if you are not using an X window manager, you will "
            "need to `sudo yubigoog`, because this needs to emulate a "
            "hardware keyboard."
        ),
        dest="no_x"
    )

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        exit(1)
    return vars(args)


def main():
    try:
        yubigoog.yubigoog.YubiGoog(parse_args(), locale.getlocale()[0])
    except KeyboardInterrupt:
        print()
        exit(1)


if __name__ == '__main__':
    main()
