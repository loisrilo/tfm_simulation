#!/usr/bin/env python

import rospy
from tfm_simulacion.msg import angulos
import time

# revisar donde va esto
ang = angulos()

#codigo talker sin modificar
def talker():
    pub = rospy.Publisher('angulos_delta', angulos, queue_size=10)
    rospy.init_node('angulos_pub', anonymous=False)
    rate = rospy.Rate(5) # 10hz
    while not rospy.is_shutdown():
        ang.theta1 = 19
        ang.theta2 = 32
        ang.theta3 = 41
        rospy.loginfo(ang)
        pub.publish(ang)
        time.sleep(0.5)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass