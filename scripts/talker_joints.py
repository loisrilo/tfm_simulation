#!/usr/bin/env python
import delta_kinematics
import roslib
import rospy
import std_msgs.msg
from sensor_msgs.msg import JointState

pi = 3.141592653
dtr = pi / 180.

def talker(theta1, theta2, theta3):
    # pub = rospy.Publisher('chatter_joints', JointState, queue_size=10)
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('talker_joints', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
	p = delta_kinematics.forward(45, 40, 30)
	# rospy.loginfo(p)
        # how the fuck should I publish this shit!? now I know, bitch
        joint = JointState()
	joint.header = std_msgs.msg.Header()        
	joint.header.stamp = rospy.Time.now()
	joint.name = ['base_brazo1', 'base_brazo2', 'codo1', 'codo2', 'act_x', 'act_y', 'act_z']
	joint.position = [theta1*dtr, theta2*dtr, theta3*dtr, 0.0, p[1]/1000, p[2]/1000, p[3]/1000]
	joint.velocity = []
	joint.effort = []
        pub.publish(joint)
        # rospy.sleep(1.0)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker(45,40,30)

    except rospy.ROSInterruptException: pass
