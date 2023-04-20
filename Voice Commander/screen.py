import screen_brightness_control as sbc
from word2number import w2n
import ctypes
import win32api, win32con


def screen_brightness_up():
    brightness = sbc.get_brightness()
    brightness = min(brightness + 10, 100)
    sbc.set_brightness(brightness, None)

def screen_brightness_down():
    brightness = sbc.get_brightness()
    brightness = max(brightness - 10, 0)
    sbc.set_brightness(brightness, None)

def screen_brightness_set(value):
    value = value.lower()
    try:
        brightness = w2n.word_to_num(value.split("screen brightness set ")[1])
        if brightness > 100 or brightness < 0:
            print('Invalid number')
            return 0
    except:
        print('Invalid number')
    
    sbc.set_brightness(brightness)

def screen_off():
    ctypes.windll.user32.SendMessageW(65535, 274, 61808, 2)

def screen_on():
    ctypes.windll.user32.SendMessageW(65535, 274, 61808, -1)
    screen_move_cursor()

def screen_move_cursor():
    x, y = (0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)