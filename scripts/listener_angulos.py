#!/usr/bin/env python


import rospy
from tfm_simulacion.msg import angulos

# data = angulos()
x = 0

def callback(data):
    global x
    # rospy.loginfo(rospy.get_caller_id() + 'I heard %s', str(data))
    # rospy.loginfo('hola')
    # rospy.loginfo(data)
    x = data.theta1
    rospy.loginfo(x)
    return x
    

def listener():
    global x

    rospy.init_node('listener', anonymous=True)
    rospy.loginfo(x)
    rospy.Subscriber('angulos_delta', angulos, callback)
    
    
    rospy.loginfo('hol')

    rospy.loginfo('adios')


if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('angulos_delta', angulos, callback)
    rospy.spin()
