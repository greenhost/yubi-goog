# yubi-goog

Google Authenticator is great, but I don't really want to be tied to my mobile phone for logging into Google Services. Yubikey is the ideal form factor for a two-factor authentication device, so why not integrate the two? 

**Well now, you can!**

## Prerequisites

* Python >=2.7
* `ykchalresp` (found in the yubikey-personalization package)
* Yubikey
* [Cross-platform GUI Personalization tool][tool]
* `pyautogui` - Run: `sudo pip install pyautogui` to install it.

## Usage

1. Set up Google Authenticator on your Google settings like you would for a mobile phone.
2. Below the QR code, press the expand button so you can see your base32-encoded
   secret key.
3. Run `./yubi_goog.py setup` this will prompt you for your base32-encoded secret and output a result in hex.
4. Program that secret into your Yubikey as a HMAC-SHA1 challenge-response key. I had to use the [GUI tool available from Yubico][tool]
5. Whenever you are prompted for a one-time password from google, just run `./yubi_goog.py yubi` and the output will be a one-time password usable for up to one minute 30 seconds.

    Alternatively, run `./yubi_goog.py hid` to employ keyboard emulation that will type the token for you.
    __Hint:__ Use this with a keyboard shortcut!

Options for each sub-command can be discovered with the `-h` flag, e.g.: 

```console
$ ./yubi_goog.py hid -h
usage: ./yubi_goog.py hid [-h] [-s [secret]] [--slot [1/2]] [--speed [50ms]]
                          [--return]

optional arguments:
  -h, --help            show this help message and exit
  -s [secret], --secret [secret]
                        Specify the Google Authentication secret.
  --slot [1/2]          In which Yubikey slot did you save your secret?
  --speed [50ms]        How fast should I type? (emulation)
  --return              Should I press enter after entering your token?
                        (emulation)
```

[tool]: http://wiki.yubico.com/files/YubiKey%20Personalization%20Tool%20Installer-lin.tgz
