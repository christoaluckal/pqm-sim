#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import sys
import math
from std_srvs.srv import SetBool

# max_speed and max_angle are values that make the calculations normalized
# Checks for user inputted values, if none are provided, defaults to max speed: 10 m/s and max angle: 45 degrees
if(len(sys.argv)<2):
    print("Setting default max_speed:10 \t max_angle:45 degrees")
    max_speed=10
    max_angle=45
else:
    max_speed = float(sys.argv[1])
    max_angle = float(sys.argv[2])

# Store original max_speed to return to default
original_speed = max_speed

# Speed value given to AckermannDrive message
global throttle_ms
throttle_ms = 0

# Steering Angle value given to AckermannDrive message
global steering_angle
steering_angle = 0

# Dont publish anything till start_input is true. Flipped only once during callback
start_input = False

def callback(data):
    '''
        Callback function that subscribes to joy topic and gets sensor_msgs.msg.Joy messages\n
        Input: Joy messages from joy \n
        Computes: Desired speed and steering angles using the current inputs and the max speed and max angle \n
        Sets: Global variables throttle_ms and steering_angle for AckermannDrive message speed and steering angle values
    '''
    global throttle_ms,steering_angle,max_speed,max_angle,original_speed,start_input

    rospy.wait_for_service("/reset_car")
    reset = rospy.ServiceProxy("/reset_car", SetBool)

    if data.buttons[1]:
        try:
            reset_status = reset(True)
            rospy.sleep(0.5)
        except rospy.ServiceException as e:
            rospy.signal_shutdown("Could not reset world")

    # Values from joystick
    throttle_input = data.axes[5]
    reverse_input = data.buttons[2]
    multiplier = data.axes[7]
    # default_speed = data.buttons[1]
    steering_input = data.axes[0]

    max_speed+=(1*multiplier)

    # if(default_speed):
    #     max_speed=original_speed

    # XBOX RT starts at +1 and ends at -1 ie [1,-1]
    # throttle_ms = (max_speed/2)+(max_speed/2)*((-1)*throttle_input)
    throttle_ms = (1-2*reverse_input)*(max_speed/2)*(1-throttle_input)
    # throttle_ms = (max_speed)*((reverse_input-throttle_input)/2)

    # XBOX LS is +1 at left and -1 at right
    # steering_angle = steering_input*max_angle*math.pi/180

    # # Non Linear-ish
    steering_angle = steering_input*max_angle

    start_input = True


def talker():
    '''
    Publisher Subscriber funtion \n
    Publishes AckermannDriver messages to topic car_1/command \n
    Subscribes to Joy messages from joy node \n

    '''
    global throttle_ms,steering_angle
    diff_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('joy_diff_publisher', anonymous=True)
    rospy.Subscriber("/joy", Joy, callback)
    rate = rospy.Rate(50)

    while start_input is False:
        continue

    while not rospy.is_shutdown():
        diff_msg = Twist()
        diff_msg.linear.x = throttle_ms
        diff_msg.angular.z = steering_angle
        diff_pub.publish(diff_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass