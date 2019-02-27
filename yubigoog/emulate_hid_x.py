import pyautogui


def token_entry(token, press_return=False, delay=0.05):
    """Emulate token entry by keyboard and optionally press return after."""
    pyautogui.typewrite(token, delay)
    if press_return:
        pyautogui.press('return')
