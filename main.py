"""
For library usage and definitions, open their respective .py files
For an overview of the code project, open the ReadMe file
"""
import os

import RPi.GPIO as GPIO

import Pi7SegPy as Pi7Seg
import PiShiftPy as shift
import ProjectClass as Conservation
import client as cli

# Start globals
# Projects hold all the relevant settings like data pins and interrupt pins
project0 = Conservation.Project()
project1 = Conservation.Project()
project2 = Conservation.Project()
project3 = Conservation.Project()
# currentInterruptChannel is used as a way to signal which project display to update
currentInterruptChannel = 0
# listOfProjects is used to iterate through all projects for pin setup
listOfProjects = []
# interrupt_flag is used to get out of the callback fast
interrupt_flag = False


# End globals


def setup_gpio():
    """
    This function sets the pin polarity (input or output).
    Uses the global listOfProjects.
    listOfProjects is populated by the set_project_pins function.
    """
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)

    for i in range(len(listOfProjects)):
        GPIO.setup(listOfProjects[i].segmentData, GPIO.OUT)
        GPIO.setup(listOfProjects[i].segmentClock, GPIO.OUT)
        GPIO.setup(listOfProjects[i].segmentLatch, GPIO.OUT)
        GPIO.output(listOfProjects[i].segmentData, GPIO.LOW)
        GPIO.output(listOfProjects[i].segmentClock, GPIO.LOW)
        GPIO.output(listOfProjects[i].segmentLatch, GPIO.LOW)
        GPIO.setup(listOfProjects[i].firstInterrupt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(listOfProjects[i].secondInterrupt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(listOfProjects[i].firstInterrupt, GPIO.FALLING, callback=my_callback, bouncetime=350)
        GPIO.add_event_detect(listOfProjects[i].secondInterrupt, GPIO.FALLING, callback=my_callback, bouncetime=350)


def set_project_pins():
    """
    This function sets up the pins used by each project.
    Reference the pinout.png and ProjectClass file.
    """
    global listOfProjects

    project0.init(2, 3, 4, "project0", 14, 15, 0)
    project1.init(17, 27, 22, "project1", 23, 24, 0)
    project2.init(10, 9, 11, "project2", 25, 8, 0)
    project3.init(5, 6, 13, "project3", 16, 20, 0)

    # this list is used in the setup_gpio function to initiate appropriate pins
    listOfProjects.append(project0)
    listOfProjects.append(project1)
    listOfProjects.append(project2)
    listOfProjects.append(project3)


def my_callback(channel):
    """
    Callback function to detect interrupts from sensors
    """
    global interrupt_flag
    global currentInterruptChannel

    currentInterruptChannel = channel
    interrupt_flag = True


def show_number(this_project, n_or_i):
    """
    Increments number and outputs to 7 segment display
    """
    shift.write_all(0)
    if n_or_i:
        this_project.currentNumber += 1
    Pi7Seg.show(list(map(int, str(this_project.currentNumber))))


def read_file_count():
    for i in range(len(listOfProjects)):
        if os.path.exists(listOfProjects[i].storedNumberFileName):
            with open(listOfProjects[i].storedNumberFileName, 'r') as file:
                try:
                    x = file.readline().strip('')
                    listOfProjects[i].current_number = int(x)
                except Exception as e:
                    print(e)
        else:
            with open(listOfProjects[i].storedNumberFileName, 'w') as file:
                try:
                    file.write("0")
                except:
                    print("Can't write internal number. Maybe you have no file permission")
            listOfProjects[i].current_number = 0


def write_number_to_file():
    for i in range(len(listOfProjects)):
        if os.path.exists(listOfProjects[i].storedNumberFileName):
            with open(listOfProjects[i].storedNumberFileName, 'w') as file:
                try:
                    file.write(str(listOfProjects[i].currentNumber))
                except Exception as e:
                    print(e)
        else:
            with open(listOfProjects[i].storedNumberFileName, 'w') as file:
                try:
                    file.write("0")
                except:
                    print("Can't write internal number. Maybe you have no file permission")


def main():
    '''
    Start of Execution
    '''
    global interrupt_flag
    global currentInterruptChannel
    count = 0
    set_project_pins()
    setup_gpio()
    read_file_count()
    while True:
        if count == 800000:
            write_number_to_file()
            try:
                serv_num = cli.get_number('Gorillaz Giraffes')
                print(serv_num)
                gorillaz = int(serv_num[0])
                giraffes = int(serv_num[1])
                if project0.current_number < gorillaz:
                    project0.current_number = gorillaz
                    print(project0.current_number)
                    Pi7Seg.init(project0.segment_data, project0.segment_clock, project0.segment_latch, 7, 7,
                                common_cathode_type=False)
                    show_number(project0, False)
                if project1.current_number < giraffes:
                    project1.current_number = giraffes
                    print(project1.current_number)
                    Pi7Seg.init(project1.segment_data, project1.segment_clock, project1.segment_latch, 7, 7,
                                common_cathode_type=False)
                    show_number(project1, False)
            except:
                pass
            count = 0
            print("wrote to file")
        if interrupt_flag:
            interrupt_flag = False
            # this logic determines which display to update
            if currentInterruptChannel == 14 or currentInterruptChannel == 15:
                Pi7Seg.init(project0.segment_data, project0.segment_clock, project0.segment_latch, 7, 7,
                            common_cathode_type=False)
                show_number(project0, True)
                try:
                    cli.send_number('Gorillaz ' + str(project0.current_number))
                except:
                    pass
            elif currentInterruptChannel == 23 or currentInterruptChannel == 24:
                Pi7Seg.init(project1.segment_data, project1.segment_clock, project1.segment_latch, 7, 7,
                            common_cathode_type=False)
                show_number(project1, True)
                try:
                    cli.send_number('Giraffes ' + str(project1.current_number))
                except:
                    pass
            elif currentInterruptChannel == 25 or currentInterruptChannel == 8:
                Pi7Seg.init(project2.segment_data, project2.segment_clock, project2.segment_latch, 7, 7,
                            common_cathode_type=False)
                show_number(project2, True)
            elif currentInterruptChannel == 16 or currentInterruptChannel == 20:
                Pi7Seg.init(project3.segment_data, project3.segment_clock, project3.segment_latch, 7, 7,
                            common_cathode_type=False)
                show_number(project3, True)

        count += 1


if __name__ == "__main__":
    try:
        print("went here")
        # set_project_pins()
        main()
    except Exception as e:
        print(e)
        GPIO.cleanup()
else:
    exit
