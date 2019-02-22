'''
    Help strings for guiding users to a working Yubikey setup.
'''
import re

INSTRUCTIONS = {
    'en': {
        'setup': (
                    'Yubikey compatible secret: \033[01;32m{}\033[0m'
                    'Program it into one of the Yubikey\'s slots by using the'
                    'Yubikey personalisation tool. Select the HOTP option.'
                ),
        'generate': 'Your generated TOTP token: \033[01;32m{}\033[0m',
        'short_secret': (
                        'Your secret needs to be 20 characters long for this'
                        'to work (160 bit secret).'
                    ),
        'usb_error_udev': (
                        'To allow this tool to access your Yubikey, you need '
                        'to run the following, to add a rule in your udev '
                        'configuration.\n\n'
                        'sudo cat <<EOF >> /etc/udev/rules.d/10-security-keys'
                        '.rules\n'
                        'SUBSYSTEMS=="usb", ATTRS{idVendor}=="1050", ATTRS'
                        '{idProduct}=="0111|0113|0114|0115|0116|0120|0402|0403'
                        '|0406|0407|0410", TAG+="uaccess"\nEOF\n\n'
                        'Then remove your Yubikey and plug it back in.'
                    )
    }
}

for msg_blck in [INSTRUCTIONS]:
    for lang, messages in msg_blck.items():
        for key, msg in messages.items():
            msg_blck[lang][key] = re.sub(
                r'\ {2,100}',
                ' ',
                re.sub(
                    r'\n\ {2,100}',
                    '\n',
                    msg
                )
            ).strip("\n")
