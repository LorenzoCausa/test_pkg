#!/usr/bin/env python3

# IMPORTS
import rospy
import roslib

from geometry_msgs.msg import Pose 
from my_custom_interfaces.msg import Drone_cmd
from std_msgs.msg import Float32

# GLOBAL VARIABLES
x=float(0)
y=float(0)
angle=float(0)
ground_distance=float(3)

old_x=float(0)
old_y=float(0)
old_angle=float(0)
old_ground_distance=float(3)

P_gain_yaw=1
D_gain_yaw=20

P_gain_throttle=1
D_gain_throttle=10

P_gain_pitch=0.001
D_gain_pitch=0.005

# FUNCTIONs
def update_olds():
    global old_x,old_y,old_angle,old_ground_distance
    old_x=x 
    old_y=y
    old_angle=angle
    old_ground_distance=ground_distance

# SUBSCRIBERs CALLBACK
def callback_loc(pose):
    global x,y,angle
    x=pose.position.x
    y=pose.position.y
    angle=pose.orientation.z-90

def callback_ground(distance):
    global ground_distance
    ground_distance=distance.data

def main():
    rospy.init_node('drone_controller', anonymous=False)
    rospy.Subscriber("localization", Pose, callback_loc,queue_size=1)
    rospy.Subscriber("ground_distance", Float32, callback_ground,queue_size=1)
    command_pub=rospy.Publisher("command", Drone_cmd, queue_size=1)

    cmd=Drone_cmd()
    rate = rospy.Rate(20) # 20hz 

    while not rospy.is_shutdown():
        cmd.yaw =     -P_gain_yaw*angle - D_gain_yaw*(angle-old_angle) # signs may be due to the inverted image of the simulation
        cmd.throttle = P_gain_throttle*(4 - ground_distance) - D_gain_throttle*(ground_distance-old_ground_distance)
        cmd.pitch =    P_gain_pitch*x - D_gain_pitch*(x-old_x)
        print("P part: ", P_gain_pitch*x,", D part: ",D_gain_pitch*(x-old_x)) 
        update_olds()

        if(abs(x)<100 and abs(angle<20)):
            cmd.roll=1
        else:
            cmd.roll=0
            
        command_pub.publish(cmd)
        #print("x:",x,", y:",y,", angle:",angle,", ground distance:",ground_distance)
        rate.sleep()

if __name__ == "__main__":
    main()
