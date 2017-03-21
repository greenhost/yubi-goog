# yubi-goog

Google Authenticator is great, but I don't really want to be tied to my mobile
phone for logging into Google Services. Yubikey is the ideal form factor for a
two-factor authentication device, so why not integrate the two?

**Well now, you can!**

## Prerequisites

* Python >=2.7
* Yubikey
* [Cross-platform GUI Personalization tool][tool] (for setting up your Yubikey)

## Installation

We recommend you create a "virtualenv" to prevent the dependencies from
cluttering your system

``` bash
# If you haven't already:
apt-get install virtualenv

git clone https://github.com/greenhost/yubi-goog ./
cd yubi-goog
virtualenv ./env
source ./env/bin/activate
pip install -r requirements.txt
chmod u+x yubi_goog.py
```
You should now be able to run this to test everything works:

``` bash
$ ./yubi_goog.py -h
usage: ./yubi_goog.py [-h] [subcommands] ...

Generate TOTP token with your Yubikey.

optional arguments:
  -h, --help     show this help message and exit

Positional arguments:
  [subcommands]
    setup        Convert your TOTP secret to a Yubikey compatible format.
    hid          Enter TOTP token generatd by Yubikey (keyboard emulation).
    yubi         Output TOTP token generatd by Yubikey.

```

## Usage

1. Set up Google Authenticator on your Google settings like you would for a
   mobile phone.
2. Below the QR code, press the expand button so you can see your base32-encoded
   secret key.
3. Run `./yubi_goog.py setup` this will prompt you for your base32-encoded
   secret and output a result in hex.
4. Program that secret into your Yubikey as a HMAC-SHA1 challenge-response key.
   I had to use the [GUI tool available from Yubico][tool]
   Alternatively, use `ykpersonalize -2 -ochal-resp -ochal-hmac -ohmac-lt64`.
   This will insert the secret in slot 2 of your yubikey (use -1 for slot 1)
5. Whenever you are prompted for a one-time password from google, just run
   `./yubi_goog.py yubi` and the output will be a one-time password usable for
   up to one minute 30 seconds.

    Alternatively, run `./yubi_goog.py hid` to employ keyboard emulation that
    will type the token for you.
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
