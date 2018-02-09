import RPi.GPIO as ada

print '{} is the version type.' .format(ada.VERSION)

ada.setmode(ada.BCM)
count = 0
ada.setup(24, ada.IN, pull_up_down=ada.PUD_DOWN)
ada.setup(23, ada.IN, pull_up_down=ada.PUD_UP)
def my_callback(channel):
    global count
    count += 1
    print '{} is the current count' .format(count)

ada.add_event_detect(24, ada.RISING, callback=my_callback, bouncetime=200)


print 'waiting for edge'
ada.wait_for_edge(23, ada.FALLING)

ada.cleanup()

print 'test'
