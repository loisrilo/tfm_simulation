#!/usr/bin/env python
import delta_kinematics
import codos
import roslib
import rospy
import std_msgs.msg
from sensor_msgs.msg import JointState

pi = 3.141592653
dtr = pi / 180.

angulos = [87, 2, 32]
punto = [53.93, -20.0572, 414.4331]
err_vis = 1


def talker(theta1, theta2, theta3):
    # pub = rospy.Publisher('chatter_joints', JointState, queue_size=10)
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('talker_joints', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        p = delta_kinematics.forward(angulos[0], angulos[1], angulos[2])
        punto = [p[1],p[2],p[3]]
        c1 = codos.punto_codo(angulos[0])
        p1 = codos.punto_ee(punto, 1)
        [a1_a, a1_b] = codos.angulos_codo(c1, p1, 1)
        c2 = codos.punto_codo(angulos[1])
        c2 = codos.rotacion120(c2)
        p2 = codos.punto_ee(punto, 2)       
        [a2_a, a2_b] = codos.angulos_codo(c2, p2, 2)
        c3 = codos.punto_codo(angulos[2])
        c3 = codos.rotacion120(c3)
        c3 = codos.rotacion120(c3)
        p3 = codos.punto_ee(punto, 3)
        [a3_a, a3_b] = codos.angulos_codo(c3, p3, 3)
        # rospy.loginfo(p)      
        joint = JointState()
        joint.header = std_msgs.msg.Header()
        joint.header.stamp = rospy.Time.now()
        joint.name = ['base_brazo1', 'base_brazo2', 'base_brazo3', 'codo1_a', 'codo1_b', 'codo2_a', 'codo2_b', 'codo3_a', 'codo3_b', 'act_x', 'act_y', 'act_z']
        joint.position = [theta1 * dtr, theta2 * dtr, theta3 * dtr, theta1 * dtr + a1_a, -a1_b*err_vis, theta2 * dtr + a2_a, -a2_b*err_vis, theta3 * dtr + a3_a, -a3_b*err_vis, p[1] / 1000, -p[2] / 1000, p[3] / 1000]
        joint.velocity = []
        joint.effort = []
        pub.publish(joint)
        # rospy.sleep(1.0)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker(angulos[0], angulos[1], angulos[2])

    except rospy.ROSInterruptException:
        pass
