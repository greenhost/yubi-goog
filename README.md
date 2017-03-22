# yubi-goog

If you're not using 2 factor authentication, you're doing it wrong. Nowadays, lot's of services offer 2FA, often based on TOTP or "Google Authenticator". But TOTP usually requires you to use an app to generate tokens. Generating tokens can be tedious. When you want to login to a service, you need to:

 1. Take out your phone and unlock it.
 2. Start up the TOTP/Google Authenticator app and generate a token.
 3. Manually type it into the field, before it expires.

What if we could reduce this to:

 1. Plugin your yubikey
 2. Press `Ctrl+Y` or `Cmd+Y` or whatever shortcut you prefer.

Besides, if you are a yubikey user, chances are, step 1 is already completed anyway, so you can authenticate with just the shortcut.

## Caveats

If this all sounds too good to be true, well maybe it is..

 - Your Yubikey only has 2 slots, you can only use this for a maximum of 2 services, assuming they are even empty.
 - It is not common for services to let you choose your own key, Yubikeys require a key length of 160 bits, which means your secret in hexadecimal form should be 20 characters long for this to work.
 - You need access to your key in the first place. Most interfaces allow you to manually enter the secret into an app, in case the app doesn't support scanning QR-codes, or scanning fails. If the interface doesn't show your key, you would need to extract it from the QR-code or from the app.

## Prerequisites

* Python >=2.7
* Yubikey

## Installation

You will need to setup your Yubikey with the Yubikey personalisation tool, you can download it [here](https://www.yubico.com/support/knowledge-base/categories/articles/yubikey-personalization-tools/). Instead you can install [`ykpersonalize`](https://github.com/Yubico/yubikey-personalization) if you prefer a command line tool.

We recommend you create a "virtualenv" to prevent the dependencies from cluttering your system.

If you haven't already, install `virtualenv` and `pip`. Optionally you can install `git` but if you don't want to, you can download the zipped source code directly [zip](https://github.com/greenhost/yubi-goog/archive/master.zip) and unzip it (the commands below assume you will use git).

### On Debian/Ubuntu

``` console
$ sudo apt-get install git-all python-setuptools virtualenv
$ git clone https://github.com/greenhost/yubi-goog ./
$ cd yubi-goog
$ virtualenv ./env
$ source ./env/bin/activate
$ pip install -r requirements.txt
```

### On Fedora/CentOS/Redhat

``` console
$ sudo yum install git-all python-pip python-virtualenv
$ git clone https://github.com/greenhost/yubi-goog ./
$ cd yubi-goog
$ virtualenv ./env
$ source ./env/bin/activate
$ pip install -r requirements.txt
```

### On macOS

Make sure you have `pip` and `virtualenv` and `ykchalresp` installed. If you haven't yet, you *can* use homebrew, or any method you prefer. You can find a guide on installing homebrew, pip and virtualenv [here](http://docs.python-guide.org/en/latest/starting/install/osx/).

Installing dependencies using homebrew:

```console
$ brew install git python ykpers
$ git clone https://github.com/greenhost/yubi-goog ./
$ cd yubi-goog
$ virtualenv ./env
$ source ./env/bin/activate
$ pip install pyobjc-core 
$ pip install pyobjc 
$ pip install -r requirements.txt
```

## Usage

You should now be able to run this to test everything works:

```console
$ python ./yubi_goog.py -h
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

1. Set up TOTP/"Google Authenticator" with a Google Authenticator app, at the service you want to use your Yubikey with. You will probably want to use the app as a backup so don't delete the account when you're done.
2. Usually somewhere near the QR code, there is a string of random characters between 15 and 20 characters long, this is your secret.
3. Run `./yubi_goog.py setup` this will prompt you for your base32-encoded   secret and output a result in hex.
4. Program that secret into your Yubikey as a HMAC-SHA1 challenge-response key using the [GUI tool available from Yubico][tool]. Alternatively, use `ykpersonalize -2 -ochal-resp -ochal-hmac -ohmac-lt64`. This will insert the secret in slot 2 of your yubikey (use -1 for slot 1)
5. Whenever you are prompted for a one-time password from google, just run `./yubi_goog.py yubi` and the output will be a one-time password usable for
   up to one minute 30 seconds.
  Alternatively, run `./yubi_goog.py hid` to employ keyboard emulation that will type the token for you.
  __Hint:__ Use this with a keyboard shortcut!

Options for each sub-command can be discovered with the `-h` flag, e.g.:

### Keyboard shortcuts

#### Linux

Find keyboard shortcuts in the preferences of your window manager and add an entry, it should allow you to start commands directly. Alternatively install [`xbindkeys`](http://www.nongnu.org/xbindkeys/xbindkeys.html) and follow it's instructions to create a shortcut that is not window manager dependent.

The command you enter into the shortcut should contain the full path to the python executable in the virtualenv you created followed by the full path of the `yubi_goog.py` file, followed by `hid` and any additional arguments, such as `--return` to emulate pressing return after entering the numbers. All together:

```
[PATH TO YOUR yubi-goog DIR]/env/bin/python [PATH TO YOUR yubi-goog DIR]/yubi_goog.py hid --return
```

#### macOS

If you are running this on macOS there is no easy way of running the command simply by a short-cut. Instead you need to create an Automator Service that runs the command.

Steps:

 1. Open automator, choose *New document*, select *Service*.
 2. In the left panel, click on *Utilities*, then *Run Shell Script*.
 3. Paste the following into the Shell Script panel:
 ```
 YUBI_GOOG_DIR=~/[PATH TO YOUR yubi-goog DIR]
 $YUBI_GOOG_DIR/env/bin/python $YUBI_GOOG_DIR/yubi_goog.py hid --return
 ```
 Replace `[PATH TO YOUR yubi-goog DIR]` by the directory where you installed `yubi-goog` (without brackets).
 4. Save as "YubiGoog".
 5. Go to *System Preferences* and click on *Keyboard*, select the *Shorcut* tab.
 6. Select *Services* in the left column and scroll down to find "YubiGoog", click on it.
 7. Click on *Add Shorcut* now press `Cmd+Y` or any other keyboard shortcut you prefer.

You should now be able to get 2FA tokens by pressing `Cmd+Y`.


### Other options

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

