#!/usr/bin/env python

import rospy
from tfm_simulacion.msg import angulos
from tfm_delta.msg import Pulsos

pulsos_recibidos = Pulsos()
angulos_envio = angulos()
angulos_envio.theta1 = 0.0
angulos_envio.theta2 = 0.0
angulos_envio.theta3 = 0.0
step = 1.8/8
i = 0
nuevo = 0
hecho = 0


def nopulses():
    pulsos_recibidos.id = int(0)
    pulsos_recibidos.p1f = int(0)
    pulsos_recibidos.p1b = int(0)
    pulsos_recibidos.p2f = int(0)
    pulsos_recibidos.p2b = int(0)
    pulsos_recibidos.p3f = int(0)
    pulsos_recibidos.p3b = int(0)


def actualiza(data):
	global pulsos_recibidos
	global hecho
	pulsos_recibidos = data
	hecho = 0
	# rospy.loginfo('recibido')



def principal():
    rospy.init_node('pulsos_a_angulos', anonymous=False)
    rate = rospy.Rate(62.5)  # 62.5 Hz, T = 16 ms.
    rospy.Subscriber("trenes_pulsos", Pulsos, actualiza)
    pub = rospy.Publisher('angulos_delta', angulos, queue_size=10)
    nopulses()
    i = 0
    step = 0.225
    global hecho
    hecho = 1
    while not rospy.is_shutdown():
        if hecho == 0:
            if pulsos_recibidos.p1f >> i & 0b1:
                angulos_envio.theta1 += step
            if pulsos_recibidos.p1b >> i & 0b1:
                angulos_envio.theta1 -= step
            if pulsos_recibidos.p2f >> i & 0b1:
                angulos_envio.theta2 += step
            if pulsos_recibidos.p2b >> i & 0b1:
                angulos_envio.theta2 -= step
            if pulsos_recibidos.p3f >> i & 0b1:
                angulos_envio.theta3 += step
            if pulsos_recibidos.p3b >> i & 0b1:
                angulos_envio.theta3 -= step
            i += 1
            if i >= 8:
                i = 0
                hecho = 1
        pub.publish(angulos_envio)
        rate.sleep()
		


if __name__ == '__main__':
    try:
        principal()

    except rospy.ROSInterruptException:
        pass
