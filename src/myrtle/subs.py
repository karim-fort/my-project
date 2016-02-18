#!/usr/bin/env python
import rospy
from serial_board import SerialBoard
import sys
import time
import os # for kbhit
from kbhit import KBHit

from std_msgs.msg import String

class SimpleBlink(SerialBoard):

    def main(self):
        analog0 = rospy.Publisher('/analog0',String,queue_size=1)
        rospy.init_node('ArduinoAsip')
        rate = rospy.Rate(10) # 10hz

        try:
            time.sleep(0.5)
            self.asip.set_pin_mode(13, self.asip.OUTPUT)
            time.sleep(0.5)
        except Exception as e:
            sys.stdout.write("Exception caught while setting pin mode: {}\n".format(e))
            self.thread_killer()
            sys.exit(1)

        while True:        
            try:
                #print("reaidng:")
                self.asip.digital_write(13, self.asip.HIGH)
                time.sleep(0.25)
                sys.stdout.write(str(self.asip.analog_read(0)))
                sys.stdout.write('\n')
                self.asip.digital_write(13, self.asip.LOW)
                time.sleep(0.25)
                sys.stdout.write(str(self.asip.analog_read(0)))
                analog0.publish(str(self.asip.analog_read(0)))
                rate.sleep()

                sys.stdout.write('\n')
            except (KeyboardInterrupt, Exception) as e:
                sys.stdout.write("Caught exception in main loop: {}\n".format(e))
                self.thread_killer()
                sys.exit()




# test SimpleBlink
if __name__ == "__main__":
    print("hello")
    SimpleBlink().main()
sys.stdout.write("Quitting!\n")
#os._exit(0)
sys.exit(0)

