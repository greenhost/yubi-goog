'''
    Help strings for guiding users to a working Yubikey setup.
'''
import re

INSTRUCTIONS = {
    'en': {
        'setup': '''
                    Yubikey compatible secret: \033[01;32m%s\033[0m
                    Program it into one of the Yubikey's slots by using the \
                    Yubikey personalisation tool. Select the HOTP option.
                 ''',
        'generate': 'Your generated TOTP token: \033[01;32m%s\033[0m',
        'short_secret': '''
                        Your secret needs to be 20 characters long for this \
                        to work (160 bit secret).
                    '''
    }
}

for msg_blck in [INSTRUCTIONS]:
    for lang, messages in msg_blck.iteritems():
        for key, msg in messages.iteritems():
            msg_blck[lang][key] = re.sub(
                r'\ {2,100}',
                ' ',
                re.sub(
                    r'\n\ {2,100}',
                    '\n',
                    msg
                )
            ).strip("\n")
