from .config import CONFIG
try:
    import RPi.GPIO as gpio
except RuntimeError:
    print("Error importing RPi.GPIO!  \
        This is probably because you need superuser privileges. \
        You can achieve this by using 'sudo' to run your script")

setmode = CONFIG.get('gpio').get('setmode')
setmode = getattr(gpio, setmode)
gpio.setmode(setmode)
