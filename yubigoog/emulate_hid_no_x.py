import evdev
import time


def token_entry(token, press_return=False, delay=0.05):
    """Emulate token entry by keyboard and optionally press return after."""
    with evdev.UInput() as ui:
        time.sleep(delay)
        for digit in token:
            key = "KEY_{}".format(digit)
            ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.ecodes[key], 1)  # press down
            ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.ecodes[key], 0)  # release
            ui.syn()
            time.sleep(delay)
        if press_return:
            ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.ecodes.KEY_ENTER, 1)
            ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.ecodes.KEY_ENTER, 0)
            ui.syn()
        


# Below seems broken, might want to try again later
# import keyboard


# def token_entry(token, press_return=False, delay=0.05):
#     """Emulate token entry by keyboard and optionally press return after."""
#     for digit in token:
#         keyboard.write(digit, delay)
#     if press_return:
#         keyboard.send(13)
