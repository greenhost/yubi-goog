"""Help strings for guiding users to a working Yubikey setup."""
import sys


messages = {
    "en_GB": {
        "setup": (
            "Yubikey compatible secret: \033[01;32m{}\033[0m\n"
            "Program it into one of the Yubikey\'s slots by using the"
            "Yubikey personalisation tool. Select the HOTP option."
        ),
        "setup_hint_google_authenticator_secret": (
            "In order for your Yubikey to be able to generate a token, you "
            "will need to supply it with a secret. Some "
            "TOTP/GoogleAuthenticator clients allow you to access those "
            "secrets. Some sites, perhaps the one you want to use this tool "
            "with, just prints it somewhere around the QR code you would "
            "normally scan (do that too, it\'s your backup ;) ). It looks "
            "something like: "
            "\"\033[01;32mBCZPBZH4MDODISMXO4OUWPFUT2LBLQGN\033[0m\".\n\n"
            "Another way to retrieve them is by finding a tool that can "
            "decode a QR code, such as a generic QR code reader app.\n"
            "The data you are looking for when decoding a QR code manually "
            " looks like this (green): "
            "otpauth://totp/Application:alice@appdomain.tld?"
            "secret=\033[01;BCZPBZH4MDODISMXO4OUWPFUT2LBLQGN\033[0m&"
            "issuer=Application"
        ),
        "totp": "Your generated TOTP token: \033[01;32m{}\033[0m",
        "short_secret": (
            "Your secret needs to be 32 characters long for this to work "
            "(80 or 160 bit secret)."
        ),
        "usb_error_udev": (
            "To allow this tool to access your Yubikey, you need to run the "
            "following, to add a rule in your udev configuration.\n\n"
            "sudo cat <<EOF >> /etc/udev/rules.d/10-security-keys.rules\n"
            "SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"1050\", ATTRS"
            "{idProduct}==\"0111|0113|0114|0115|0116|0120|0402|0403"
            "|0406|0407|0410\", TAG+=\"uaccess\"\nEOF\n\n"
            "Then remove your Yubikey and plug it back in."
        ),
        "num_digits": "--digits argument should be 6 or 8.",
        "access_denied": "Can\'t access your Yubikey, permission denied.",
        "maybe_no_x_server": (
            "Can't access your window manager, are you "
            "running on Xorg? If you are not, then you should try the --no-x "
            "argument (requires sudo)."
        ),
        "need_sudo": (
            "The --no-x argument requires sudo because it emulates a hardware "
            "keyboard, bypassing the window manager."
        ),
        "not_common_totp_val": (
            "TOTP usually uses a secret of 80 or 160 bits, this tool uses "
            "the Yubikey's HOTP feature and provides it the current time as a "
            "challenge. Yubikeys default to a secret of 160 bytes. Please "
            "enter a secret length of 80 or 160."
        ),
        "generate": "Your TOTP secret: \033[01;32m{}\033[0m"
    }
}

# Replace messages module by this dict so:
#  - Import messages instead of messages.messages
#  - Allow methods of Dict, e.g. `__get_attr__(attr)` and `.get(attr, default)`
sys.modules[__name__] = messages
