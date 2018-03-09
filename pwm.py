import RPi.GPIO as ada
ada.setmode(ada.BOARD)
ada.setup(32,ada.OUT)
p = ada.PWM(32,100000)
p.start(50)
try:
    input('Press return to stop:')
except:
    p.stop()
ada.cleanup()
